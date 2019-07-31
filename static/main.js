$(document).ready(function(){
	var socket = io();
	socket.on('connect', function() {
        	socket.emit('my event', {data: 'I\'m connected!'});
		console.log('reload')
        });
	socket.on('reload', function() {
		location.reload();
	});
});
