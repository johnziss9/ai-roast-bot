from flask import Flask, render_template, jsonify, request
from modules.camera import Camera
from modules.generator import RoastGenerator
from modules.analyzer import ImageAnalyzer
import os
from datetime import datetime

app = Flask(__name__)
generator = RoastGenerator()
analyzer = ImageAnalyzer()

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

@app.route('/generate-roast', methods=['POST'])
def generate_roast():
    try:
        # Get analysis data from request
        data = request.get_json()
        analysis_data = data.get('analysis', {})
        
        roast = generator.generate_roast(analysis_data)
        return jsonify({
            'success': True,
            'roast': roast
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/analyze')
def analyze():
    try:
        # Get the most recent capture
        captures_dir = 'static/captures'
        captures = [f for f in os.listdir(captures_dir) if f.endswith('.jpg')]
        
        if not captures:
            return jsonify({
                'success': False,
                'error': 'No image to analyze'
            }), 404
        
        # Get latest capture
        latest_capture = sorted(captures)[-1]
        image_path = os.path.join(captures_dir, latest_capture)
        
        # Analyze it
        analysis = analyzer.analyze_image(image_path)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
