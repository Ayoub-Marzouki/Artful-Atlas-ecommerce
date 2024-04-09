// Get the elements for Art Enthusiast and Artist
const enthusiastOption = document.getElementById('customer');
const artistOption = document.getElementById('artist');
const background1 = document.getElementById('background1');
const background2 = document.getElementById('background2');

// Add event listeners to the options
enthusiastOption.addEventListener('click', function() {
    background1.classList.add('bright');
    background2.classList.remove('bright');
});

artistOption.addEventListener('click', function() {
    background1.classList.remove('bright');
    background2.classList.add('bright');
});
