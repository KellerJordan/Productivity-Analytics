


function getAllURLS() {
	console.log("Getting all URLs..");
	
	var scripts = document.getElementsByTagName("script");

	for (var i = 0; i < scripts.length; i++) {
     if (scripts[i].src) console.log(i,scripts[i].src)
  }
	blockURL(scripts);
	   
}

function blockURL(urls) {
	console.log("Blocking.. " );

	var myJson = JSON.stringify(urls);

	var xhttp = new XMLHttpRequest();
  	xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.responseText);
    }
  };

  xhttp.open("POST", "http://127.0.0.1:8000/inspect/", myJson, true); /* Test endpoint */
  xhttp.send();
}

window.addEventListener("load", function(){

    console.log("On Load..");
    getAllURLS();
});



