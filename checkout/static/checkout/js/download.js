/**
 * Code for converting an image to a blob so it can be downloaded on same site
 * https://stackoverflow.com/questions/44070437/how-to-get-a-file-or-blob-from-an-url-in-javascript
 */
const downloadItems = document.querySelectorAll('.download-item');
for (const downloadItem of downloadItems ) {
    let url = downloadItem.getAttribute('href');

    fetch(url)
    .then(res => res.blob()) // Gets the response and returns it as a blob
    .then(blob => {
        // Here's where you get access to the blob
        // And you can use it for whatever you want
        // Like calling ref().put(blob)

        // Here, I use it to make an image appear on the page
        let objectURL = URL.createObjectURL(blob);
        downloadItem.setAttribute("href", objectURL); 
    });

}