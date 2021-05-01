// global variable
var final_response = "";
		
function tokenizeEnglish(inText) {
		// loop over the result array and replace space and end of sentence 
		// and store it newString
		
		newString = "";
		for(y = 0; y < inText.length; y++) {
			w = inText[y];
			if(w == " ") // replace space with comma
				newString = newString + ",";
			else 
				newString = newString + w;
		}
		console.log("Processed tokenised string : " + newString);
		return newString;
}
		
		
function FinalText(word, fileName) {
		this.word = word;
		this.fileName = fileName;
}
		
		
function clickme(speech) {
		console.log(speech);
		tokens = [];
		
		// tokenize
		tokens = tokenizeEnglish(speech).split(',');
		
		for(x = 0; x < tokens.length; x++) {
			if(tokens[x] == "")
				tokens.splice(x, 1);
		}
		
		console.log("Tokens Received: ", tokens);
		
		wordArray = [];
		arrayCounter = 0;
		
		//var sigmlList = JSON.parse('../static/sigmlFiles.json'); 
		
		/*$.getJSON("../static/sigmlFiles.json", function(json) {
			sigmlList = JSON.parse(json.data);
		}); */
		console.log("SigmlLength: " + sigmlList.length);
	
		for(x = 0; x < tokens.length; x++) {
			word_found = false;
			for(y = 0; y < sigmlList.length; y++) {
				if(sigmlList[y].name == tokens[x]) {
					// console.log(sigmlList[y].sid);
					wordArray[arrayCounter++] = new FinalText(tokens[x], sigmlList[y].fileName);
					word_found = true;
					break;
				}
			}
			// if word not found then add individual alphabetic signing gestures
			if(word_found == false) {
				wordlen = tokens[x].length;
				for(p = 0; p < wordlen; p++) {
					q = tokens[x][p];
					//q=q.toUpperCase();
					for(k = 0; k < sigmlList.length; k++) {
						if(sigmlList[k].name == q) {
							wordArray[arrayCounter++] = new FinalText(q, sigmlList[k].fileName);
							break;
						}
					}
				}
					max = 0,countit = 0;
					for(k = 0; k < sigmlList.length; k++) {
						countit++;
					if (sigmlList[k].sid > max)
					{ max = sigmlList[k].sid; }
				}
				console.log("maxi is : "+max);
				max = max + 1;
				if(tokens[x] != "EOL"){
					console.log("k is : "+k);
					var obj = {"sid": max, "name": tokens[x], "fileName": tokens[x] + ".sigml"};
						var newdata = JSON.stringify(sigmlList);
					console.log(newdata);
					}
			} // if not word found part ends here
		}
		
		console.log(wordArray);
		console.log(wordArray.length);
		$("#debugger").html(JSON.stringify(wordArray));
			// wordArray object contains the word and corresponding files to be played
		// call the startPlayer on it in syn manner
		totalWords = wordArray.length;
		i = 0;
		var int = setInterval(function () {
											if(i == totalWords) {
												if(playerAvailableToPlay) {
													clearInterval(int);
													finalHint = $("#inputText").val();
													$("#textHint").html(finalHint);
												}
											} else {
												if(playerAvailableToPlay) {
													playerAvailableToPlay = false;
													startPlayer("SignFiles/" + wordArray[i].fileName);
													$("#textHint").html(wordArray[i].word);
													i++;
												}
											}
										}, 3000);
}
	
	
function speak() {
	console.log('Speech input started!');
	if (window.hasOwnProperty('webkitSpeechRecognition')) {
			var recognition = new webkitSpeechRecognition();
			recognition.continuous = false;
			recognition.interimResults = false;
			recognition.lang = "en-US";
			recognition.start();
			recognition.onresult = function(e) {
			var speech = e.results[0][0].transcript;
			
				url = 'http://localhost:5000/parser' + '?speech=' + speech ;
				var anHttpRequest = new XMLHttpRequest();									
				anHttpRequest.onreadystatechange = function() {
														if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200) {
															final_response = JSON.parse(anHttpRequest.responseText);
															document.getElementById('isl').innerHTML = final_response.isl_text_string; 
															document.getElementById('speech_').innerHTML = speech; 
															console.log('Parsed Speech:' , final_response.pre_process_string);
															clickme(final_response.pre_process_string);
															console.log('clickme successful!');
														}
													};
					anHttpRequest.open( "GET", url, true );
				anHttpRequest.send();
				recognition.stop();			
				console.log('End of Speech input!');
			};
			
			recognition.onerror = function(e) {
				recognition.stop();
			}
	}
}