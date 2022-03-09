var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on( 'connect', function() {
    console.log("fetchStats sent")
    socket.emit('fetchStats', {
        data: 'request stats'
    })
})

socket.on( 'statsChange', function( msg ) {
    const spanFiles = document.getElementById('nbFiles');
    const spanClasses = document.getElementById('nbClasses');
    const spanEnums = document.getElementById('nbEnums');
    const spanFunctions = document.getElementById('nbFunctions');
    const spanDuration = document.getElementById('duration');
    spanFiles.innerHTML = msg.nbFiles
    spanClasses.innerHTML = msg.nbClasses
    spanEnums.innerHTML = msg.nbEnums
    spanFunctions.innerHTML = msg.nbFunctions
    spanDuration.innerHTML = msg.duration
})
