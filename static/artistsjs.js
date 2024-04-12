document.addEventListener("DOMContentLoaded", function() {
    var filterHeader = document.getElementById("filter-header");
    var dropContent = document.getElementById("drop-content");
    var searchIcon = document.getElementById("search");

    filterHeader.addEventListener("click", function() {
        dropContent.classList.toggle("hidden");
        if (!dropContent.classList.contains("hidden")) {
            dropContent.style.maxHeight = dropContent.scrollHeight + "px";
            searchIcon.style.opacity=1;
        } else {
            dropContent.style.maxHeight = 0;
            searchIcon.style.opacity=0;
        }
    });

    // Function to resize images while maintaining aspect ratio
    function resizeImages(images, maxWidth, maxHeight) {
        images.forEach(function(image) {
            // Create a new Image object to get the original dimensions
            var img = new Image();
            img.onload = function() {
                var aspectRatio = img.width / img.height;
                var newWidth = img.width;
                var newHeight = img.height;

                // Check if width exceeds the maximum width
                if (newWidth > maxWidth) {
                    newWidth = maxWidth;
                    newHeight = newWidth / aspectRatio;
                }

                // Check if height exceeds the maximum height
                if (newHeight > maxHeight) {
                    newHeight = maxHeight;
                    newWidth = newHeight * aspectRatio;
                }

                // Apply the new dimensions to the image
                image.width = newWidth;
                image.height = newHeight;
            };
            // Set the src attribute to trigger the onload event
            img.src = image.src;
    });
    }
    var portraitImages = document.querySelectorAll(".portrait");
    var landscapeImages = document.querySelectorAll(".landscape");

    resizeImages(portraitImages, 400, 400);
    resizeImages(landscapeImages, 500, 300);
});

document.addEventListener("DOMContentLoaded", function() {
    const filterItems = document.querySelectorAll('.filter-item');

    filterItems.forEach(item => {
        item.addEventListener('click', function() {
            const checkbox = this.nextElementSibling; // Get the associated checkbox

            checkbox.checked = !checkbox.checked; // Toggle the checkbox

            if (checkbox.checked) {
                this.style.backgroundColor = 'skyblue'; // Set background color when checked
            } else {
                this.style.backgroundColor = 'initial'; // Reset background color when unchecked
            }
        });
    });
});

