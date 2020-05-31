vm={}
document.addEventListener("DOMContentLoaded", function(){

	// Initialize socketIO
	var socket = io();

	// Set to true when data is meaningfully added
	dataAdded = false

	// Contains a stream of messages sent from the server
	messages = []

	// A list of sells frequently updated by the server
	cells = {}

	// Initialize the vue instance
	vm=new Vue({
		el: '#app',
		data: {
			cells: cells,
			messages: messages,
			loading: 'none',
		},
		methods:  {
			runAll: function (event) {
				socket.emit('run_all')
			},
			run_cell: function (id) {
				socket.emit('run cell', id)
			},
			reRender() {
				// Re render the latex under certain conditions
				if (window.MathJax && dataAdded) {
					console.log('rendering mathjax');
					// Trigger re render
					window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub], () => console.log('done'));
					// Indicate re render has been begun
					dataAdded = false
				}
			}
		},
		delimiters: ['[[',']]'],
		updated () {
			this.$nextTick(function () {
				this.reRender();
			})
		}
	})
	socket.on('connect', function() {
		console.log('Connected to server');
	});
	socket.on('disconnect', function() {
		console.log('Disconnected to server');
	});
	socket.on('message', function(message) {
		document.title = message
		messages.push(message)
	});
	socket.on('loading', function(loading) {
		vm.loading = loading
	})
	socket.on('stop loading', function() {
		vm.loading = 'none'
	})
	socket.on('flash', function() {
		messages.push('Cannot run new cells while old cells are still running...')
	});
	socket.on('ping client', function() {
		socket.emit('check if saved')
	});
	socket.on('output', function(output) {
		console.log('pushing outs')
		vm.cells[vm.loading]['outputs'].push(output)
	})
	socket.on('plot output', function(output) {
		console.log('pushing outs')
		vm.cells[vm.loading]['outputs'].push(output)
	})
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
		// Replace the current cells with the new ones from the server
		vm.cells = cellList
		// Stop the loading effects
		vm.loading = 'none'
		// Indicate that data was meaningfully added,
		// to trigger a MathJax re render
		dataAdded = true 
	});
});
