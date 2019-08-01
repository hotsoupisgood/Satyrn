$(document).ready(function(){
	var socket = io();
	socket.on('connect', function() {
//        	socket.emit('connect', {data: 'I\'m connected!'});
        });
	socket.on('reload', function() {
		location.reload();
	});
});
