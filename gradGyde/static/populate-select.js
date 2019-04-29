/** 
 * Populates a given select element using a given array.
 * @param {string} selectID
 * @param {Array} options
 */
function populateSelect(selectID, options) {
  var select = document.getElementById(selectID);

  var opt;
  var el;

  for (var i = 0; i < options.length; i++) {
    opt = options[i];
    el = document.createElement("option");
    el.textContent = opt;
    el.value = opt;
    select.appendChild(el);
  }
}