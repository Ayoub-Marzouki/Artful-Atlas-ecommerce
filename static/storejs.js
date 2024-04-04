const addToCartButtons = document.querySelectorAll(".cart-button");
const messageContainer = document.getElementById("message-container");
const cartCounter = document.getElementById("cart-counter");
let clickCounter = parseInt(localStorage.getItem("clickCounter")) || 0; // Retrieve value from localStorage

// Update the cart counter
function updateCartCounter() {
  cartCounter.innerHTML = clickCounter;
}

// Display the message and update the counter
function showMessage() {
  messageContainer.style.opacity = 1;
  setTimeout(function () {
    messageContainer.style.opacity = 0;
  }, 2000);
  clickCounter++;
  localStorage.setItem("clickCounter", clickCounter); // Update value in localStorage
  updateCartCounter();
}

// Add click event listener to each "Add to Cart" button
addToCartButtons.forEach(button => {
  button.addEventListener("click", showMessage);
});

// Initialize the cart counter on page load
updateCartCounter();
