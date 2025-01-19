document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        // Ensure the response is handled correctly
        if (!response.ok) {
            const errorText = await response.text();
            document.getElementById('outputText').value = `Error: ${errorText}`;
        } else {
            const resultText = await response.text(); // Get text from the response
            document.getElementById('outputText').value = resultText;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('outputText').value = `Error: ${error.message}`;
    }
});
