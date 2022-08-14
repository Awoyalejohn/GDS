/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

let stripePublicKey = document.querySelector("#id_stripe_public_key").innerText.slice(1, -1);
let clientSecret = document.querySelector("#id_client_secret").innerText.slice(1, -1);
let stripe = Stripe(stripePublicKey);
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
  } else {
    errorDiv.textContent = '';
  }
});



// Handle form submit

const form = document.querySelector('#payment-form');

form.addEventListener('submit', (event) => {
  event.preventDefault();
  card.disabled = true;
  document.querySelector('#submit-button').disabled = true;

  stripe.confirmCardPayment(clientSecret, {
    payment_method: {
      card: card,
    }
  }).then(function (result) {
    if (result.error) {
      let errorDiv = document.querySelector('card-errors');
      let html = `
      <span class="icon" role="alert">
        <i class="fas fa-times"></i>
      </span>
      <span>${result.error.message}</span      
    `;
      errorDiv.innerHTML = html;
      card.disabled = false;
      document.querySelector('#submit-button').disabled = false;
    } else {
      if (result.paymentIntent.status === 'succeeded') {
        form.submit();
      }
    }
  })
});