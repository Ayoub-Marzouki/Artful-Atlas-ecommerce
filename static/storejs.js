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
