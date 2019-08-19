$(document).ready(function(){
	var socket = io();
//	var intervalID = int()
	function myCallback() {
		socket.emit('checkOnUpdate')
	 }
	socket.on('connect', function() {
		console.log('Connected to server');
		socket.emit('checkOnUpdate')
//		intervalID=window.setInterval(myCallback, 1000);
        });
	socket.on('disconnect', function() {
		console.log('Disconnected to server');
//		window.clearInterval(intervalID)
        });
	socket.on('check complete', function(reload) {
		if(reload) {
			location.reload();
		}else {
			socket.emit('checkOnUpdate')
		}
	});
	socket.on('reload', function() {
		location.reload();
	});
});
