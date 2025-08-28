function downloadVideo() {
    const videoUrl = document.getElementById('videoUrl').value.trim();
    const statusDiv = document.getElementById('status');
    const resultDiv = document.getElementById('result');

    if (!videoUrl) {
        statusDiv.innerHTML = '<p class="error">Please enter a video URL</p>';
        return;
    }

    statusDiv.innerHTML = '<p><span class="loading"></span>Downloading video... Please wait</p>';
    resultDiv.innerHTML = '';

    const formData = new FormData();
    formData.append('url', videoUrl);

    fetch('/download', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            statusDiv.innerHTML = '<p>Download completed successfully!</p>';
            resultDiv.innerHTML = `
                <p>Title: ${data.title}</p>
                <a href="/get-video/${encodeURIComponent(data.download_path.split('/').pop())}" target="_blank">
                    Download Video
                </a>
            `;
        } else {
            statusDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
            resultDiv.innerHTML = '';
        }
    })
    .catch(error => {
        statusDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
        resultDiv.innerHTML = '';
    });
}
