const socket = io();

socket.on('progress', function(progress) {
    let percent = (progress.downloaded_bytes / progress.total_bytes) * 100;
    document.getElementById('progress-bar').style.width = percent + '%';
});

function startDownload() {
    let formData = new FormData(document.getElementById('download-form'));
    fetch('/download', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
    .then(data => {
        console.log(data.status);
    });
}
