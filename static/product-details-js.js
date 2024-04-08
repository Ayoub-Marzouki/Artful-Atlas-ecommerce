function createLightbox(imageUrl) {
    // Create a lightbox overlay
    const lightbox = document.createElement('div');
    lightbox.classList.add('lightbox');
    
    // Create an image element for the background image
    const image = document.createElement('img');
    image.src = imageUrl;
    
    // Append the image to the lightbox
    lightbox.appendChild(image);
    
    // Append the lightbox to the document body
    document.body.appendChild(lightbox);
    
    // Close the lightbox when clicking outside of it
    lightbox.addEventListener('click', function() {
        document.body.removeChild(lightbox);
    });
}

const artworkImage = document.getElementById('artwork-image');
artworkImage.addEventListener('click', function(event) {
    // Prevent the click event from bubbling up to the profile artwork
    event.stopPropagation();

    const imageUrl = this.src;
    createLightbox(imageUrl);
});

const secondaryImages = document.getElementsByClassName('secondary-images');
for (const image of secondaryImages) {
    image.addEventListener('click', function(event) {
        // Prevent the click event from bubbling up to the profile artwork
        event.stopPropagation();
        const imageUrl = this.src;
        updateMainImage(imageUrl);

    });
}

// Function to update the main image with the clicked secondary image
function updateMainImage(imageUrl) {
    if (artworkImage.src === imageUrl) {
        return; // Exit the function early if it's the same image
    }
    // Smoothly fade out the image
    artworkImage.style.transition = 'opacity 1s';
    artworkImage.style.opacity = '0';
    
    // Wait for the fade-out effect to complete
    setTimeout(function() {
        // Change the image source
        artworkImage.src = imageUrl;
        
        // Smoothly fade in the new image
        artworkImage.style.opacity = '1';
    }, 1000); // Adjust the delay as needed
}



