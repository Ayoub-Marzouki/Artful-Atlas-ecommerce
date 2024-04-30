$(document).on("click", ".add-to-wishlist", function() {
    let product_id = $(this).attr("data-product-item");
    let this_val = $(this);

    $.ajax({
        url: "/add-to-wishlist/",
        data: {
            "id": product_id,
        },
        dataType: "json",
        beforeSend: function() {
            console.log("Adding to Wishlist...");
        },
        success: function(response) {
            if (response.success) {
                $("#wishlist-counter").text(response.wishlist_count);
                console.log("added to wishlist.")
                if (this_val.is("div")) {
                    this_val.find("span").text("Added to Wishlist.");
                    this_val.find("img.icons").attr("src", "/static/images/icons/full-heart.png");
                } else {
                    this_val.html("Added to Wishlist.");
                }
            } else {
                console.log("Failed to add to Wishlist.");
            }
        }
    });
});


$(document).on("click", ".delete", function() {
    let product_id = $(this).closest("#wishlist-artworks").find(".product-id").val();
    let this_val = $(this);

    $.ajax({
        url: "/delete-from-wishlist/",
        data: {
            "id": product_id,
        },
        dataType: "json",
        beforeSend: function() {
            this_val.css("opacity", "0");
        },
        success: function(response) {
            if (response.success) {
                this_val.css("opacity", "1")
                this_val.closest("#wishlist-artworks").remove();
                $("#wishlist-counter").text(response.wishlist_count);
                if (response.wishlist_count === 0) {
                    $("#else-h2").show();
                } else {
                    $("#else-h2").hide();
                }
            } else {
                this_val.css("opacity", "1")
                console.error("Failed to delete item from wishlist:", response.message);
            }
        }
    });
});

