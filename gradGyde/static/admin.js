
/**
 * Switches which tab is active.
 * Changes HTML displayed according to which tab is active.
 * @param newTabID
 * @param tabIDArray
 * @param elementID
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

  // reset results section to have nothing in it.
  var divResults = document.getElementById("results");
  divResults.innerHTML = "";

  generateForm(newTabID, elementID, oldFormID);
}


/**
 * Generates what HTML is to be displayed.
 * @param tab
 * @param elementID
 * @param oldFormID
 */
function generateForm(tab, elementID, oldFormID) {

  var label;
  var input;
  var select;
  var text;
  var option;
  var button;

  // get old form and remove
  var oldForm = document.getElementById(oldFormID);
  oldForm.parentNode.removeChild(oldForm);

  // get element
  var element = document.getElementById(elementID);

  // start fresh with a new form
  var form = document.createElement("form");

  // button to add course or add an area of interest
  button = document.createElement("button");
  button.setAttribute("type", "button");
  button.setAttribute("data-toggle", "modal");
  button.setAttribute("style", "margin: 0 auto");

  // if button is for adding a course
  if (tab == "courses") {
    button.setAttribute("href", "#courseModal");

    // add text accordingly, append to form
    text = document.createTextNode("Add Course");
    button.appendChild(text);
    form.appendChild(button);

    // set form id
    form.setAttribute("id", "form-courses");

    // break 
    form.appendChild(document.createElement("br"));
    form.appendChild(document.createElement("br"));
    form.appendChild(document.createElement("br"));


    // the main portion of the form now for adding courses

    /***************
     * COURSE NAME *
     ***************/
    // label
    label = document.createElement("label");
    label.setAttribute("for", "inputName");

    // text
    text = document.createTextNode("Course Name");
    label.appendChild(text);

    // append to form
    form.appendChild(label);

    // input
    input = document.createElement("input");
    input.setAttribute("name", "name");
    input.setAttribute("type", "text");
    input.setAttribute("class", "form-control");
    input.setAttribute("id", "inputName");
    input.setAttribute("placeholder", "Enter course name");

    // append to form
    form.appendChild(input);

    // line break
    form.appendChild(document.createElement("br"));


    /****************
     * YEAR OFFERED *
     ****************/
    label = document.createElement("label");
    label.setAttribute("for", "inputYear");

    text = document.createTextNode("Year");
    label.appendChild(text);

    form.appendChild(label);
    form.appendChild(document.createElement("br"));

    select = document.createElement("select");
    select.setAttribute("name", "year");
    select.setAttribute("id", "inputYear");
    select.setAttribute("class", "mdb-select colorful-select dropdown-primary md-form");

    // populate select for year
    var currentYear = new Date().getFullYear(), years = [];
    startYear = currentYear - 10;

    var el;
    var opt;

    opt = "Any";
    el = document.createElement("option");
    el.textContent = opt;
    el.value = opt;
    select.appendChild(el);

    while (startYear <= currentYear) {
      opt = startYear;
      el = document.createElement("option");
      el.textContent = opt;
      el.value = opt;
      select.appendChild(el);

      startYear++;
    }

    form.appendChild(select);

    // line break
    form.appendChild(document.createElement("br"));
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

    // select semester
    select = document.createElement("select");
    select.setAttribute("name", "semester");
    select.setAttribute("id", "selectSemester");
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
    button.setAttribute("onclick", "getResults('courses', event);");
    button.setAttribute("style", "border-radius:3px;");

    text = document.createTextNode("Search");
    button.appendChild(text);

    form.appendChild(button);


  // if an area of interest (AOC, double, slash)
  } else {

    /********
     * NAME *
     ********/
    // label
    label = document.createElement("label");
    label.setAttribute("for", "inputName");

    // switch cases to determine which type
    switch (tab) {
      case "aocs":

        button.setAttribute("href", "#aocModal");

        text = document.createTextNode("Add AOC");

        button.appendChild(text);
        form.appendChild(button);

        form.setAttribute("id", "form-aocs");
        text = document.createTextNode("AOC Name");

        break;
      case "doubles":

        button.setAttribute("href", "#doubleModal");

        text = document.createTextNode("Add Double");

        button.appendChild(text);
        form.appendChild(button);

        form.setAttribute("id", "form-doubles");
        text = document.createTextNode("Double Name");

        break;
      case "slashes":

        button.setAttribute("href", "#slashModal");

        text = document.createTextNode("Add Slash");

        button.appendChild(text);
        form.appendChild(button);

        form.setAttribute("id", "form-slashes");
        text = document.createTextNode("Slash Name");

        break;
    }

    form.appendChild(document.createElement("br"));
    form.appendChild(document.createElement("br"));
    form.appendChild(document.createElement("br"));

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
        break;
    }

    form.appendChild(input);

    // line break
    form.appendChild(document.createElement("br"));


    /****************
     * YEAR OFFERED *
     ****************/
    label = document.createElement("label");
    label.setAttribute("for", "inputYear");

    text = document.createTextNode("Year");
    label.appendChild(text);

    form.appendChild(label);
    form.appendChild(document.createElement("br"));

    select = document.createElement("select");
    select.setAttribute("name", "year");
    select.setAttribute("id", "inputYear");
    select.setAttribute("class", "mdb-select colorful-select dropdown-primary md-form");

    // populate select for year
    var currentYear = new Date().getFullYear(), years = [];
    startYear = currentYear - 10;

    var el;
    var opt;

    opt = "Any";
    el = document.createElement("option");
    el.textContent = opt;
    el.value = opt;
    select.appendChild(el);

    while (startYear <= currentYear) {
      opt = startYear;
      el = document.createElement("option");
      el.textContent = opt;
      el.value = opt;
      select.appendChild(el);

      startYear++;
    }

    form.appendChild(select);

    // 2 line breaks
    form.appendChild(document.createElement("br"));
    form.appendChild(document.createElement("br"));

    // submit button
    button = document.createElement("button");
    button.setAttribute("style", "border-radius:3px;");

    switch (tab) {
      case "aocs":
        button.setAttribute("onclick", "getResults('aocs', event);");
        break;
      case "doubles":
        button.setAttribute("onclick", "getResults('doubles', event);");
        break;
      case "slashes":
        button.setAttribute("onclick", "getResults('slashes', event);");
        break;
    }

    text = document.createTextNode("Search");
    button.appendChild(text);

    form.appendChild(button);
  }

  element.appendChild(form);
}


/*
 * Gets the results and displays in results section of the page.
 * @param type
 */
function getResults(searchType, event) {
  event.preventDefault();

  var formID = "#form-" + searchType

  if (searchType == "courses") {

    $.ajax({url: "/admin/results", 
      type: "get",
      data: {
        type: "courses",
        name: document.getElementById("inputName").value,
        year: document.getElementById("inputYear").value,
        semester: document.getElementById("selectSemester").value
      },
      success: function(results) {
        results = JSON.parse(results);

        // display results

        var resultsSection = document.getElementById("results");
        resultsSection.innerHTML = "";

        var text;
        var h;
        var hr;
        var p;
        var b;
        var button;

        // results title
        h = document.createElement("h3");
        var b = document.createElement("b");
        text = document.createTextNode("Results");
        b.appendChild(text);
        h.appendChild(b);
        resultsSection.appendChild(h);
        resultsSection.appendChild(document.createElement("br"));

        for (var i in results) {
          course = results[i];

          // name portion
          b = document.createElement("b");

          text = document.createTextNode(course["name"]);
          b.appendChild(text);

          h = document.createElement("h5");
          h.appendChild(b);
          h.setAttribute("id", "h-" + course["id"]);
          resultsSection.appendChild(h);

          // info portion
          // create p element, style for indentation
          p = document.createElement("p");
          p.setAttribute("style", "margin-left: 40px;font-size:16px;");
          p.setAttribute("id", "p-" + course["id"]);

          text = document.createTextNode("Year: " + course["year"]);
          p.appendChild(text);
          p.appendChild(document.createElement("br"));
          text = document.createTextNode("Semester: " + course['semester']);
          p.appendChild(text);
          p.appendChild(document.createElement("br"));

          resultsSection.appendChild(p);

          button = document.createElement("button");
          button.setAttribute("id", course["id"]);
          button.setAttribute("onclick", "removeCourse(this.id)");
          button.setAttribute("style", "font-size:14px;");

          text = document.createTextNode("Remove");
          button.appendChild(text);

          resultsSection.appendChild(button);

          resultsSection.appendChild(document.createElement("hr"));
        }
      },
      error: function(xhr) {
        // display an error message
        console.log("error");
      }
    });
  } else {

    $.ajax({url: "/admin/results", 
      type: "get",
      data: {
        type: searchType,
        name: document.getElementById("inputName").value,
        year: document.getElementById("inputYear").value,
      },
      success: function(results) {
        results = JSON.parse(results);

        // display results

        var resultsSection = document.getElementById("results");
        resultsSection.innerHTML = ""

        // results title
        h = document.createElement("h3");
        var b = document.createElement("b");
        text = document.createTextNode("Results");
        b.appendChild(text);
        h.appendChild(b);
        resultsSection.appendChild(h);
        resultsSection.appendChild(document.createElement("br"));

        var aoi;
        var html
        var h;
        var text;
        var p;
        var b;

        for (var i in results) {
          aoi = results[i];

          // name portion
          b = document.createElement("b");

          var type = aoi["type"];

          switch (type) {
            case ("aoc"):
              type = "AOC";
              break;
            case ("double"):
              type = "Double";
              break;
            case ("slash"):
              type = "Slash";
              break;
          }
          var year = aoi["year"];

          text = document.createTextNode(aoi["name"] + " " + type + " " + year);
          b.appendChild(text);

          h = document.createElement("h5");
          h.setAttribute("id", "h-" + aoi["id"]);
          h.appendChild(b);
          resultsSection.appendChild(h);

          // info portion
          // create p element, style for indentation
          p = document.createElement("p");
          p.setAttribute("style", "margin-left: 40px;font-size:16px;");
          p.setAttribute("id", "p-" + aoi["id"]);

          html = generateRequirementsHTML(aoi["name"], aoi); 

          p.insertAdjacentHTML('beforeend', html);

          resultsSection.appendChild(p);

          button = document.createElement("button");
          button.setAttribute("id", aoi["id"]);
          button.setAttribute("onclick", "removeAOI(this.id, '" + aoi["name"] + " " + type + " " + year + "')");
          button.setAttribute("style", "font-size:14px;");

          text = document.createTextNode("Remove");
          button.appendChild(text);

          resultsSection.appendChild(button);

          resultsSection.appendChild(document.createElement("hr"));
        }
      },
      error: function(xhr) {
        // display an error message
        console.log("error");
      }
    });
  }
}


/**
 * Generates HTML form of requirements based on area of interest.
 * @param aoi
 */
function generateRequirementsHTML(aoiName, aoi) {
  var html = "";

  var reqs = aoi["requirements"];

  var name;
  var fulfilled;
  var numCredits;

  // for each requirement
  for (req in reqs) {

    // get requirement name, whether it has been fulfilled, and # credits
    name = reqs[req]["name"];
    fulfilled = reqs[req]["fulfilled"];
    numCredits = reqs[req]["amount"];

    // if the req is fulfilled
    if (fulfilled == true) {
      // if the req only requires a single course to be satisfied,
      // use correct grammar
      if (numCredits == 1) {
        html += "<img src='../static/img/check-blue.png' height='16px'></img><b>" + name + "</b> : " + reqs[req]["amount"].toString() 
        + " course credit required" + "</p>";
      } else {
        html += "<img src='../static/img/check-blue.png' height='16px'></img><b>" + name + "</b> : " + reqs[req]["amount"].toString() 
        + " course credits required" + "</p>";
      }
    } else {
      if (numCredits == 1) {
        html += "<img src='../static/img/x-blue.png' height='16px'></img><b>" + name + "</b> : " + reqs[req]["amount"].toString()
        + " course credit required" + "</p>";
      } else {
        html += "<img src='../static/img/x-blue.png' height='16px'></img><b>" + name + "</b> : " + reqs[req]["amount"].toString()
        + " course credits required" + "</p>";
      }
    }

    // if requirement has classes
    if (reqs[req].hasOwnProperty("classes")) {

      var courses = reqs[req]["classes"];
      var taken;

      // for each course
      for (course in courses) {

        name = courses[course]["name"];
        taken = courses[course]["taken"];

        // if taken display text with check box
        if (taken == true) {
          html += "<p class='tab'><img src='../static/img/check-dark.png' height='16px'></img>" + name + "</p>";
        // else display text with x box
        } else {
          html += "<p class='tab'><img src='../static/img/x-dark.png' height='16px'></img>" 
          + name + "</p>";
        }
      } 
    }
  }
  return html;
}

/**
 * Post request to add course as taken by user.
 */
function removeCourse(courseID, name) {
  retVal = confirm("Are you sure you want to remove " + name + "?");

  if (retVal == true) {
    $.post("/admin/removecourse", {
      id: courseID
    });

    var button = document.getElementById(courseID);
    var text = document.getElementById("text" + courseID);

    button.parentElement.removeChild(button);

    var p = document.getElementById("p-" + courseID);
    p.parentElement.removeChild(p);

    var h = document.getElementById("h-" + courseID);
    h.parentElement.removeChild(h);
  }
}

/**
 * Post request to add AOI as taken by user.
 */
function removeAOI(aoiID, name) {
  retVal = confirm("Are you sure you want to remove " + name + "?");

  if (retVal == true) {
    $.post("/admin/removeaoi", {
      id: aoiID
    });

    var button = document.getElementById(aoiID);
    var text = document.getElementById("text" + aoiID);

    button.parentElement.removeChild(button);

    var p = document.getElementById("p-" + aoiID);
    p.parentElement.removeChild(p);

    var h = document.getElementById("h-" + aoiID);
    h.parentElement.removeChild(h);
  }
}


var aocIndex = 1;
var doubleIndex = 1;
var slashIndex = 1;

/**
 * 
 */
function addRequirement(elementID, type) {
  if (type == "AOC") {
    index = aocIndex;
  } else if (type == "Double") {
    index = doubleIndex;
  } else {
    index = slashIndex;
  }

  form = document.getElementById(elementID);

  form.appendChild(document.createElement("br"));
  form.appendChild(document.createElement("br"));

  // requirement
  var label = document.createElement("label");
  label.setAttribute("for", "select" + type + "Req" + index);

  var text = document.createTextNode("Requirement " + index);
  label.appendChild(text);

  form.appendChild(label);
  form.appendChild(document.createElement("br"));

  var select = document.createElement("select");
  select.setAttribute("class", type.toLowerCase() + "req" + index + " form-control");
  select.setAttribute("name", "req" + index);
  select.setAttribute("style", "width:100%;");
  select.setAttribute("id", "select" + type + "Req" + index);

  form.appendChild(select);
  form.appendChild(document.createElement("br"));
  form.appendChild(document.createElement("br"));

  // credits and courses
  var div = document.createElement("div");
  div.setAttribute("class", "tab");

  label = document.createElement("label");
  label.setAttribute("for", "input" + type + "Req" + index + "Credit");

  text = document.createTextNode("Number Credits Required for Requirement " + index);
  label.appendChild(text);

  div.appendChild(label);
  div.appendChild(document.createElement("br"));

  var input = document.createElement("input");
  input.setAttribute("name", "req" + index + "Credit");
  input.setAttribute("type", "number");
  input.setAttribute("class", "form-control");
  input.setAttribute("id", "input" + type + "Req" + index + "Credit");
  input.setAttribute("placeholder", "Enter number credits required");
  input.setAttribute("min", "0");

  div.appendChild(input);
  div.appendChild(document.createElement("br"));

  label = document.createElement("label");
  label.setAttribute("for", "select" + type + "Req" + index + "Courses");

  text = document.createTextNode("Courses for Requirement " + index);
  label.appendChild(text);

  div.appendChild(label);
  div.appendChild(document.createElement("br"));

  select = document.createElement("select");
  select.setAttribute("class", type.toLowerCase() + "req" + index + "courses form-control");
  select.setAttribute("name", "req" + index + "courses");
  select.setAttribute("style", "width:100%;");
  select.setAttribute("id", "select" + type + "Req" + index + "Courses");
  select.setAttribute("multiple", "multiple");
  select.disabled = true;

  div.appendChild(select);

  form.appendChild(div);

  // select2 and jquery to populate search dropdown in forms

  $("." + type.toLowerCase() + "req" + index).select2({
    data: reqs,
    tags: true,
    tokenSeparators: [','],
    createTag: function (params) {
      var term = $.trim(params.term);


      if (term === '') {
        return null;
      }

      document.getElementById("select" + type + "Req" + index + "Courses").disabled = false;

      return {
        id: term,
        text: term,
        newTag: true, // add additional parameters
      }
    }
  });

  $("." + type.toLowerCase() + "req" + index + "courses").select2({
    data: courses,
    tags: true,
    tokenSeparators: [','],
    createTag: function(params) {
      return undefined;
    }
  });


  if (type == "AOC") {
    aocIndex++;
  } else if (type == "Double") {
    doubleIndex++;
  } else {
    slashIndex++;
  }
}