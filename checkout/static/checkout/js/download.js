// Now we need it to work for all items
const downloadItems = document.querySelectorAll('.download-item');
for (let downloadItem of downloadItems ) {
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