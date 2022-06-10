// Get Stripe publishable key
fetch("/config")
.then((result) => { return result.json(); })
.then((data) => {

  // Initialize Stripe.js

  // @ts-ignore
  const stripe = Stripe(data.publicKey);

  // Event handler
  document.querySelector("#submitBtn")!.addEventListener("click", () => {

    const product = document.getElementById('product_slug')!.innerText;

    // Get Checkout Session ID
    fetch("/create-checkout-session/" + product)
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });
});
