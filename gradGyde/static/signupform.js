
function populate_aoc(data) {
	document.getElementById("select_AOC");

	var aoc = {{ aocs|safe }};

	console.log(aoc);

	var aocDouble = {{ doubles|safe }};

	console.log(aocDouble);

	var slash = {{ slashs|safe }};

	console.log(slash);

}