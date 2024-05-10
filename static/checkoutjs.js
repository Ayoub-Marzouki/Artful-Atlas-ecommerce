// window.onload = function() {
//     console.log("Window loaded");
//     const iframe = document.getElementsByTagName("iframe")[0]; // Accessing the first iframe
//     iframe.onload = function() {
//         console.log("Iframe loaded");
//         // Retrieve the credit / debit card input fields
//         const firstNameField = document.getElementById("billingAddress.givenName");
//         const lastNameField = document.getElementById("billingAddress.familyName");
//         const addressField = document.getElementById("billingAddress.line1");
//         const emailField = document.getElementById("email");
//         const phoneField = document.getElementById("phone");

//         // Retrieve the user's registered info
//         const firstName = document.getElementById("first-name");
//         const lastName = document.getElementById("last-name");
//         const address = document.getElementById("address");
//         const email = document.getElementById("user-email");
//         const phone = document.getElementById("user-phone");

//         // Assign user information to the credit/debit card fields
//         firstNameField.value = firstName.textContent;
//         lastNameField.value = lastName.textContent;
//         addressField.value = address.textContent;
//         emailField.value = email.textContent;
//         phoneField.value = phone.textContent;

//         // Log retrieved information (for debugging)
//         console.log("Retrieved user information:");
//         console.log("First Name:", firstName.textContent);
//         console.log("Last Name:", lastName.textContent);
//         console.log("Address:", address.textContent);
//         console.log("Email:", email.textContent);
//         console.log("Phone:", phone.textContent);
//     }
// }

// onApprove: function(data, actions) {
//     return actions.order.capture().then(function(details) {
//         window.location.href= "/payment/payment-completed/{{order.oid}}";
//     });
// },
// enableStandardCardFields: true,