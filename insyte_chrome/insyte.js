


function getAllURLS() {
	console.log("Getting all URLs..");
	
	var scripts = document.getElementsByTagName("script");

	for (var i = 0; i < scripts.length; i++) {
     if (scripts[i].src) console.log(i,scripts[i].src)
  }
	blockURL("hello");
	   
}

function blockURL(url) {
	console.log("Blocking.. " + url);
	var xhttp = new XMLHttpRequest();
  	xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.responseText);
    }
  };

  xhttp.open("GET", "https://httpbin.org/get", true); /* Test endpoint */
  xhttp.send();
}

window.addEventListener("load", function(){

    console.log("On Load..");
    getAllURLS();
});



