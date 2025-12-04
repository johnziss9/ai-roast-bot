document.addEventListener('DOMContentLoaded', () => {
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
                statusDiv.textContent = 'Photo captured! Generating roast...';
                const imagePath = `/static/captures/${captureData.filename}`;
                capturedImage.src = imagePath;
                capturedImage.style.display = 'block';
                
                // Step 2: Generate the roast
                const roastResponse = await fetch('/generate-roast');
                const roastData = await roastResponse.json();
                
                if (roastData.success) {
                    statusDiv.textContent = 'Roast complete! 🔥';
                    roastText.textContent = roastData.roast;
                    roastContainer.style.display = 'block';
                } else {
                    statusDiv.textContent = `Roast generation failed: ${roastData.error}`;
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
});
