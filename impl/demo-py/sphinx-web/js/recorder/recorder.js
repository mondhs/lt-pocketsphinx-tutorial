'use strict';

(function(window) {

	var Recorder = function(source, cfg) {
		var recording = false, currCallback;
		var config = cfg || {};
		var bufferLen = config.bufferLen || 4096;
		this.context = source.context;
		if (!this.context.createScriptProcessor) {
			this.node = this.context.createJavaScriptNode(bufferLen, 2, 2);
		} else {
			this.node = this.context.createScriptProcessor(bufferLen, 2, 2);
		}

		var worker = new Worker(getUrlForWorker(RecorderWorkerClass));

		worker.addEventListener('message', function(e) {
			if(e.data.cmd === 'info'){
				console.log('[Message]: info', e.data.context);	
			}else{
				console.log('[Message]: exec: ', e.data, currCallback);
				currCallback(e.data.context);
			}
			
		}, false);

		worker.addEventListener('error', function(e) {
			console.log('[Error]: ', [ 'ERROR: Line ', e.lineno, ' in ',
					e.filename, ': ', e.message ].join(''));
		}, false);

		worker.postMessage({
			command : 'init',
			config : {
				sampleRate : this.context.sampleRate
			}
		});
		

		this.node.onaudioprocess = function(e) {
			if (!recording) {
				return;
			}
			worker.postMessage({
				command : 'record',
				buffer : [ e.inputBuffer.getChannelData(0),
						e.inputBuffer.getChannelData(1) ]
			});
		}

		this.configure = function(cfg) {
			for ( var prop in cfg) {
				if (cfg.hasOwnProperty(prop)) {
					config[prop] = cfg[prop];
				}
			}
		}

		this.record = function() {
			recording = true;
		}

		this.stop = function() {
			recording = false;
		}

		this.clear = function() {
			worker.postMessage({
				command : 'clear'
			});
		}

		this.getBuffers = function(cb) {
			currCallback = cb || config.callback;
			worker.postMessage({
				command : 'getBuffers'
			})
		}

		this.exportWAV = function(cb, type) {
			currCallback = cb || config.callback;
			type = type || config.type || 'audio/wav';
			if (!currCallback) {
				throw new Error('Callback not set');
			}
			worker.postMessage({
				command : 'exportWAV',
				type : type
			});
		}

		this.exportMonoWAV = function(cb, type) {
			currCallback = cb || config.callback;
			type = type || config.type || 'audio/wav';
			if (!currCallback) {
				throw new Error('Callback not set');
			}
			worker.postMessage({
				command : 'exportMonoWAV',
				type : type
			});
		}


		source.connect(this.node);
		this.node.connect(this.context.destination); // this should not be
		// necessary
	};

	Recorder.forceDownload = function(blob, filename) {
		var url = (window.URL || window.webkitURL).createObjectURL(blob);
		var link = window.document.createElement('a');
		link.href = url;
		link.download = filename || 'output.wav';
		var click = document.createEvent("Event");
		click.initEvent("click", true, true);
		link.dispatchEvent(click);
	}

	window.Recorder = Recorder;

})(window);

/**
 * function that allows use local function as worker function
 * 
 * @param workerFunction
 * @returns
 */
function getUrlForWorker(workerFunction) {
	var BlobBuilder = window.BlobBuilder || window.MozBlobBuilder
			|| window.WebKitBlobBuilder || window.BlobBuilder;
	var URL = window.URL || window.webkitURL;
	var mainString = workerFunction.toString();
	var bodyString = mainString.substring(mainString.indexOf("{") + 1,
			mainString.lastIndexOf("}"));
	var blob = new Blob([ bodyString ], {
		type : 'javascript/worker'
	});
	return URL.createObjectURL(blob);
}
/**
 * RecorderWorkerClass - Web Worker for actual recording and storage operations
 */
function RecorderWorkerClass() {
	var recLength = 0, recBuffersL = [], recBuffersR = [], sampleRate;
	self.onmessage = function(e) {
		switch (e.data.command) {
		case 'init':
			init(e.data.config);
			break;
		case 'record':
			record(e.data.buffer);
			break;
		case 'exportWAV':
			exportWAV(e.data.type);
			break;
		case 'exportMonoWAV':
			exportMonoWAV(e.data.type);
			break;
		case 'getBuffers':
			getBuffers();
			break;
		case 'clear':
			clear();
			break;
		}
	}
	self.init = function(config) {
		postMessage({
			cmd : "info",
			context : "RecorderWorkerClass class init : " + config.sampleRate
		});
		sampleRate = config.sampleRate;
	}
	self.record = function(inputBuffer) {
		// postMessage("RecorderWorkerClass class record");
		recBuffersL.push(inputBuffer[0]);
		recBuffersR.push(inputBuffer[1]);
		recLength += inputBuffer[0].length;
	}

	self.exportWAV = function(type) {
		postMessage({
			cmd : "info",
			context : "RecorderWorkerClass class export Wav: " + type
		});
		var bufferL = mergeBuffers(recBuffersL, recLength);
		var bufferR = mergeBuffers(recBuffersR, recLength);
		var interleaved = interleave(bufferL, bufferR);
		var dataview = encodeWAV(interleaved);
		var audioBlob = new Blob([ dataview ], {
			type : type
		});
		postMessage({
			cmd : "exportWAV",
			context : audioBlob
		});
	}

	self.exportMonoWAV = function(type) {
		postMessage({
			cmd : "info",
			context : "RecorderWorkerClass export Mono Wav : " + type
		});
		var bufferL = mergeBuffers(recBuffersL, recLength);
		var dataview = encodeWAV(bufferL, true);
		var audioBlob = new Blob([ dataview ], {
			type : type
		});

		postMessage({
			cmd : "exportMonoWAV",
			context : audioBlob
		});
	}

	self.getBuffers = function() {
		postMessage({
			cmd : "info",
			context : "RecorderWorkerClass export getBuffers " 
		});
		var buffers = [];
		buffers.push(mergeBuffers(recBuffersL, recLength));
		buffers.push(mergeBuffers(recBuffersR, recLength));
		postMessage(buffers);
	}

	self.clear = function() {
		postMessage({
			cmd : "info",
			context : "RecorderWorkerClass class clear : "
		});
		recLength = 0;
		recBuffersL = [];
		recBuffersR = [];
	}

	self.mergeBuffers = function(recBuffers, recLength) {
		postMessage({
			cmd : "info",
			context : "RecorderWorkerClass class mergeBuffers : "+recLength
		});
		var result = new Float32Array(recLength);
		var offset = 0;
		for ( var i = 0; i < recBuffers.length; i++) {
			result.set(recBuffers[i], offset);
			offset += recBuffers[i].length;
		}
		return result;
	}

	self.interleave = function(inputL, inputR) {
		postMessage({
			cmd : "info",
			context : "RecorderWorkerClass class interleave : "+inputL.length
		});
		var length = inputL.length + inputR.length;
		var result = new Float32Array(length);

		var index = 0, inputIndex = 0;

		while (index < length) {
			result[index++] = inputL[inputIndex];
			result[index++] = inputR[inputIndex];
			inputIndex++;
		}
		return result;
	}

	self.floatTo16BitPCM = function(output, offset, input) {
		for ( var i = 0; i < input.length; i++, offset += 2) {
			var s = Math.max(-1, Math.min(1, input[i]));
			output.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
		}
	}

	self.writeString = function(view, offset, string) {
		for ( var i = 0; i < string.length; i++) {
			view.setUint8(offset + i, string.charCodeAt(i));
		}
	}

	self.encodeWAV = function(samples, mono) {
		var buffer = new ArrayBuffer(44 + samples.length * 2);
		var view = new DataView(buffer);

		/* RIFF identifier */
		writeString(view, 0, 'RIFF');
		/* file length */
		view.setUint32(4, 32 + samples.length * 2, true);
		/* RIFF type */
		writeString(view, 8, 'WAVE');
		/* format chunk identifier */
		writeString(view, 12, 'fmt ');
		/* format chunk length */
		view.setUint32(16, 16, true);
		/* sample format (raw) */
		view.setUint16(20, 1, true);
		/* channel count */
		view.setUint16(22, mono ? 1 : 2, true);
		/* sample rate */
		view.setUint32(24, sampleRate, true);
		/* byte rate (sample rate * block align) */
		view.setUint32(28, sampleRate * 4, true);
		/* block align (channel count * bytes per sample) */
		view.setUint16(32, 4, true);
		/* bits per sample */
		view.setUint16(34, 16, true);
		/* data chunk identifier */
		writeString(view, 36, 'data');
		/* data chunk length */
		view.setUint32(40, samples.length * 2, true);

		floatTo16BitPCM(view, 44, samples);

		return view;
	}

}
