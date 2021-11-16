var speaker = new SpeechSynthesisUtterance();
const synth = speechSynthesis;
console.log(speaker);
var speakTimer, stopTimer;
var play = false;
var isStart = false;
var arrEntities={'lt':'<','gt':'>','nbsp':' ','amp':'&','quot':'"'}; 
// 开始朗读
function speakText() {
	
	if (!isStart) {
		var context = document.getElementById('content');
		clearTimeout(speakTimer);
		synth.cancel();
		console.log(synth);
		speakTimer = setTimeout(function() {
			var voices=synth.getVoices();
			speaker.volume = 10;
			speaker.voice=voices[16];
			var msg = context.innerHTML.replace(/<\/?[^>]*>/g, ''); //去除HTML Tag
	        msg = msg.replace(/[|]*\n/, ''); //去除行尾空格
			speaker.text = msg.replace(/&(lt|gt|nbsp|amp|quot);/ig,function(all,t){return arrEntities[t];});
			synth.speak(speaker);
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
	document.getElementById('sayer').className = "glyphicon glyphicon-play";
	isStart = false;
	play = false;
	stopTimer = setTimeout(function() {
		window.speechSynthesis.cancel();
	}, 20);
	
}