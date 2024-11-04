document.addEventListener('DOMContentLoaded', function () {
    let images = [];
    let currentIndex = 0;
    function compare(list1, list2) {
        return list1.length === list2.length && list1.every((value, index) => value === list2[index]);
    }
    // Function to fetch image paths from the server
    async function fetchImagePaths() {
        try {
            const response = await fetch("http://127.0.0.1:5000/get_image_paths");
            cur_images = await response.json();
            if (compare(cur_images, images) === false) {
                images = cur_images;
                currentIndex = 0;
                if (images.length > 0) {
                    displayImage(currentIndex);
                } else {
                    console.error("No images available");
                }
            }
            
            
        } catch (error) {
            console.error("Error fetching image paths:", error);
        }
    }

    // Function to display an image based on the current index
    function displayImage(index) {
        const imageElement = document.getElementById('image-display');
        if (index >= 0 && index < images.length) {
            imageElement.src = images[index];
        } else {
            index = 0;
        }
    }

    // Event listener for the "Next" button
    document.getElementById('next-button').addEventListener('click', function () {
        if (currentIndex < images.length - 1) {
            currentIndex++;
            displayImage(currentIndex);
        }
        console.log("next")
    });

    // Event listener for the "Previous" button
    document.getElementById('prev-button').addEventListener('click', function () {
        if (currentIndex > 0) {
            currentIndex--;
            displayImage(currentIndex);
        }
        console.log('prev')
    });

    // Fetch image paths when the page loads
    // fetchImagePaths();
    setInterval(fetchImagePaths, 1000);
});
