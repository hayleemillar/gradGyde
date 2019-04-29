
/**
 * Populates the sections of the course history according to year.
 * @param elementID
 * @param courses
 */
function populateSections(elementID, jsonData, sectionType, boolSort) {
  var sections = [];

  // for each course
  for (var i in jsonData) {
    // if year course was offered not in array, push
    if (!(sections.includes(jsonData[i][sectionType]))) {
      sections.push(jsonData[i][sectionType]);
    }
  }

  if (boolSort == true) {
    // sort years in descending order
    sections.sort();
  }

  // get element sections will be appended to
  var element = document.getElementById(elementID);
  var section;
  var text;
  var b;

  for (var i in sections) {
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
 * @param courses
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

    // text = document.createTextNode("remove");
    button.appendChild(img);
    
    div = document.createElement("div");
    div.setAttribute("id", "text" + jsonData[i]["id"]);
    div.setAttribute("style", "display:inline;");

    if (forWhat == "courses") {
      // create text and line break
      text = document.createTextNode(jsonData[i]["name"] + ": " + jsonData[i]['semester'] + " Semester");
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



function removeCourse(delID, postPath) {
  $.post(postPath, {
      id: delID
  });

  var button = document.getElementById(delID);
  var text = document.getElementById("text" + delID);

  button.parentElement.removeChild(button);
  text.parentElement.removeChild(text);
}
