$(document).ready(function(){
	var socket = io();
	var intervalID = window.setInterval(myCallback, 500);

	function myCallback() {
		socket.emit('checkOnUpdate')
	 }
	socket.on('connect', function() {
		console.log('Connected to server');
        });
	socket.on('disconnect', function() {
		console.log('Disconnected to server');
        });
	socket.on('reload', function() {
		location.reload();
	});
});
