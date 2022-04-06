/* global io, mermaid */

const socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', () => {
	console.log('fetchStats sent');
	socket.emit('fetchStats', {
		data: 'request stats',
	});
});

socket.on('statsChange', msg => {
	const spanFiles = document.getElementById('nbFiles');
	const spanClasses = document.getElementById('nbClasses');
	const spanEnums = document.getElementById('nbEnums');
	const spanFunctions = document.getElementById('nbFunctions');
	const spanDuration = document.getElementById('duration');
	const languagePieDiag = document.getElementById('LanguagePieDiag');
	spanFiles.innerHTML = msg.nbFiles;
	spanClasses.innerHTML = msg.nbClasses;
	spanEnums.innerHTML = msg.nbEnums;
	spanFunctions.innerHTML = msg.nbFunctions;
	spanDuration.innerHTML = msg.duration;
	languagePieDiag.innerHTML = msg.languagePie;
	console.log(msg.languagePie);

	languagePieDiag.removeAttribute('data-processed');
	const insert = function (code) {
		languagePieDiag.innerHTML = code;
	};

	mermaid.render('preparedScheme', msg.languagePie, insert);
});

const config = {
	startOnLoad: true,
	securityLevel: 'loose',
};
mermaid.initialize(config);
