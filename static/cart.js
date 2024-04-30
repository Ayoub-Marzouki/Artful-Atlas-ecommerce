
const addToCartButtons = document.querySelectorAll(".cart-button");
const messageContainer = document.getElementById("message-container");


// Display the message and update the counter
function showMessage() {
  messageContainer.style.opacity = 1;
  setTimeout(function () {
    messageContainer.style.opacity = 0;
  }, 2000);
}

// Add click event listener to each "Add to Cart" button
addToCartButtons.forEach(button => {
  button.addEventListener("click", showMessage);
});


//  Ajax for adding products to cart / wishlist

$(".cart-button").on("click", function() {
    // Retrieve product details from the DOM relative to the clicked button
    let product_title = $(this).siblings(".product-title").val();
    let product_id = $(this).siblings(".product-id").val();
    let product_price;
    let product_image;
    let artist_name;
    let artist_page;
    let product_page;
   // Check if the button is within the main product or related products
    if ($(this).closest("#info").length > 0) {
        // For the main product
        product_price = $(this).closest("#info").find("#price-section .price").text();
        product_image = $(this).closest("#artwork-overview").find("#artwork-image").attr("src");
        artist_name = $(this).closest("#info").find("#artist-name").text().trim();
        artist_page = $(this).closest("#info").find("#artist-name").attr("href");
        product_page = $(this).closest("#info").find("a[data-product-url]").attr("href");
    } else if ($(this).closest("#wishlist-artworks").length > 0) {
        // For wishlist template
        product_id = $(this).closest("#wishlist-artworks").find(".product-id").val();
        product_price = $(this).closest("#wishlist-artworks").find(".price").text();
        product_image = $(this).closest("#wishlist-artworks").find(".artwork-image").attr("src");
        artist_name = $(this).closest("#wishlist-artworks").find(".artwork-artist").text().trim();
        artist_page = $(this).closest("#wishlist-artworks").find(".artwork-artist").attr("href");
        product_page = $(this).closest("#wishlist-artworks").find("a[data-product-url]").attr("href");
    } else {
        // For related products
        product_price = $(this).closest("figure").find(".price").text();
        product_image = $(this).closest("figure").find("img.store-images").attr("src");
        artist_name = $(this).closest("figure").find("#artist-name").text().trim();
        artist_page = $(this).closest("figure").find("#artist-name").attr("href");
        product_page = $(this).closest("figure").find("a[data-product-url]").attr("href");
    }
    

    let this_val = $(this);

    // Log product details to the console
    console.log("title", product_title);
    console.log("id", product_id);
    console.log("price", product_price);
    console.log("image", product_image);
    console.log("current element", this_val);
    console.log("artist : ", artist_name);
    console.log("product page", product_page);
    console.log("artist page", artist_page);

    // Send an AJAX request to add the product to the cart
    $.ajax({
        url: '/add-to-cart',
        data: {
            'id': product_id,
            'title': product_title,
            'price': product_price,
            'image':product_image,
            'artist':artist_name,
            'page': product_page,
            'artistpage': artist_page,
        },
        dataType: 'json',
        // Log a message indicating that the artwork is being added to the cart
        beforeSend: function() {
            console.log("Adding artwork to cart...");
        },
        // If the request is successful, update the button text and log a success message
        success: function(response) {
            this_val.html("Artwork Added to cart");
            console.log("Artwork added to cart!");
            $("#cart-counter").text(response.totalCartItems)
        }
    });
});


$(document).on("click", ".remove", function() {
    let product_id = $(this).attr("data-product");
    let this_val = $(this);

    console.log("Product id : ", product_id);
    console.log("this : ", this_val);

    $.ajax({
        url: "/delete-from-cart",
        data: {
            "id": product_id,
        },
        dataType: "json",
        beforeSend: function() {
            this_val.css("opacity", "0");
        },
        success: function(response) {
            this_val.css("opacity", "1")
            $("#cart-counter").text(response.totalCartItems)
            $("#updated-cart").html(response.data)
        }
    });
});
