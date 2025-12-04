import cv2
import os

class ImageAnalyzer:
    def __init__(self):
        # Load the pre-trained face detection model (Haar Cascade)
        # This file comes with OpenCV
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
    
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
        
        return analysis
