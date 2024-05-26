// Scroll to section
function scrollToSection(buttonId, sectionId) {
    const scrollButton = document.getElementById(buttonId);
    const section = document.getElementById(sectionId);
    if (scrollButton && section) {
        scrollButton.addEventListener('click', () => {
            const offset = section.offsetTop;

            window.scrollTo({
                top: offset,
                behavior: 'smooth'
            });
        });
}
}

// Function to create sliders
function createSlider(sliderId, intervalTime) {
    const slider = document.getElementById(sliderId);
    const sliderImages = slider.querySelector('.slider-images');

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

    function startAutoSlide() {
        intervalID = setInterval(() => {
            if (!isPaused) {
                nextSlide();
            }
        }, intervalTime);
    }

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
        threshold: 0.5,
    });
    observer.observe(slider);

}

scrollToSection('down00','selection');
scrollToSection('down0', 'nav');


createSlider('slider1', 5000);
createSlider('slider2', 5000);


var elements = document.querySelectorAll('.animate-trigger');

elements.forEach(function(element) {
    element.style.animationPlayState = "paused";
});


// Group elements based on their heights
var lowHeightElements = [];
var midHeightElements = [];
var highHeightElements = [];

elements.forEach(function(element) {
    var height = element.getBoundingClientRect().height;
    if (height < 100) {
        lowHeightElements.push(element);
    } else if (height >= 100 && height < 500) {
        midHeightElements.push(element);
    } else {
        highHeightElements.push(element);
    }
});

// Define different threshold values for each group
const lowHeightThreshold = 0.1;
const midHeightThreshold = 0.3;
const highHeightThreshold = 0.4;

// Create Intersection Observer instances for each group with their corresponding threshold values
function createObserver(elements, threshold) {
    const observer = new IntersectionObserver(startAnimationWhenVisible, {
        root: null,
        rootMargin: "0px",
        threshold: threshold,
    });
    elements.forEach(function(element) {
        observer.observe(element);
    });
}

// Create observers for each group
createObserver(lowHeightElements, highHeightThreshold);
createObserver(midHeightElements, midHeightThreshold);
createObserver(highHeightElements, lowHeightThreshold);

// Define the callback function for each observer
function startAnimationWhenVisible(entries, observer) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            var targetElement = entry.target;
            targetElement.style.animationPlayState = "running";
            observer.unobserve(targetElement);
        }
    });
}

