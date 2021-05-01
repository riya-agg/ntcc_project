	function startPlayer(objURL) {
		parent.appletframe.startPlayer(objURL);
	}
	
	function SetClass(event,clazz){
		var source;
		if (!event.target) { source = event.srcElement; } else { source = event.target; }
		if (source.tagName=="TR"||source.tagName=="TABLE")
			return;
		while(source.tagName!="TD") {
			// alert(source.tagName);
			source=source.parentNode;
		}
		source.className=clazz;
	}
	

	function playText(stext) {
		CWASA.playSiGMLText(0, stext);   // line 49382 of allcsa.js
	}

	function setSiGMLURL(sigmlURL) {
		var loc = window.location.href;
		var locDir = loc.substring(0, loc.lastIndexOf('/'));
		// console.log("SiGML: "+sigmlURL);
		// console.log("Location Dir: "+locDir);
		sigmlURL = locDir + "/" + sigmlURL;
		// console.log("URL "+sigmlURL);
		document.getElementById("URLText").value = sigmlURL;
		return sigmlURL;
	}

	function startPlayer(sigmlURL) {
		sigmlURL = setSiGMLURL(sigmlURL);
		// Equivalent to click on Sign button
		CWASA.playSiGMLURL(0, sigmlURL);  // line 49393 of allcsa.js
	}

