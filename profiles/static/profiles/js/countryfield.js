const country = document.querySelector('#id_default_country')
let countrySelected = country.value;

if (!countrySelected) {
  country.style.color = '#aab7c4';
}
country.addEventListener('change', (event) => {
    countrySelected = event.target.value;
    if(!countrySelected) {
      event.target.style.color = '#aab7c4';
    } else{
      event.target.style.color = '#000'
    }
});