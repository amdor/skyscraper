/**
 *addEvent function for crossplatform add event capability
 */
function addEvent(elem, evnt, func) { //http://stackoverflow.com/questions/6927637/addeventlistener-in-internet-explorer
   if (elem.addEventListener)  // W3C DOM
      elem.addEventListener(evnt,func,false);
   else if (elem.attachEvent) { // IE DOM
      elem.attachEvent("on"+evnt, func);
   }
   else { // No much to do
      elem[evnt] = func;
   }
}

var inputUriCount = 0;
var sendButton = null;
var inputContainerDiv = null;
var textDivTemplate = null;

function windowLoaded(event) {
    sendButton = document.getElementById("sendButton");
    
    //creating the div that'll contain all input fields
    var textDiv = document.createElement("DIV");
    textDiv.className = "inputTextDiv";
    textDiv.id = "uriArray"+inputUriCount;
    textDiv.innerHTML = "hasznaltauto.hu url:";
    
    //textfield that asks for a car uri
    var textField = document.createElement("INPUT");
    textField.id = "uriInput"+inputUriCount;
    textField.type = "text";
    textField.name = "uri"+inputUriCount;
    
    //add a new input field, or remove current
    var anchorButtonPlus = document.createElement("A");
    anchorButtonPlus.setAttribute("href", "#");
    anchorButtonPlus.className = "roundButton";
    
    var anchorButtonMinus = anchorButtonPlus.cloneNode();
    
    anchorButtonPlus.innerHTML = "+";
    anchorButtonMinus.innerHTML = "-";
    
    textDiv.appendChild(textField);
    textDiv.appendChild(anchorButtonPlus);
    textDiv.appendChild(anchorButtonMinus);
    inputContainerDiv = document.getElementById("inputContainerID");
    inputContainerDiv.insertBefore(textDiv, sendButton);
    
    addEvent(inputContainerDiv,"click", addTextDiv);
    addEvent(inputContainerDiv,"click", deleteTextDiv);
     
    textDivTemplate = textDiv.cloneNode(true); //clone it to avoid inheriting further modifications needed for the first row only
    inputUriCount++;
    
    //for the first  row hide minus button
    anchorButtonMinus.style.display = "none";
    
}

/**
 *Eventlistener listens only to roundbuttons that are containing +
 *their parent's parent div is the event listener target.
 *We add a new div with the input fields from the template
*/
function addTextDiv(event) {
    if (event.target.className === "roundButton" && event.target.innerHTML === "+") {
        var newTextDiv = textDivTemplate.cloneNode(true);
        newTextDiv.getElementsByTagName("INPUT");
        inputContainerDiv.insertBefore(newTextDiv, sendButton);
        inputUriCount++;
    }
    event.stopPropagation();
}

/**
 *Eventlistener listens only to roundbuttons that are containing -
 *their parent div is the event listener target.
 *Removes inputfields next to the clicked minus button.
 */
function deleteTextDiv(event) {
    if (event.target.className === "roundButton" && event.target.innerHTML === "-") {
        inputContainerDiv.removeChild(event.target.parentNode);
        inputUriCount--;
    }
    event.stopPropagation();
}