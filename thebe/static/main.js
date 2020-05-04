vm={}
document.addEventListener("DOMContentLoaded", function(){
	messages = []
	cells = {}
	vm=new Vue({
		el: '#app',
		data: {
			cells: cells,
			messages: messages,
			loading: 'none',
			spinnerHtml: '<div class="lds-grid"></div>'
		},
		delimiters: ['[[',']]'],
		updated: function () {
			this.$nextTick(function () {
				hljs.initHighlighting()
			})
		}
	})
	var socket = io();
	socket.on('connect', function() {
		console.log('Connected to server');
        });
	socket.on('disconnect', function() {
		console.log('Disconnected to server');
        });
	socket.on('message', function(message) {
		messages.push(message)
	});
	socket.on('loading', function(loading) {
		vm.loading = loading
	})
	socket.on('flash', function() {
		messages.push('Cannot run new cells while old cells are still running...')
	});
	socket.on('ping client', function() {
		socket.emit('check if saved')
	});
	socket.on('show output', function(newOutput) {
		for (var i in vm.cells){
			out=newOutput.shift()
			vm.cells[i].changed=false
			vm.cells[i].stderr=out.stderr
			vm.cells[i].stdout=out.stdout
			vm.cells[i]['image/png']=out['image/png']
		}
	});
	socket.on('show all', function(cellList) {
		vm.cells = cellList
		vm.loading = 'none'
	});
});
