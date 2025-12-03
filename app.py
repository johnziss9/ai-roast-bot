from flask import Flask, render_template
from modules.camera import Camera
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/capture')
def capture():
    """Capture a photo and return the filename"""
    try:
        # Create camera instance
        camera = Camera()
        
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'capture_{timestamp}.jpg'
        filepath = os.path.join('static', 'captures', filename)
        
        # Capture the image
        if camera.capture_image(filepath):
            return {'success': True, 'filename': filename}
        else:
            return {'success': False, 'error': 'Failed to capture image'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
