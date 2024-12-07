# client.py

import cv2
import numpy as np
import tensorflow as tf
import pickle
import base64
import imutils
import os
from joblib import load
class LivenessDetectionClient:
    def __init__(self, model_path, le_path, encodings_path, detector_folder, confidence=0.5):
        self.confidence = confidence

        # Load the encoded faces and names
        with open(encodings_path, 'rb') as file:
            self.encoded_data = pickle.load(file)

        # Load the face detector model
        proto_path = os.path.sep.join([detector_folder, 'deploy.prototxt'])
        submodel_path = os.path.sep.join([detector_folder, 'res10_300x300_ssd_iter_140000.caffemodel'])
        self.detector_net = cv2.dnn.readNetFromCaffe(proto_path, submodel_path)

        # Load the liveness model and label encoder
        self.liveness_model = tf.keras.models.load_model(model_path)

        # if not os.path.exists(le_path):
        #     print(f"File not found: {le_path}")
        # else:
        #     print("file found")

        try:
            with open(le_path, 'rb') as file:
                self.le = pickle.load(file)
                print("Pickle file loaded successfully:", self.le)
        except Exception as e:
                print("Error loading pickle file:", e)

    def _decode_image(self, image_base64):
        # Decode base64 image
        image_data = base64.b64decode(image_base64)
        return cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)

    def detect_liveness(self, image_base64):
        # Decode and process the image
        image = self._decode_image(image_base64)
        frm = imutils.resize(image, width=800)
        (h, w) = frm.shape[:2]
        
        blob = cv2.dnn.blobFromImage(cv2.resize(frm, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        self.detector_net.setInput(blob)
        detections = self.detector_net.forward()
        
        results = []  # Store results for each face detected
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.confidence:
                # Bounding box for the detected face
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # Ensure bounding box coordinates are within dimensions
                startX, startY = max(0, startX), max(0, startY)
                endX, endY = min(w, endX), min(h, endY)

                # Extract the face ROI
                face = image[startY:endY, startX:endX]

                # Preprocess for the liveness model
                face = cv2.resize(face, (32, 32))
                face = face.astype("float") / 255.0
                face = np.expand_dims(face, axis=0)

                # Predict liveness
                preds = self.liveness_model.predict(face)[0]
                j = np.argmax(preds)
                label = self.le.classes_[j]

                # Add to results
                results.append({
                    "box": (startX, startY, endX, endY),
                    "label": label,
                    "confidence": preds[j]
                })

        # Convert bounding box and confidence to standard types for JSON serialization
        for result in results:
            result["box"] = tuple(map(int, result["box"]))
            result["confidence"] = float(result["confidence"])

        return results
