document.addEventListener('DOMContentLoaded', function() {
    // Find all paragraphs containing the text "Change"
    const paragraphs = document.querySelectorAll('p');

    // Loop through each paragraph to find the one containing "Change"
    paragraphs.forEach(paragraph => {
        // Check if the paragraph contains the text "Change"
        if (paragraph.textContent.includes('Change')) {
            // Split the paragraph content into parts before and after "Change"
            const parts = paragraph.innerHTML.split('Change');
            
            // Reconstruct the paragraph content with "Change" wrapped in a span
            paragraph.innerHTML = parts[0] + '<span style="margin-left: 170px; font-weight:bold;">Change</span>' + parts[1];
        }
    });

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

});
