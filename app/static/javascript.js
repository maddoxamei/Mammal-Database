function clone(filename){
  var link = document.querySelector('link[rel="import"]');
  var content = link.import;

  // Grab DOM from warning.html's document.
  var el = content.querySelector('.'+filename);

  document.body.appendChild(el.cloneNode(true));
}

function init(){
  alert("RWAR");
}

function loadHTML(id, filename){
  document.getElementById(id).load(filename+".html"); //$ = document.getElementById
}
