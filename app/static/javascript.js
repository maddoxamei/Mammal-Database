//document.addEventListener('DOMContentLoaded', init, false);
function init(){
  selectManagement(document.getElementById('queryTab'), 'Query')
  //loadHTML("header", "header");
}

function importHTML(obj){
  var total = (obj.contentDocument.body||obj.contentDocument).children.length;
  var element, clone;
  for (var i = 0; i < total; i++){
    element = (obj.contentDocument.body||obj.contentDocument).children[i];
    clone = document.createElement(element.tagName);
    clone.innerHTML = element.innerHTML;
    document.getElementById(obj.getAttribute('data')).appendChild(clone);
  }
  obj.remove();
}

function selectManagement(tab, direction) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(direction).style.display = "block";
  tab.className += " active";
}

function query(){
  alert("querying", document.getElementById('search').value);
}

function update(){
  alert("will update");
}

function add(){
  alert("will add");
}

function remove(){
  alert("will remove");
}
