vm={}
document.addEventListener("DOMContentLoaded", function(){
	cells={}
	vm=new Vue({
		el: '#app',
		data: {
			cells:cells,
			spinnerHtml:'<div class="lds-grid"></div>'

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
			vm.cells[i]['image']='<img src="data:image/png;base64, '+out['image/png']+'" />'
			if(vm.cells[i].stderr=='None'){
				vm.cells[i].stderr=out.stderr
				vm.cells[i].changed=false
			}
			if(vm.cells[i].stdout=='None'){
				vm.cells[i].stdout=out.stdout
				vm.cells[i].changed=false
			}
		}
			
	});
});
