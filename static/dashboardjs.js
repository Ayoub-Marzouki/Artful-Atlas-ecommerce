document.addEventListener('DOMContentLoaded', function() {
    // Get all tab elements and content sections
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.content');

    // Hide all content sections
    contents.forEach(content => {
        content.style.display = 'none';
    });

    // Show the default content section (dashboard) and mark its tab as selected
    const defaultTabId = 'dashboard-tab';
    
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

    // Javascript charts for orders

    const ctx = document.getElementById('myChart');
    const ordersLength = document.getElementById('orders-length').innerHTML;
    const current_month = document.getElementById('month').innerHTML;
    let monthly_orders = [0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0, 0];

    switch (parseInt(current_month)) {
        case 1:
            monthly_orders[0] = ordersLength;
            break;
        case 2:
            monthly_orders[1] = ordersLength;
            break;
        case 3:
            monthly_orders[2] = ordersLength;
            break;
        case 4:
            monthly_orders[3] = ordersLength;
            break;
        case 5:
            monthly_orders[4] = ordersLength;
            break;
        case 6:
            monthly_orders[5] = ordersLength;
            break;
        case 7:
            monthly_orders[6] = ordersLength;
            break;
        case 8:
            monthly_orders[7] = ordersLength;
            break;
        case 9:
            monthly_orders[8] = ordersLength;
            break;
        case 10:
            monthly_orders[9] = ordersLength;
            break;
        case 11:
            monthly_orders[10] = ordersLength;
            break;
        case 12:
            monthly_orders[11] = ordersLength;
            break;
        default:
            break;
    }

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            datasets: [{
                label: 'Number of Orders',
                data: monthly_orders, 
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    
});


// Choose an address as a default address
$(document).on("click", ".make-default",function() {
    let id = $(this).attr("data-address-id")
    let this_val = $(this)

    console.log("ID : ", id);
    console.log("Current : ", this_val);

    $.ajax({
        url:"/update-address-status",
        data: {
            "id":id,
        },
        dataType:"json",
        success: function(response) {
            console.log("Changed address status")
            if (response.boolean == true) {
                $(".uncheck").show()
                $(".check").hide()
                $(".btn").show()

                $(".uncheck" + id).hide()
                $(".check" + id).show()
                $(".btn" + id).hide()
            }
        }
    })
})


let maxAddresses = 3; // Maximum number of addresses allowed


// If we have 3 addresses, we won't show the form that allows user to add an address
function updateUI() {
    if ($("address").length >= maxAddresses) {
        $("#add-address-button").prop("disabled", true);
        $("#add-address-form").hide();
    } else {
        $("#add-address-button").prop("disabled", false);
        $("#add-address-form").show()
    }
}

$(document).ready(function() {
    updateUI();
});

$(document).on("click", "#delete", function() {
    let address_id = $(this).attr("data-address-id")
    let this_val = $(this)

    console.log("Address id : ", address_id);
    console.log("this : ", this_val);

    $.ajax({
        url: "/delete-address",
        data: {
            "address_id": address_id,
        },
        dataType: "json",
        success: function(response) {
            this_val.css("display", "none")
            $("#address-" + address_id).remove()
        }
    });
});