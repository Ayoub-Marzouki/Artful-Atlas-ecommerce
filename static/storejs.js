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
