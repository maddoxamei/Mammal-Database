function clone(filename){
  var link = document.querySelector('link[rel="import"]');
  var content = link.import;

  // Grab DOM from warning.html's document.
  var el = content.querySelector('.'+filename);

  document.body.appendChild(el.cloneNode(true));
}

document.addEventListener('DOMContentLoaded', init, false);

function init(){
  //loadHTML("header", "header");
}

function loadHTML(id, filename){
  var html = document.createTextNode();
  document.getElementById(id).appendChild(html);
  document.getElementById(id).innerHTML='<object type="text/html" data="'+filename+'" ></object>';
  alert(document.getElementById(id).innerHTML);
}

function importHTML(obj){
  var total = (obj.contentDocument.body||obj.contentDocument).children.length;
  var element, clone;
  for (var i = 0; i < total; i++){
    element = (obj.contentDocument.body||obj.contentDocument).children[i];
    clone = document.createElement(element.tagName);
    clone.innerHTML = element.innerHTML;
    document.getElementById("header").appendChild(clone);
  }
  obj.remove();
}
