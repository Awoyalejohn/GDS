//  Code to calculate quote request form checkout total when the type and size are selected in the select box
let typeArray = [0];
let sizeArray = [0];
let subtotal = 0;
let subtotalElement =  document.querySelector('#subtotal');
let discountPercent = 10;
let discountElement = document.querySelector('#discount');
let totalElement = document.querySelector('#total');

// checks the type select box is selceted and changes the price shown on the card total box
// on the quote request page
const selectType = document.querySelector('#id_type');
  selectType.addEventListener('change', (event) => {
    let selectedValue = event.target.value;
    let typeCost = null;
    let discount = null;

    // selects the price based on the current value
    if (selectedValue == 'IC' || selectedValue == 'ST') {
      typeCost = 9.99;
    } else if (selectedValue == 'LG' || selectedValue == 'BN') {
      typeCost = 19.99;
    } else if (selectedValue == 'PS' || selectedValue == 'WP') {
      typeCost = 39.99;
    } else {
      typeCost = 0;
    }

    typeArray[0] = typeCost;
    subtotal = (typeArray[0] + sizeArray[0]).toFixed(2);
    if (subtotal > 40) {
      discount = (subtotal * discountPercent / 100).toFixed(2);
    } else {
      discount = (0).toFixed(2);
    }
    
    subtotalElement.textContent = "£" + subtotal.toString();
    discountElement.textContent = "-£" + discount.toString();
    let total = (subtotal - discount).toFixed(2);
    totalElement.textContent = "£" + total.toString();

  });


// checks the size select box is selceted and changes the price shown on the card total box
// on the quote request page
const selectSize = document.querySelector('#id_size');
  selectSize.addEventListener('change', (event) => {
    let selectedValue = event.target.value;
    let sizeCost = null;
    let discount = null;

    // selects the price based on the current value
    if (selectedValue == 'S') {
      sizeCost = 9.99;
    } else if (selectedValue == 'M') {
      sizeCost = 19.99;
    } else if (selectedValue == 'L') {
      sizeCost = 29.99;
    } else {
      sizeCost = 0;
    }

    sizeArray[0] = sizeCost;
    subtotal = (typeArray[0] + sizeArray[0]).toFixed(2);
    if (subtotal > 40) {
      discount = (subtotal * discountPercent / 100).toFixed(2);
    } else {
      discount = (0).toFixed(2);
    }
    subtotalElement.textContent = "£" + subtotal.toString();
    discountElement.textContent = "-£" + discount.toString();
    let total = (subtotal - discount).toFixed(2);
    totalElement.textContent = "£" + total.toString();

  });

