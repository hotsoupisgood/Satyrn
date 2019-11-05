vm={}
document.addEventListener("DOMContentLoaded", function(){
	cells={}
	vm=new Vue({
		el: '#app',
		data: {
			cells:cells,
		},
		delimiters: ['[[',']]']
	})
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
	socket.on('check complete', function() {
		socket.emit('checkOnUpdate')
	});
	socket.on('showLoading', function(newCells) {
		console.log(newCells);
		vm.cells=newCells
	});
	socket.on('showOutput', function(newOutput) {
		console.log(vm.cells)
		for (var i in vm.cells){
			out=newOutput.shift()
			console.log(out)
			if(vm.cells[i].stderr=='none'&&vm.cells[i].stdout=='none'){
				vm.cells[i].stdout=out.stdout
				vm.cells[i].stderr=out.stderr
			}
		}
			
	});
});
