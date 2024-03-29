// Scroll to slider
function scrollToSlider(buttonId, sliderId) {
    const scrollButton = document.getElementById(buttonId);
    const slider = document.getElementById(sliderId);

    scrollButton.addEventListener('click', () => {
        const offset = slider.offsetTop;

        window.scrollTo({
            top: offset,
            behavior: 'smooth'
        });
    });
}

// Function to create sliders
function createSlider(sliderId, intervalTime) {
    const slider = document.getElementById(sliderId);
    const sliderImages = slider.querySelector('.slider-images');
    const sliderArrows = slider.querySelector('.slider-arrows');
    const leftArrow = sliderArrows.querySelector('.left-arrow');
    const rightArrow = sliderArrows.querySelector('.right-arrow');

    let slideIndex = 0;
    let intervalID;
    let isPaused = false;

    function showSlide() {
        const slideWidth = slider.clientWidth;
        sliderImages.style.transform = `translateX(-${slideIndex * slideWidth}px)`;
    }

    function nextSlide() {
        const numSlides = sliderImages.children.length;
        slideIndex = (slideIndex + 1) % numSlides;
        showSlide();
    }

    function previousSlide() {
        const numSlides = sliderImages.children.length;
        slideIndex = (slideIndex - 1 + numSlides) % numSlides;
        showSlide();
    }

    function startAutoSlide() {
        intervalID = setInterval(() => {
            if (!isPaused) {
                nextSlide();
            }
        }, intervalTime);
    }

    function pauseAutoSlide() {
        isPaused = true;
    }

    function resumeAutoSlide() {
        isPaused = false;
    }

    // Attach event listeners for navigation
    leftArrow.addEventListener('click', () => {
        pauseAutoSlide();
        previousSlide();
        slider.focus();
    });

    rightArrow.addEventListener('click', () => {
        pauseAutoSlide();
        nextSlide();
        slider.focus();
    });

    // Function to start the slider when it becomes visible
    function startSliderWhenVisible(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                startAutoSlide();
                observer.unobserve(entry.target);
            }
        });
    }

    // Create an Intersection Observer to trigger the slider when it becomes visible
    const observer = new IntersectionObserver(startSliderWhenVisible, {
        root: null,
        rootMargin: "0px",
        threshold: 0.5, // Adjust the threshold as needed
    });

    observer.observe(slider);

    // Pause the slider when hovering
    slider.addEventListener('mouseover', pauseAutoSlide);
    slider.addEventListener('mouseout', resumeAutoSlide);
}

// Call the function to create the sliders
scrollToSlider('down0', 'moroccan-slider');
scrollToSlider('down1', 'home-main');

createSlider('slider1', 5000);
createSlider('slider2', 2500);



// Start slider on scroll
const slider0Images = document.querySelectorAll('.slider0-image');
let currentIndex0 = 0;
let intervalId0 = null;

function changeImage() {
    slider0Images[currentIndex0].style.opacity = 0;
    currentIndex0 = (currentIndex0 + 1) % slider0Images.length;
    slider0Images[currentIndex0].style.opacity = 1;
}

function startSlider0() {
    if (!intervalId0) {
        intervalId0 = setInterval(changeImage, 3000);
    }
}

function stopSlider0() {
    clearInterval(intervalId0);
    intervalId0 = null;
}

window.addEventListener('scroll', () => {
    const slider0Container = document.getElementById('moroccan-slider');
    const slider0Rect = slider0Container.getBoundingClientRect();

    // Calculate the midpoint of the slider
    const sliderMidpoint = slider0Rect.top + slider0Rect.height / 2;

    // Calculate the scroll position to consider the half-visibility
    const halfViewportHeight = window.innerHeight / 2;
    const scrollPosition = window.scrollY + halfViewportHeight;

    // Check if the midpoint of the slider is within the visible portion of the viewport
    if (sliderMidpoint <= scrollPosition && slider0Rect.bottom >= 0) {
        startSlider0();
    } else {
        stopSlider0();
    }
});


// Fade slide functionality
const sliderObjects = document.querySelectorAll('.slider-object');

function fadeSlide(nextIndex) {
    sliderObjects[currentIndex].classList.remove('active');
    sliderObjects[nextIndex].classList.add('active');
    currentIndex = nextIndex;
}

sliderObjects.forEach((slide, index) => {
    slide.style.transitionDelay = `${(index + 1) * 0.1}s`; // Adjust the delay as needed
});

let currentIndex = 0;

setInterval(() => {
    const nextIndex = (currentIndex + 1) % sliderObjects.length;
    fadeSlide(nextIndex);
}, 4000); // interval time to adjust the slide duration
