import cv2
import os

# Age ranges that the model predicts
AGE_RANGES = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']

class ImageAnalyzer:
    def __init__(self):
        # Load the pre-trained face detection model (Haar Cascade)
        # This file comes with OpenCV
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        # Load age detection model
        age_proto = 'models/age_deploy.prototxt'
        age_model = 'models/age_net.caffemodel'
        self.age_net = cv2.dnn.readNet(age_model, age_proto) 
    
    def analyze_image(self, image_path):
        """
        Analyze an image and detect faces.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with analysis results
        """
        # Read the image
        image = cv2.imread(image_path)
        
        if image is None:
            return {'error': 'Could not read image'}
        
        # Convert to grayscale (face detection works better on grayscale)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=8,
            minSize=(50, 50)
        )
        
        # Build analysis results
        analysis = {
            'faces_detected': len(faces),
            'has_face': len(faces) > 0
        }
        
        # If we found a face, detect age
        if len(faces) > 0:
            # Get the first (largest) face
            (x, y, w, h) = faces[0]
            
            # Extract face region for age detection
            face_img = image[y:y+h, x:x+w].copy()
            
            # Prepare the face for the age model (it expects 227x227 images)
            blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), 
                                         (78.4263377603, 87.7689143744, 114.895847746), 
                                         swapRB=False)
            
            # Predict age
            self.age_net.setInput(blob)
            age_preds = self.age_net.forward()
            age_index = age_preds[0].argmax()
            age_range = AGE_RANGES[age_index]
            
            analysis['age_range'] = age_range
        
        return analysis

