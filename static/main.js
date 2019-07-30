$(document).ready(function(){
//	var socket = io.connect('http://192.168.1.7:5001');
	var socket = io();
//	var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
//   	var socket = io.connect('http://localhost:5000');
	socket.on('connect', function() {
        	socket.emit('my event', {data: 'I\'m connected!'});
		console.log('reload')
        });
	socket.on('reload', function(msg) {
        $('#log').append('<p>Received: ' + msg.data + '</p>');
		location.reload();
	});
});
