const captureBtn = document.getElementById('captureBtn');
const statusDiv = document.getElementById('status');
const capturedImage = document.getElementById('capturedImage');

captureBtn.addEventListener('click', async () => {
    captureBtn.disabled = true;
    captureBtn.textContent = 'Capturing photo...';
    statusDiv.textContent = 'Capturing photo...';
    
    // Hide roast from previous capture
    const roastContainer = document.getElementById('roastContainer');
    const roastText = document.getElementById('roastText');
    roastContainer.style.display = 'none';
    
    try {
        // Step 1: Capture the photo
        const captureResponse = await fetch('/capture');
        const captureData = await captureResponse.json();
        
        if (captureData.success) {
            statusDiv.textContent = 'Photo captured! Analyzing image...';
            const imagePath = `/static/captures/${captureData.filename}`;
            capturedImage.src = imagePath;
            capturedImage.style.display = 'block';
            
            // Step 2: Analyze the image
            const analyzeResponse = await fetch('/analyze');
            const analyzeData = await analyzeResponse.json();
            
            if (analyzeData.success) {
                statusDiv.textContent = 'Analysis complete! Generating roast...';
                
                // Step 3: Generate the roast with analysis data
                const roastResponse = await fetch('/generate-roast', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        analysis: analyzeData.analysis
                    })
                });
                
                const roastData = await roastResponse.json();
                
                if (roastData.success) {
                    statusDiv.textContent = 'Roast complete! 🔥';
                    roastText.textContent = roastData.roast;
                    roastContainer.style.display = 'block';
                } else {
                    statusDiv.textContent = `Roast generation failed: ${roastData.error}`;
                }
            } else {
                statusDiv.textContent = `Analysis failed: ${analyzeData.error}`;
            }
        } else {
            statusDiv.textContent = `Error: ${captureData.error}`;
        }
    } catch (error) {
        statusDiv.textContent = `Error: ${error.message}`;
    } finally {
        captureBtn.disabled = false;
        captureBtn.textContent = 'Capture Photo';
    }
});
