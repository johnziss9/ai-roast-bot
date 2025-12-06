const captureBtn = document.getElementById('captureBtn');
const statusDiv = document.getElementById('status');
const capturedImage = document.getElementById('capturedImage');
const spinner = document.getElementById('spinner');
const countdownDiv = document.getElementById('countdown');

// Countdown function
function startCountdown(seconds) {
    return new Promise((resolve) => {
        countdownDiv.classList.add('active');
        countdownDiv.textContent = seconds;
        
        const countdownInterval = setInterval(() => {
            seconds--;
            if (seconds > 0) {
                countdownDiv.textContent = seconds;
            } else if (seconds === 0) {
                countdownDiv.textContent = 'Smile! 😄';
            } else {
                clearInterval(countdownInterval);
                countdownDiv.classList.remove('active');
                resolve();
            }
        }, 1000);
    });
}

captureBtn.addEventListener('click', async () => {
    captureBtn.disabled = true;
    captureBtn.textContent = 'Get ready...';
    statusDiv.textContent = 'Get ready to pose!';

    // Start countdown before capture
    await startCountdown(3);
    
    // Now update for actual capture
    captureBtn.textContent = 'Capturing photo...';
    statusDiv.textContent = 'Capturing photo...';
    spinner.classList.add('active'); // Show spinner
    
    // Hide roast from previous capture
    const roastContainer = document.getElementById('roastContainer');
    const roastText = document.getElementById('roastText');
    roastContainer.classList.remove('show');
    capturedImage.classList.remove('show', 'shrink');
    
    try {
        // Step 1: Capture the photo
        const captureResponse = await fetch('/capture');
        const captureData = await captureResponse.json();
        
        if (captureData.success) {
            statusDiv.textContent = 'Photo captured! Analyzing image...';
            const imagePath = `/static/captures/${captureData.filename}`;
            capturedImage.src = imagePath;
            capturedImage.classList.add('show');
            
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
                    capturedImage.classList.add('shrink');
                    roastContainer.classList.add('show');
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
        spinner.classList.remove('active'); // Hide spinner
    }
});
