document.getElementById('pdf-upload-form').addEventListener('submit', function(event) {
  event.preventDefault();

  const fileInput = document.getElementById('pdf-file');
  const formData = new FormData();
  formData.append('pdf', fileInput.files[0]);

  fetch('https://api.cloud.llamaindex.ai/api/v1/parsing/upload', {
    method: 'POST',
    headers: {
      'Authorization': 'bearer llx-4NtZLmrLPlJX6ZQZBN4T1Y9B8Bu2YlQPy8UjaxEJN7PzXYOo',  // Replace with your API token
    },
    body: formData,
  })
  .then(response => response.json())
  .then(data => {
    console.log(data); // Handle the JSON result here
  })
  .catch(error => console.error('Error:', error));
});
