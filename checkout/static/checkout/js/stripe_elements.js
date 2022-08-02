/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

let stripe_public_key = document.querySelector("#id_stripe_public_key").innerText.slice(1, -1);
let client_secret = document.querySelector("#id_client_secret").innerText.slice(1, -1);
let stripe = Stripe(stripe_public_key);
let elements = stripe.elements();
let style = {
  base: {
    color: '#32325d',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};
let card = elements.create('card', { style: style });
card.mount('#card-element');

// Handle realtime validation errors on the card element
card.addEventListener('change', (event) => {
  let errorDiv = document.querySelector('#card-errors');
  if (event.error) {
    let html = `
      <span class="icon" role="alert">
        <i class="fas fa-times"></i>
      </span>
      <span>${event.error.message}</span      
    `;
    errorDiv.innerHTML = html;
  } else{
    errorDiv.textContent = '';
  }
});