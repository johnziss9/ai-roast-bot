from modules.analyzer import ImageAnalyzer
import os

print("Testing Image Analyzer...")
print("-" * 50)

analyzer = ImageAnalyzer()

# Find the most recent capture
captures_dir = 'static/captures'
captures = [f for f in os.listdir(captures_dir) if f.endswith('.jpg')]

if captures:
    # Sort by filename (which includes timestamp) and get the latest
    latest_capture = sorted(captures)[-1]
    image_path = os.path.join(captures_dir, latest_capture)
    
    print(f"Analyzing: {latest_capture}")
    
    analysis = analyzer.analyze_image(image_path)
    
    print("\nAnalysis Results:")
    print(f"  Faces detected: {analysis['faces_detected']}")
    print(f"  Has face: {analysis['has_face']}")
    
    if 'age_range' in analysis:
        print(f"  Age range: {analysis['age_range']}")
    else:
        print("  Age range: Not detected")
    
    if 'gender' in analysis:
        print(f"  Gender: {analysis['gender']}")
    else:
        print("  Gender: Not detected")
    
    if 'eyes_detected' in analysis:
        print(f"  Eyes detected: {analysis['eyes_detected']}")
    else:
        print("  Eyes detected: Not detected")

    # Print full analysis for debugging
    print(f"\nFull analysis data: {analysis}")
else:
    print("No captures found. Take a photo first!")

print("-" * 50)
