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
  } else{
    errorDiv.textContent = '';
  }
});

// Handle form submit
const form = document.querySelector('#payment-form');

form.addEventListener('submit', (event) => {
  // Prevents form from submitting
  event.preventDefault();
  //disables card element
  card.disabled = true;
  document.querySelector('#submit-button').disabled = true;

  // Checks the checkbox if its checked
  let saveInfo = document.querySelector('#id-save-info')
  if (typeof (saveInfo) != 'undefined' && saveInfo != null) {
    saveInfo = saveInfo.checked;
  } else {
    saveInfo = false;
  }

  // Gets CSRF Token from using {% csrf_token %} in the form
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  // Url that the data will be posted to
  const url = '/checkout/cache_checkout_data/';

  //headers
  headerInfo = {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken,
  };

  // Data to post
  const postData = {
    "client_secret": clientSecret,
    "save_info": saveInfo
  };

  // Django docs implementation of posting data with CSRF token
  const request = new Request(
    url,
    {
      method: 'POST',
      headers: headerInfo,
      body: JSON.stringify(postData),
      mode: 'same-origin' // Do not send CSRF token to another domain.
    }
  );

  fetch(request)
    .then(function (data) {
      stripe.confirmCardPayment(clientSecret, {
        payment_method: {
          card: card,
          billing_details: {
            name: form.full_name.value.trim(),
            phone: form.phone_number.value.trim(),
            email: form.email.value.trim(),
            address: {
              line1: form.street_address1.value.trim(),
              line2: form.street_address2.value.trim(),
              city: form.town_or_city.value.trim(),
              country: form.country.value.trim(),
              state: form.county.value.trim(),
            }
          }
        },
        shipping: {
          name: form.full_name.value.trim(),
          phone: form.phone_number.value.trim(),
          address: {
            line1: form.street_address1.value.trim(),
            line2: form.street_address2.value.trim(),
            city: form.town_or_city.value.trim(),
            country: form.country.value.trim(),
            postal_code: form.postcode.value.trim(),
            state: form.county.value.trim(),
          }
        },
      }).then(function (result) {
        if (result.error) {
          let errorDiv = document.querySelector('#card-errors');
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
    })
    .catch(function (error) {
      // Reloads the page
      location.reload();
    });
});