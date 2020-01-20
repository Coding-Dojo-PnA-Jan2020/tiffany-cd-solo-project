var addButton = document.querySelector(".add-new-step");

var cookingInstructionsContainer = document.querySelector(".cooking-instructions");

// var something = "<p>more yay</p>";

var something = document.createElement("p");

var somethingElse = document.createTextNode("more yay");

var ccc = something.appendChild(somethingElse);

function addStep() {
  console.log("yay");
}

addButton.addEventListener("click", function (){
  console.log("clickety click");
  var lastKnownStep = document.querySelector
  cookingInstructionsContainer.appendChild(ccc);
})
