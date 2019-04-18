/**
 * Takes in a json and produces a progress bar within a 
 * specified element
 * @param aois some areas of interest, whether that be an AOC, double, or slash
 * @param elementID the ID of the element the progress bars should be appended to
 */
function addProgressBars(aois, elementID) {
  
  var area;
  var reqs;
  var numFufilled;

  var progressBar;
  var emptyProgress;
  var partialProgress;

  var element = document.getElementById(elementID);

  // for each area of interest (aoi)
  for (aoi in aois) {

    area = aois[aoi]["Name"];

    reqs = aois[aoi]["Requirements"];

    // number of requirements
    reqCount = Object.keys(reqs).length;
    // initialize count of requirements fufilled to 0
    numFulfilled = 0;

    // for each requirement in requirements
    for (req in reqs) {
      // if the user has fufilled the requirement, increment numFufilled
      if (reqs[req]["Fulfilled"] == true) {
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
    aoiArray.push(aois[aoi]["Name"]);
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
 * @param bodyElementID element ID the form will be appended to
 * @returns array of element IDs that are associated with the tabs
 */
function populateAoiTabs(aois, tabElementID) {

  // get element the tab will be appended to
  var tabElement = document.getElementById(tabElementID);

  var area;
  var aoiList;

  var index = 0;
  var tab;
  var button;
  var text;

  // for each area of interest
  for (aoi in aois) {

    // get aoi name
    area = aois[aoi]["Name"];

    // create tab using bootstrap stuff
    tab = document.createElement("li");
    tab.className = "nav-item";

    button = document.createElement("button");
    button.setAttribute("id", "aoc-" + index.toString());
    button.setAttribute("data-toggle", "tab");
    button.setAttribute("role", "tab");
    button.setAttribute("aria-controls", "dashboard");
    button.setAttribute("style", "font-size:16px;");
    button.setAttribute("onclick", "switchRequirements(this.id, 'summary')");

    // if the tab is the first one made, make it active by default
    if (index == 0) {
      button.className = "nav-link active";
      button.setAttribute("aria-selected", "true");
    // if the tab is not the first one, do not make active
    } else {
      button.className = "nav-link";
      button.setAttribute("aria-selected", "false");
    }

    // append elements together to create tab
    text = document.createTextNode(area);
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
function generateRequirementsHTML(aoiName, aois) {
  var html = "";

  html += "<h3><center><b>Requirements for " + aoiName + "</b></center></h3>";

  for (aoi in aois) {
    if (aois[aoi]["Name"] == aoiName) {
      var reqs = aois[aoi]["Requirements"];

      var name;
      var fulfilled;

      for (req in reqs) {

        name = reqs[req]["Name"];
        fulfilled = reqs[req]["Fulfilled"];

        if (fulfilled == true) {
          html += "<img src='../static/img/check-blue.png'></img>" + name;
        } else {
          html += "<img src='../static/img/x-blue.png'></img>" + name;
        }

        if (reqs[req].hasOwnProperty("Classes")) {

          var courses = reqs[req]["Classes"];
          var taken;

          for (course in courses) {

            name = courses[course]["Name"];
            taken = courses[course]["Taken"];

            if (taken == true) {
              html += "<p class='tab'><img src='../static/img/check-dark.png'></img>" + name + "</p>";
            } else {
              html += "<p class='tab'><img src='../static/img/x-dark.png'></img>" + name + "</p>";
            }
          } 
        }
      }
      return html;
    }
  }
  return "No requirements could be found";
}


/**
 * Switches the form HTML according to 
 */
function switchRequirements(aois, aoiID, elementID) {

  element = document.getElementById(elementID);
  aoi = document.getElementById(aoiID).innerHTML;
  console.log(aoi);
  console.log(aois);

  element.innerHTML = generateRequirementsHTML(aoi, aois);
}




reqs = {};

aois = $.extend(aocs, doubles);
aois = $.extend(aois, slashes);

// var aocs is declared in dash_stud.html
// this is because it is data from the DB and is received by the HTML

populateAOIList(aois, "user-aoc");
addProgressBars(aois, "progress-bars");
populateAoiTabs(aois, "summary-tabs");
switchRequirements(aois, "aoc-0", "reqHTML");