
/**
 * Switches which tab is active.
 * Changes HTML displayed according to which tab is active.
 * @param oldTabID
 * @param newTabID
 */
function switchTab(newTabID, tabIDArray, elementID) {

	var temp;

	// for each ID
	for (id in tabIDArray) {
		// get element
		temp = document.getElementById(tabIDArray[id]);

		// if the element is active, deactivate
		if (temp.getAttribute("aria-selected") == "true") {
			var oldTab = temp;
			oldTab.setAttribute("class", "nav-link");
			oldTab.setAttribute("aria-selected", "false");
		}
	}

	// get new element to be active
	var newTab = document.getElementById(newTabID);

	// set to active
	newTab.setAttribute("class", "nav-link active");
	newTab.setAttribute("aria-selected", "true");

	var oldFormID = "form-" + oldTab.getAttribute("id");

	generateForm(newTabID, elementID, oldFormID);
}


/**
 * Generates what HTML is to be displayed.
 * @param tab
 */
function generateForm(tab, elementID, oldFormID) {

	var oldForm = document.getElementById(oldFormID);
	oldForm.parentNode.removeChild(oldForm);

	var label;
	var input;
	var select;
	var text;
	var option;
	var button;

	var form = document.createElement("form");
	form.setAttribute("method", "post");
	form.setAttribute("action", "");

	if (tab == "courses") {
		form.setAttribute("id", "form-courses");

		/***************
		 * COURSE NAME *
		 ***************/
		// label
		label = document.createElement("label");
		label.setAttribute("for", "inputName");

		text = document.createTextNode("Course Name");
		label.appendChild(text);

		form.appendChild(label);

		// input
		input = document.createElement("input");
		input.setAttribute("name", "name");
		input.setAttribute("type", "text");
		input.setAttribute("class", "form-control");
		input.setAttribute("id", "inputName");
		input.setAttribute("placeholder", "Enter course name");

		form.appendChild(input);

		// line break
		form.appendChild(document.createElement("br"));


		/****************
		 * YEAR OFFERED *
		 ****************/
		// label
		label = document.createElement("label");
		label.setAttribute("for", "inputYear");

		text = document.createTextNode("Year");
		label.appendChild(text);

		form.appendChild(label);

		// input
		input = document.createElement("input");
		input.setAttribute("name", "year");
		input.setAttribute("type", "number");
		input.setAttribute("class", "form-control");
		input.setAttribute("id", "inputYear");
		input.setAttribute("placeholder", "Enter year");

		form.appendChild(input);

		// line break
		form.appendChild(document.createElement("br"));


		/********************
		 * SEMESTER OFFERED *
		 ********************/
		// label
		label = document.createElement("label");
		label.setAttribute("for", "selectSemester");

		text = document.createTextNode("Select semester");
		label.appendChild(text);

		form.appendChild(label);

		// select
		select = document.createElement("select");
		select.setAttribute("name", "semester");
		select.setAttribute("id", "select_semester");
		select.setAttribute("class", "mdb-select colorful-select dropdown-primary md-form");
		select.setAttribute("for", "selectSemester");

		// select options
		option = document.createElement("option");
    option.textContent = "Fall";
    option.value = "Fall";
    select.appendChild(option);

    option = document.createElement("option");
    option.textContent = "Spring";
    option.value = "Spring";
    select.appendChild(option);

    option = document.createElement("option");
    option.textContent = "Summer";
    option.value = "Summer";
    select.appendChild(option);

    form.appendChild(document.createElement("br"));

    form.appendChild(select);

    // 2 line breaks
    form.appendChild(document.createElement("br"));
    form.appendChild(document.createElement("br"));

    // submit button
    // submit = document.createElement("center");

    button = document.createElement("button");
    button.setAttribute("onclick", "location.href='/student_dashboard/explore");
    button.setAttribute("style", "border-radius:3px;");

    text = document.createTextNode("Search");
    button.appendChild(text);

    form.appendChild(button);


	} else {

		/************
		 * AOC NAME *
		 ************/
		// label
		label = document.createElement("label");
		label.setAttribute("for", "inputName");

		switch (tab) {
			case "aocs":
				form.setAttribute("id", "form-aocs");
				text = document.createTextNode("AOC Name");
				break;
			case "doubles":
				form.setAttribute("id", "form-doubles");
				text = document.createTextNode("Double Name");
				break;
			case "slashes":
				form.setAttribute("id", "form-slashes");
				text = document.createTextNode("Slash Name");
		}

		label.appendChild(text);

		form.appendChild(label);

		// input
		input = document.createElement("input");
		input.setAttribute("name", "name");
		input.setAttribute("type", "text");
		input.setAttribute("class", "form-control");
		input.setAttribute("id", "inputName");

		switch (tab) {
			case "aocs":
				input.setAttribute("placeholder", "Enter AOC name");
				break;
			case "doubles":
				input.setAttribute("placeholder", "Enter double name");
				break;
			case "slashes":
				input.setAttribute("placeholder", "Enter slash name");
		}

		form.appendChild(input);

		// line break
		form.appendChild(document.createElement("br"));


		/****************
		 * YEAR OFFERED *
		 ****************/
		// label
		label = document.createElement("label");
		label.setAttribute("for", "inputYear");

		text = document.createTextNode("Year");
		label.appendChild(text);

		form.appendChild(label);

		// input
		input = document.createElement("input");
		input.setAttribute("name", "year");
		input.setAttribute("type", "number");
		input.setAttribute("class", "form-control");
		input.setAttribute("id", "inputYear");
		input.setAttribute("placeholder", "Enter year");

		form.appendChild(input);

		// 2 line breaks
		form.appendChild(document.createElement("br"));
		form.appendChild(document.createElement("br"));

		// submit button
		button = document.createElement("button");
    button.setAttribute("onclick", "location.href='/student_dashboard/explore");
    button.setAttribute("style", "border-radius:3px;");

    text = document.createTextNode("Search");
    button.appendChild(text);

    form.appendChild(button);
	}

	var element = document.getElementById(elementID);
	element.appendChild(form);
}