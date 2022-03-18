/* global io */

const socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('fileAnalyzedChange', msg => {
	const div = document.getElementById('AnalyzedFile');
	div.innerHTML = 'Analyzing : ' + msg.file;
});

socket.on('analysisCompleted', _ => {
	window.location.href = './home';
});
