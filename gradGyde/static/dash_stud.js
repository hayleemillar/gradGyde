aocs = {
  "AOC1" : {
    "Name" : "Computer Science 2018",
    "Requirements" : {
      "Req1" : {
        "Name" :  "CS Introductory Course",
        "Amount" : 1,
        "Fulfilled" : true,
        "Classes" : {
          "Class1" : {
            "Name" : "Intro to Programming in Python",
            "Taken" : false
          },
          "Class2" : {
            "Name" : "Intro to Programming in C",
            "Taken" : true
          }   
        }   
      },
      "Req2" : {
        "Name" :  "Math",
        "Amount" : 2,
        "Fulfilled" : false,
        "Classes" : {
          "Class1" : {
            "Name" : "Calculus 1",
            "Taken" : false
          },
          "Class2" : {
            "Name" : "Discrete Mathematics for Computer Science",
            "Taken" : true
          },
          "Class3" : {
            "Name" : "Dealing With Data",
            "Taken" : false
          }   
        }   
      }
    }
  }
};

/**
 * @param aoi some areas of interest, whether that be an AOC, double, or slash
 * @param 
 * 
 * Takes in a json and produces a progress bar within a 
 * specified element
 */
function addProgressBars(aois, elementID) {
  
  var course;
  var reqs;
  var numFufilled;

  var progressBar;
  var emptyProgress;
  var partialProgress;

  var element = document.getElementById(elementID);

  // for each area of interest (aoi)
  for (aoi in aois) {

    course = aois[aoi]["Name"];

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

    console.log(numFulfilled);

    // PROGRESS BAR
    element.appendChild(document.createElement("br"));

    progressBar = document.createElement("div");
    progressBar.className = "grad-progress";

    // course title
    title = document.createElement("h5");
    titleText = document.createElement("b");
    text = document.createTextNode(course + " : " + 
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

addProgressBars(aocs, "progress-bars");