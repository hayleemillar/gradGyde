/** 
 * Populates a given select element using a given array.
 * @param {string} selectID
 * @param {Array} options
 */
function populateSelect(selectID, options) {
  var select = document.getElementById(selectID);

  for (var i = 0; i < options.length; i++) {
    var opt = options[i];
    var el = document.createElement("option");
    el.textContent = opt;
    el.value = opt;
    select.appendChild(el);
  }

}