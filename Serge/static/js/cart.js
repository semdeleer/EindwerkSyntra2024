var updateBtns = document.getElementsByClassName('update-cart');

for (let i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener('click', function handleUpdateClick() {
    const productId = this.dataset.product;
    const action = this.dataset.action;

    console.log('productId:', productId, 'Action:', action);

    if (user === 'AnonymousUser') {
      addCookieItem(productId, action);
    } else {
      updateUserOrder(productId, action);
    }
  });
}

function updateUserOrder(productId, action) {
  console.log('User is authenticated, sending data...');

  const url = '/update_item/';

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ productId, action }), // Destructuring for concise data
  })
    .then((response) => response.json())
    .then((data) => {
      // Handle successful update (e.g., update UI, confirmation message)
      console.log('Update successful:', data); // Log response for debugging
    })
    .catch((error) => {
      // Handle errors gracefully (e.g., display error message to user)
      console.error('Update failed:', error);
    });
}

function addCookieItem(productId, action) {
  console.log('User is not authenticated');

  let cart = JSON.parse(document.cookie.match(/cart=(.*?)(;|$)/)?.[1] || '{}'); // Robust cookie parsing

  if (action === 'add') {
    if (!cart[productId]) {
      cart[productId] = { quantity: 1 };
    } else {
      cart[productId].quantity++;
    }
  } else if (action === 'remove') {
    if (cart[productId]) {
      cart[productId].quantity--;
      if (cart[productId].quantity <= 0) {
        delete cart[productId];
      }
    } else {
      console.warn('Item not found in cart for removal:', productId); // Log warning
    }
  } else {
    console.warn('Invalid action for addCookieItem:', action); // Log warning
  }

  console.log('CART:', cart);
  document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/';

  // Consider a more granular update
  location.reload(); // Reload for a full refresh (optional, adjust based on your needs)
}
