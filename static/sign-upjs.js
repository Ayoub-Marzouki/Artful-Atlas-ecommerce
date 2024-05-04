// Select the first child of the div with the id "id_user_type" and give it the id "customer"
const customerRadio = document.querySelector('#id_user_type > div:first-child');
customerRadio.id = 'customer';
const customerRadioButton = customerRadio.querySelector('input[type="radio"]');
customerRadioButton.checked = false;

// Select the second child of the div with the id "id_user_type" and give it the id "artist"
const artistRadio = document.querySelector('#id_user_type > div:last-child');
artistRadio.id = 'artist';
const artistRadioButton = artistRadio.querySelector('input[type="radio"]');
artistRadioButton.checked = false; // Optionally, set it to false if you want only one option to be pre-selected

// Get the elements for Art Enthusiast and Artist
const enthusiastOption = document.getElementById('customer');
const artistOption = document.getElementById('artist');
const background1 = document.getElementById('background1');
const background2 = document.getElementById('background2');

// Add event listeners to the options
enthusiastOption.addEventListener('click', function() {
    background1.classList.add('bright');
    background2.classList.remove('bright');
    customerRadioButton.checked = true; // Ensure the radio button is checked
    artistRadioButton.checked = false; // Uncheck the other radio button
});

artistOption.addEventListener('click', function() {
    background1.classList.remove('bright');
    background2.classList.add('bright');
    artistRadioButton.checked = true; // Ensure the radio button is checked
    customerRadioButton.checked = false; // Uncheck the other radio button
});
