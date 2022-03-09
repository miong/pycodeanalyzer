var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on( 'fileAnalyzedChange', function( msg ) {
    const div = document.getElementById('AnalyzedFile');
    div.innerHTML = 'Analyzing : '+msg.file
})

socket.on( 'analysisCompleted', function( msg ) {
    window.location.href = "./home"
})
