var speaker = new window.SpeechSynthesisUtterance();
var speakTimer, stopTimer;
var play = false;
var isStart = false;
// 开始朗读
function speakText() {
	if (!isStart) {
		var context = document.getElementById('content');
		clearTimeout(speakTimer);
		window.speechSynthesis.cancel();
		speakTimer = setTimeout(function() {
			speaker.volume = 0.9
			speaker.text = context.innerHTML;
			window.speechSynthesis.speak(speaker);
		}, 200);
		isStart = true;
		play = true;
		document.getElementById('sayer').className = "glyphicon glyphicon-pause";
	} else {
		if (!play) {
			window.speechSynthesis.resume();
			play = true;
			document.getElementById('sayer').className = "glyphicon glyphicon-pause";
		} else {
			window.speechSynthesis.pause();
			play = false;
			document.getElementById('sayer').className = "glyphicon glyphicon-play";
		}
	}

}
// 停止朗读
function stopSpeak() {
	clearTimeout(stopTimer);
	clearTimeout(speakTimer);
	stopTimer = setTimeout(function() {
		window.speechSynthesis.cancel();
	}, 20);
}