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

// Get the profile-artwork element and attach event listener
const profileArtwork = document.getElementById('profile-artwork');
profileArtwork.addEventListener('click', function() {
    const imageUrl = this.getAttribute('data-image-url');
    createLightbox(imageUrl);
});

// Get the profile-picture element and attach event listener
const profilePicture = document.querySelector('.profile-picture');
profilePicture.addEventListener('click', function(event) {
    // Prevent the click event from bubbling up to the profile artwork
    event.stopPropagation();

    const imageUrl = this.src;
    createLightbox(imageUrl);
});

// Select the anchor tag with href="#comments"
const commentLink = document.querySelector('a[href="#comments"]');

// Add a click event listener to the anchor tag
commentLink.addEventListener('click', function(event) {
    // Prevent the default behavior of the anchor tag (instant jump)
    event.preventDefault();

    // Get the target element (h1 with id="comments")
    const commentsSection = document.getElementById('comments');

    // Scroll to the comments section with smooth animation
    commentsSection.scrollIntoView({ behavior: 'smooth' });
});



