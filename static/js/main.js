// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {
    const captureBtn = document.getElementById('captureBtn');
    const statusDiv = document.getElementById('status');
    
    captureBtn.addEventListener('click', function() {
        // Disable button and show status
        captureBtn.disabled = true;
        statusDiv.textContent = 'Capturing photo...';
        
        // Send request to capture endpoint
        fetch('/capture')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    statusDiv.textContent = 'Photo captured!';
                    
		    // Display the image
                    const img = document.getElementById('capturedImage');
                    const container = document.getElementById('imageContainer');
                    img.src = '/static/captures/' + data.filename;
                    container.style.display = 'block';
                } else {
                    statusDiv.textContent = 'Error: ' + data.error;
                }
                // Re-enable button
                captureBtn.disabled = false;
            })
            .catch(error => {
                statusDiv.textContent = 'Error capturing photo';
                console.error('Error:', error);
                captureBtn.disabled = false;
            });
    });
});
