from picamera2 import Picamera2
import time
import os

class Camera:
    def __init__(self):
        """Initialize the camera"""
        pass  # Don't initialize picam2 here
        
    def capture_image(self, filepath):
        """Capture an image and save it to filepath"""
        picam2 = None
        try:
            # Create and configure camera fresh each time
            picam2 = Picamera2()
            config = picam2.create_still_configuration()
            picam2.configure(config)
            
            # Start the camera
            picam2.start()
            # Give it a moment to adjust exposure
            time.sleep(2)
            # Capture the image
            picam2.capture_file(filepath)
            
            return True
        except Exception as e:
            print(f"Error capturing image: {e}")
            return False
        finally:
            # Always clean up camera resources
            if picam2 is not None:
                try:
                    picam2.stop()
                    picam2.close()
                except:
                    pass  # Ignore errors during cleanup