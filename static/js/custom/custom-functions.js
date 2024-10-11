// Add to cart functionality

$("#add-to-cart-btn").on("click", function(){
    let quantity = $("#item-quantity").val();
    let product_id = $("#product-id").val();
    let product_price = $("#product-price").text();
    let title = $("#product-name").val();
    let slug = $("#product-slug").val();
    let img = document.getElementById("product-image").src;
    let this_val = $(this);

    $.ajax({
        url: '/add-to-cart',
        data: {
            'id': product_id,
            "title": title,
            "qty": quantity,
            "price": product_price,
            "img": img,
            "slug": slug
        },
        dataType: 'json',
        beforeSend: function() {
            console.log("Adding to cart...");
        },
        success: function(response){
            this_val.html("Added to cart!");
            console.log(response.total_cart_items)
            console.log("Added product to cart successfully!");
            $(".count").text(response.total_cart_items)
        }
    })
})

// price updating while changing quantity at cart page

document.addEventListener('DOMContentLoaded', function() {
    const plusButtons = document.querySelectorAll('.js-btn-plus');
    const minusButtons = document.querySelectorAll('.js-btn-minus');
    const subtotalElement = document.getElementById('subtotal');
    const totalElement = document.getElementById('total');

    function updateCart() {
        let subtotal = 0;
        let total = 0;

        document.querySelectorAll('tr[data-item-id]').forEach(tr => {
            const price = parseFloat(tr.querySelector('.product-price').textContent.replace('₹', ''));
            const quantityInput = tr.querySelector('.quantity');
            const quantity = parseInt(quantityInput.value);
            const itemTotal = price * quantity;

            tr.querySelector('.product-total').textContent = `₹${itemTotal.toFixed(2)}`;
            subtotal += itemTotal;
        });

        // Update the subtotal and total elements
        subtotalElement.textContent = `₹${subtotal.toFixed(2)}`;
        totalElement.textContent = `₹${(subtotal + 50).toFixed(2)}`; // Assuming no additional charges like taxes
    }

    plusButtons.forEach(button => {
        button.addEventListener('click', function() {
            const quantityInput = this.closest('tr').querySelector('.quantity');
            let quantity = parseInt(quantityInput.value);
            quantity += 1; // Increase by 1
            quantityInput.value = quantity;
            updateCart();
        });
    });

    minusButtons.forEach(button => {
        button.addEventListener('click', function() {
            const quantityInput = this.closest('tr').querySelector('.quantity');
            let quantity = parseInt(quantityInput.value);
            if (quantity > 1) {
                quantity -= 1; // Decrease by 1
                quantityInput.value = quantity;
                updateCart();
            }
        });
    });

    // Optionally, update the cart on page load
    updateCart();
});
