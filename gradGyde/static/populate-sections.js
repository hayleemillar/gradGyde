
/**
 * Populates the sections of the course history according to year.
 * @param elementID
 * @param jsonData
 * @param sectionType
 * @param boolSort
 */
function populateSections(elementID, jsonData, sectionType, boolSort) {
  var sections = [];

  // for each course
  for (var i in jsonData) {
    // if year course was offered not in array, push to array sections
    if (!(sections.includes(jsonData[i][sectionType]))) {
      sections.push(jsonData[i][sectionType]);
    }
  }

  // if sections need to be sorted, sort in descending order
  if (boolSort == true) {
    // sort years in descending order
    sections.sort();
  }

  // get element sections will be appended to
  var element = document.getElementById(elementID);
  var section;
  var text;
  var b;

  // for each section
  for (var i in sections) {
    // populate html
    section = document.createElement("h4");
    section.setAttribute("id", sections[i].toString())
    b = document.createElement("b");
    text = document.createTextNode(sections[i].toString());

    b.appendChild(text);
    section.appendChild(b);
    element.appendChild(section);
  }
}


/**
 * Populates the courses under each section year the user has taken.
 * @param jsonData
 * @param sectionType
 * @param postPath
 * @param forWhat
 */
function populateSubsections(jsonData, sectionType, postPath, forWhat) {

  var p;
  var button;
  var img;
  var div;
  var text;

  // for each course
  for (var i in jsonData) {
    // create p element, style for indentation
    p = document.createElement("p");
    p.setAttribute("style", "margin-left: 40px;font-size:18px;");

    // get year section it should be under
    section = document.getElementById(jsonData[i][sectionType].toString());

    // button
    button = document.createElement("button");
    // set button id to course id
    button.setAttribute("id", jsonData[i]["id"]);
    button.setAttribute("onclick", "removeCourse(this.id, '" + postPath + "')");
    button.setAttribute("style", "background-color:#FFFFFFFF;display:inline;");
    button.setAttribute("alt", "Delete Course");
    button.setAttribute("title", "delete course");

    img = document.createElement("img");
    img.setAttribute("src", "../static/img/delete.png");

    // append remove image to button
    button.appendChild(img);
    
    div = document.createElement("div");
    div.setAttribute("id", "text" + jsonData[i]["id"]);
    div.setAttribute("style", "display:inline;");

    // if for courses
    if (forWhat == "courses") {
      // create text and line break
      text = document.createTextNode(jsonData[i]["name"] + ": " + jsonData[i]['semester'] + " Semester");
    // if for areas of interest
    } else if (forWhat == "aois") {
      text = document.createTextNode(jsonData[i]["name"] + ": " + jsonData[i]['year']);
    }

    div.appendChild(text);

    br = document.createElement("br");

    // append to paragraph element
    p.appendChild(button);
    p.appendChild(div);
    p.appendChild(br);

    // append to section
    section.appendChild(p);
  }
}


/*
 * Posts removal of specified ID
 * Removes element with the specified ID from the frontend and all corresponding visuals
 * @param delID
 * @param postPath
 */
function removeCourse(delID, postPath) {
  // post to backend
  $.post(postPath, {
      id: delID
  });

  // get button and tect associated with ID
  var button = document.getElementById(delID);
  var text = document.getElementById("text" + delID);

  // remove both from their parent elements
  button.parentElement.removeChild(button);
  text.parentElement.removeChild(text);
}

