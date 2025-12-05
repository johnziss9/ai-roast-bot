from picamera2 import Picamera2
import time
import os

class Camera:
    def __init__(self):
        """Initialize the camera"""
        self.picam2 = Picamera2()
        # Configure for still image capture
        config = self.picam2.create_still_configuration()
        self.picam2.configure(config)
        
    def capture_image(self, filepath):
        """Capture an image and save it to filepath"""
        try:
            # Start the camera
            self.picam2.start()
            # Give it a moment to adjust exposure
            time.sleep(2)
            # Capture the image
            self.picam2.capture_file(filepath)
            # Stop and close the camera properly
            self.picam2.stop()
            self.picam2.close()
            
            # Reinitialize for next capture
            self.picam2 = Picamera2()
            config = self.picam2.create_still_configuration()
            self.picam2.configure(config)
            
            return True
        except Exception as e:
            print(f"Error capturing image: {e}")
            return False