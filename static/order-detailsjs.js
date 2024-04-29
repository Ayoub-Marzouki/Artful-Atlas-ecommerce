document.addEventListener('DOMContentLoaded', function() {
    // Get all tab elements and content sections
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.content');

    // Hide all content sections
    contents.forEach(content => {
        content.style.display = 'none';
    });

    // Show the default content section (dashboard) and mark its tab as selected
    const defaultTabId = 'orders-tab';
    
    // Add 'selected' class and background color to the default tab
    const defaultTab = document.querySelector(`#${defaultTabId}`);
    if (defaultTab) {
        defaultTab.classList.add('selected');
        defaultTab.style.backgroundColor = 'lightblue'; // Set background color for default tab
    }

    // Add click event listener to each tab
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Hide all content sections
            contents.forEach(content => {
                content.style.display = 'none';
            });

            // Remove 'selected' class and background color from all tabs
            tabs.forEach(tab => {
                tab.classList.remove('selected');
                tab.style.backgroundColor = '';
            });

            // Mark the clicked tab as selected and set its background color
            this.classList.add('selected');
            this.style.backgroundColor = 'lightblue';

            // Show the corresponding content section
            const targetId = this.id.replace('-tab', '');
            const targetContent = document.querySelector(`#${targetId}`);
            if (targetContent) {
                targetContent.style.display = 'block';
            }
        });
    });

    // Trigger click event on the default tab to display its content
    if (defaultTab) {
        defaultTab.click();
    }
});
