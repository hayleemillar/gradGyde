/**
 * Takes in a json and produces a progress bar within a 
 * specified element
 * @param aois some areas of interest, whether that be an AOC, double, or slash
 * @param elementID the ID of the element the progress bars should be appended to
 */
function addProgressBars(aois, type, elementID) {
  
  var area;
  var reqs;
  var numFufilled;

  var progressBar;
  var emptyProgress;
  var partialProgress;

  var element = document.getElementById(elementID);

  // for each area of interest (aoi)
  for (aoi in aois) {

    area = aois[aoi]["name"] + " " + type + " " + aois[aoi]["year"];

    reqs = aois[aoi]["requirements"];

    // number of requirements
    reqCount = Object.keys(reqs).length;
    // initialize count of requirements fufilled to 0
    numFulfilled = 0;

    // for each requirement in requirements
    for (req in reqs) {
      // if the user has fufilled the requirement, increment numFufilled
      if (reqs[req]["fulfilled"] == true) {
        numFulfilled++;
      }
    }

    // PROGRESS BAR
    element.appendChild(document.createElement("br"));

    progressBar = document.createElement("div");
    progressBar.className = "grad-progress";

    // area title
    title = document.createElement("h5");
    titleText = document.createElement("b");
    text = document.createTextNode(area + " : " + 
      numFulfilled.toString() + "/" + reqCount.toString());
    titleText.appendChild(text);
    title.appendChild(titleText);

    progressBar.appendChild(title);

    // empty progress bar that the amount the user has fulfilled will be
    //   displayed over.
    emptyProgress = document.createElement("div");
    emptyProgress.className = "progress";

    // partial filled progress bar to layer over empty progress
    partialProgress = document.createElement("div");
    partialProgress.className = "progress-bar";
    partialProgress.setAttribute("role", "progressbar");
    partialProgress.setAttribute("style", "width: " + ((numFulfilled/reqCount) 
      * 100).toString() + "%;background-color:#222222;");

    // append partial filled progress bar to empty progress bar
    emptyProgress.appendChild(partialProgress);

    // append empty progress bar to the div element grad-progress
    progressBar.appendChild(emptyProgress);

    // append div grad-progress to element retrieved by param elementID
    element.appendChild(progressBar);
  }
}


/**
 * Creates a (string) list of areas of interest and appends it to element 
 * specified by elementID.
 * @param aois some areas of interest, whether that be an AOC, double, or slash
 * @param elementID the element ID to populate
 */
function populateAOIList(aois, elementID) {

  var aoiArray = [];
  var aoiList = "";

  // for each area of interest (aoi)
  for (aoi in aois) {
    // get name of aoi
    aoiArray.push(aois[aoi]["name"] + " " + aois[aoi]["year"]);
  }

  // for each aoi name
  for (var i = 0; i < aoiArray.length; i++) {

    // if there is only one aoi
    if (i == 0 && i == aoiArray.length - 1) {
      aoiList = aoiArray[i];
    // if there is more than one aoi
    } else if (i < aoiArray.length) {
      aoiList = aoiList + aoiArray[i] + ", ";
    // if there is more than one aoi, but the ith aoi is the last in array
    } else if (i == aoiArray.length - 1) {
      aoiList = aoiList + aoiArray[i];
    }
  }

  // create text node and append to element specified by elementID
  text = document.createTextNode(aoiList);
  element = document.getElementById(elementID);
  element.appendChild(text);
}


/**
 * For each area of interest (aoi) in aois, create a tab element of its name
 *  and append it to tabElementID. A form of checkbox requirements will be
 *  associated with the tab and should be displayed when the tab is clicked.
 * @param aois areas of interest
 * @param tabElementID element ID the tab will be appended to
 * @param activeFirst boolean
 * @returns array of element IDs that are associated with the tabs
 */
function populateAoiTabs(activeFirst, aois, tabElementID) {

  // get element the tab will be appended to
  var tabElement = document.getElementById(tabElementID);

  var area;
  var type;
  var year;
  var aoiList;

  var index = 0;
  var tab;
  var button;
  var text;

  // for each area of interest
  for (aoi in aois) {

    // get aoi name
    area = aois[aoi]["name"] ;
    type = aois[aoi]["type"];
    year = aois[aoi]["year"];

    // create tab using bootstrap stuff
    tab = document.createElement("li");
    tab.className = "nav-item";

    button = document.createElement("button");
    button.setAttribute("id", "tab-" + aois[aoi]["id"]);
    button.setAttribute("data-toggle", "tab");
    button.setAttribute("role", "tab");
    button.setAttribute("aria-controls", "dashboard");
    button.setAttribute("style", "font-size:16px;");
    button.setAttribute("onclick", "switchRequirements(aocs, doubles, slashes, '" + area + "', '" + type + "', 'summary')");

    // if the tab is the first one made, make it active by default
    if (index == 0 && activeFirst) {
      button.className = "nav-link active";
      button.setAttribute("aria-selected", "true");
    // if the tab is not the first one, do not make active
    } else {
      button.className = "nav-link";
      button.setAttribute("aria-selected", "false");
    }

    // append elements together to create tab
    switch (type) {
      case "divisional":
        text = document.createTextNode(area + " AOC " + year);
        break;
      case "double":
        text = document.createTextNode(area + " Double " + year);
        break;
      case "slash":
        text = document.createTextNode(area + " Slash " + year);
        break;
    }

    button.appendChild(text);

    tab.appendChild(button);
    tabElement.appendChild(tab);

    // increment
    index++;
  }
}


/**
 * Generates HTML form of requirements based on area of interest.
 * @param aoi
 */
function generateRequirementsHTML(aoiName, aois, aoiType) {
  var html = "";
  var title;

  // console.log(aois[aoi]["name"]);
  // console.log(aoiName);

  // for each aoi
  for (aoi in aois) {
    // if aoi name is the param String aoiName
    if (aois[aoi]["name"] == aoiName) {
      // generate HTML for it

      html += "<h3><center><b id='reqTitle'>Requirements for " + aoiName + " " + aoiType + " " + aois[aoi]["year"].toString() + "</b></center></h3>";

      var reqs = aois[aoi]["requirements"];

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
            html += "<img src='../static/img/check-blue.png'></img><b>" + name + "</b> : " + reqs[req]["amount"].toString() 
            + " course credit required" + "</p>";
          } else {
            html += "<img src='../static/img/check-blue.png'></img><b>" + name + "</b> : " + reqs[req]["amount"].toString() 
            + " course credits required" + "</p>";
          }
        } else {
          if (numCredits == 1) {
            html += "<img src='../static/img/x-blue.png'></img><b>" + name + "</b> : " + reqs[req]["amount"].toString()
            + " course credit required" + "</p>";
          } else {
            html += "<img src='../static/img/x-blue.png'></img><b>" + name + "</b> : " + reqs[req]["amount"].toString()
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
              html += "<p class='tab'><img src='../static/img/check-dark.png'></img>" + name + "</p>";
            // else display text with x box
            } else {
              html += "<p class='tab'><img src='../static/img/x-dark.png'></img>" 
              + name + "</p>";
            }
          } 
        }
      }
      return html;
    }
  }
  // in case something goes wrong
  return "No requirements found";
}


/**
 * Switches the form HTML according to aoi
 */
function switchRequirements(aocs, doubles, slashes, aoiName, aoiType, elementID) {

  element = document.getElementById(elementID);
  // aoi = document.getElementById(aoiID).innerHTML;

  var oldTab;

  for (var i in aocs) {
    oldTab = document.getElementById("tab-" + aocs[i]["id"]);
    if (oldTab.getAttribute("aria-selected") == "true") {
      oldTab.setAttribute("aria-selected", "false");
      oldTab.setAttribute("class", "nav-link");
    }
  }
  for (var i in doubles) {
    oldTab = document.getElementById("tab-" + doubles[i]["id"]);
    if (oldTab.getAttribute("aria-selected") == "true") {
      oldTab.setAttribute("aria-selected", "false");
      oldTab.setAttribute("class", "nav-link");
    }
  }
  for (var i in slashes) {
    oldTab = document.getElementById("tab-" + slashes[i]["id"]);
    if (oldTab.getAttribute("aria-selected") == "true") {
      oldTab.setAttribute("aria-selected", "false");
      oldTab.setAttribute("class", "nav-link");
    }
  }

  var newTab;

  if (aoiType == "divisional") {

    for (var i in aocs) {
      if (aocs[i]["name"] == aoiName) {
        newTab = document.getElementById("tab-" + aocs[i]["id"]);
        newTab.setAttribute("aria-selected", "true");
        newTab.setAttribute("class", "nav-link active");
      }
    }
    element.innerHTML = generateRequirementsHTML(aoiName, aocs, "AOC");

  } else if (aoiType == "double") {

    for (var i in doubles) {
      if (doubles[i]["name"] == aoiName) {
        newTab = document.getElementById("tab-" + doubles[i]["id"]);
        newTab.setAttribute("aria-selected", "true");
        newTab.setAttribute("class", "nav-link active");
      }
    }
    element.innerHTML = generateRequirementsHTML(aoiName, doubles, "Double");

  } else if (aoiType == "slash") {

    for (var i in slashes) {
      if (slashes[i]["name"] == aoiName) {
        newTab = document.getElementById("tab-" + slashes[i]["id"]);
        newTab.setAttribute("aria-selected", "true");
        newTab.setAttribute("class", "nav-link active");
      }
    }
    element.innerHTML = generateRequirementsHTML(aoiName, slashes, "Slash");
  }
}
