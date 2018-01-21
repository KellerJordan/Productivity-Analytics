


function getAllURLS() {
	console.log("Getting all URLs..");
	
	var urls = [];
	var scripts = document.getElementsByTagName("script");
	var links = document.links;
	var img_src = document.getElementsByTagName("img");

	for (var i = 0; i < scripts.length; i++)
	 	if (scripts[i].src) urls.push(scripts[i].src);
   
    for (var i = 0; i < links.length; i++)
   		if (links[i].href) urls.push(links[i].href);

   	for (var i = 0; i < img_src.length; i++)
   		if (img_src[i].src) urls.push(img_src[i].src);

	checkURLS(urls);
	   
}

function checkURLS(urls) {
	console.log("Checking.. " );

	var myJson = JSON.stringify(urls);

	var xhttp = new XMLHttpRequest();
  	xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.responseText);
      if (this.responseText != null)
      	blockURLS(this.responseText);
    }
  };

  xhttp.open("POST", "http://127.0.0.1:8000/inspect/", myJson, true); /* Test endpoint */
  xhttp.send();
}

function blockURLS(urls) {
	console.log("Blocking..");
}


window.addEventListener("load", function(){

    console.log("On Load..");
    getAllURLS();
});



