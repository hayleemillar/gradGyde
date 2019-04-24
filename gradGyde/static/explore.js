
/**
 * Switches which tab is active.
 * Changes HTML displayed according to which tab is active.
 * @param oldTabID
 * @param newTabID
 */
function switchTab(newTabID, tabIDArray) {

	var oldTab;

	// for each ID
	for (id in tabIDArray) {
		// get element
		oldTab = document.getElementById(tabIDArray[id]);

		// if the element is active, deactivate
		if (oldTab.getAttribute("class") == "nav-link active") {
			oldTab.setAttribute("class", "nav-link");
			oldTab.setAttribute("aria-selected", "false");
		}
	}

	// get new element to be active
	var newTab = document.getElementById(newTabID);

	// set to active
	newTab.setAttribute("class", "nav-link active");
	newTab.setAttribute("aria-selected", "true");
}


/**
 * Generates what HTML is to be displayed.
 * @param tab
 */
function generateHTML(tab) {

}