document.addEventListener('DOMContentLoaded', function() {
    var filterHeader = document.getElementById("filter-header");
    var dropContent = document.getElementById("drop-content");

    filterHeader.addEventListener("click", function() {
    dropContent.classList.toggle("hidden");
    })


    const deleteButtons = document.querySelectorAll('.delete-button');
    const removeUrl = document.getElementById("remove-url").innerHTML;

    // Function to create and display the custom confirmation box
    function showConfirmation(message) {
      const confirmationBox = document.createElement('div');
      confirmationBox.classList.add('confirmation-box');
      confirmationBox.innerHTML = `
        <div class="confirmation-message">${message}</div>
        <div class="confirmation-buttons">
          <button class="confirm-button">Yes</button>
          <button class="cancel-button">Cancel</button>
        </div>
      `;
      document.body.appendChild(confirmationBox);

      // Handle button clicks inside the confirmation box
      confirmationBox.addEventListener('click', (event) => {
        if (event.target.classList.contains('confirm-button')) {
          window.location.href = removeUrl;
          confirmationBox.remove(); // Remove confirmation box after confirmation
        } else if (event.target.classList.contains('cancel-button')) {
          confirmationBox.remove();
        }
      });
    }

    // Attach click event listener to each delete button
    deleteButtons.forEach(button => {
      button.addEventListener('click', function(event) {
        event.preventDefault();
        const message = 'Are you sure you want to delete this artwork?';
        showConfirmation(message); // Call custom confirmation function
      });
});
})