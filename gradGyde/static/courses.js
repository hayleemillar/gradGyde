
/**
 * Populates the sections of the course history according to year.
 * @param elementID
 * @param courses
 */
function populateSections(elementID, courses) {
  var years = [];

  // for each course
  for (course in courses) {
    // if year course was offered not in array, push
    if (!(years.includes(courses[course]["year"]))) {
      years.push(courses[course]["year"]);
    }
  }

  // sort years in descending order
  years.sort();

  // get element sections will be appended to
  var element = document.getElementById(elementID);
  var section;
  var text;
  var b;

  for (year in years) {
    section = document.createElement("h4");
    section.setAttribute("id", years[year].toString())
    b = document.createElement("b");
    text = document.createTextNode(years[year].toString());

    b.appendChild(text);
    section.appendChild(b);
    element.appendChild(section);
  }
}


/**
 * Populates the courses under each section year the user has taken.
 * @param courses
 */
function populateCourses(courses) {

  var p;
  var button;
  var img;
  var div;

  // for each course
  for (course in courses) {
    // create p element, style for indentation
    p = document.createElement("p");
    p.setAttribute("style", "margin-left: 40px;font-size:18px;");

    // get year section it should be under
    section = document.getElementById(courses[course]["year"].toString());
    console.log(section);

    // button
    button = document.createElement("button");
    // set button id to course id
    button.setAttribute("id", courses[course]["id"]);
    button.setAttribute("onclick", "removeCourse(this.id)");
    button.setAttribute("style", "background-color:#FFFFFFFF;display:inline;");
    button.setAttribute("alt", "Delete Course");
    button.setAttribute("title", "delete course");

    img = document.createElement("img");
    img.setAttribute("src", "../static/img/delete.png");

    // text = document.createTextNode("remove");
    button.appendChild(img);
    
    div = document.createElement("div");
    div.setAttribute("id", "text" + courses[course]["id"]);
    div.setAttribute("style", "display:inline;");

    // create text and line break
    text = document.createTextNode(courses[course]["name"]);

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



function removeCourse(courseID) {
  $.post("/removecourse", {
      id: courseID
  });

  var button = document.getElementById(courseID);
  var text = document.getElementById("text" + courseID);

  button.parentElement.removeChild(button);
  text.parentElement.removeChild(text);
}
