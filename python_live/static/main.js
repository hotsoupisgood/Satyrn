
function showLoading(cellHash){
	$('#'+cellHash).replaceWith('<div class="lds-roller"></div>')
}
$(document).ready(function(){
	var socket = io();
	function myCallback() {
		socket.emit('checkOnUpdate')
	 }
	socket.on('connect', function() {
		console.log('Connected to server');
		socket.emit('checkOnUpdate')
        });
	socket.on('disconnect', function() {
		console.log('Disconnected to server');
        });
	socket.on('check complete', function(cell) {
		if(cells) {
			for (var cell in cells) {
				showLoading(cell('hash'))
			}
		} else {
			socket.emit('checkOnUpdate')
		}
	});
	socket.on('reload', function() {
		location.reload();
	});
	socket.on('showLoading', function(cellToLoad) {
		
	});
	socket.on('newCell', function(cellToRun) {
		
	});
	socket.on('deleteCell', function(cellToDelete) {
		
	});
	socket.on('newOutput', function(output) {
		
	});
});
