/** 
 * Populates a given select element using a given array.
 * @param {string} selectID
 * @param {Array} options
 */
function populateSelect(selectID, options) {
  // select to be populated
  var select = document.getElementById(selectID);

  // option and element placeholders
  var opt;
  var el;

  // for each option
  for (var i = 0; i < options.length; i++) {
    // create an element and assign its text content to option
    opt = options[i];
    el = document.createElement("option");
    el.textContent = opt;
    el.value = opt;

    // append to select element
    select.appendChild(el);
  }
}