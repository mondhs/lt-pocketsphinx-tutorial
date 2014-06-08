'use strict';

var RecognitionManager = function() {
	/**
	 * Comes from AudioContextMonkeyPatch.js
	 */
	this.audioContext = null;
	this.inputPoint = null
	this.realAudioInput = null
	this.audioInput = null
	RecognitionManager.audioRecorder = null;
	RecognitionManager.callbackMap =null;
	this.state = "down";
	RecognitionManager.hostUrl = './api/recognize/stream/undefined/undefined';

	this.setRecognitionUrl = function(hostUrl) {
		console.log("Changing to host: " + hostUrl);
		RecognitionManager.hostUrl = hostUrl;
	}

	
	this.changeCallbacks = function(callbackMap) {
		RecognitionManager.callbackMap = callbackMap;
	}
	

	/**
	 * 
	 */
	this.prepareRecording = function() {
		if (!navigator.getUserMedia)
			navigator.getUserMedia = navigator.webkitGetUserMedia
					|| navigator.mozGetUserMedia;
		if (!navigator.cancelAnimationFrame)
			navigator.cancelAnimationFrame = navigator.webkitCancelAnimationFrame
					|| navigator.mozCancelAnimationFrame;
		if (!navigator.requestAnimationFrame)
			navigator.requestAnimationFrame = navigator.webkitRequestAnimationFrame
					|| navigator.mozRequestAnimationFrame;

		navigator.getUserMedia({
			audio : true
		}, this.startUserMedia, function(e) {
			alert('Error getting audio');
			console.log(e);
		});
	}
	/**
	 * 
	 */
	this.startUserMedia = function(stream) {
		this.audioContext = new AudioContext()
		console.log('Input connected to audio context destination. audioContext.sampleRate: ' + this.audioContext.sampleRate);
		this.inputPoint = this.audioContext.createGain();
		this.realAudioInput = this.audioContext.createMediaStreamSource(stream);
		this.audioInput = this.realAudioInput;
		this.audioInput.connect(this.inputPoint);
		

		RecognitionManager.audioRecorder = new Recorder(this.inputPoint);

		var zeroGain = this.audioContext.createGain();
		zeroGain.gain.value = 0.0;
		this.inputPoint.connect(zeroGain);
		zeroGain.connect(this.audioContext.destination);

		this.state = "waiting";
		console.log('Recorder initialised.' + RecognitionManager.audioRecorder);
		RecognitionManager.invokeCallback("onPrepared");
	}
	/**
	 * 
	 */
	this.startRecording = function() {
		if (!RecognitionManager.audioRecorder) {
			console.log('Error... audio recorder not initialized');
			RecognitionManager.invokeCallback("onError","ERR_NOT_INIT_AURIO_RECORDER");
			return;
		}
		this.state = "recording";
		console.log('starting record...' + RecognitionManager.audioRecorder);
		RecognitionManager.audioRecorder.clear();
		RecognitionManager.audioRecorder.record();
		console.log('Recording...' + this.state);
		RecognitionManager.invokeCallback("onStartRecording");
	}
	/**
	 * 
	 */
	this.stopRecording = function() {
		if (!RecognitionManager.audioRecorder) {
			console.log('Error... audio recorder not initialized');
			RecognitionManager.invokeCallback("onError","ERR_NOT_INIT_AURIO_RECORDER");
			return;
		}
		console.log('Stopped recording.' + RecognitionManager.audioRecorder);
		RecognitionManager.invokeCallback("onStopRecording");
		RecognitionManager.audioRecorder.stop();
		// create WAV download link using audio data blob
		RecognitionManager.audioRecorder
				&& RecognitionManager.audioRecorder.exportMonoWAV(function(blob) {
					RecognitionManager.invokeCallback("onSendForRecognition");
					RecognitionManager.uploadForRecognition(blob);
				});
		this.state = "waiting";
		
	}
	/**
	 * 
	 */
	RecognitionManager.uploadForRecognition = function(soundBlob) {
		console.log("requesting server to process: "
				+ RecognitionManager.hostUrl);

		var fd = new FormData();
		fd.append('wavfile', soundBlob);
		var recognizerUrl = RecognitionManager.hostUrl;
		
		$.ajax({
			url : recognizerUrl,
			data : fd,
			cache : false,
			async : false,
			contentType : false,
			processData : false,
			type : 'PUT',
			success : function(data) {
				console.log("Retrieved: " + JSON.stringify(data));
				RecognitionManager.invokeCallback("onRecognitionResults", data);
			},
			error: function(jqXHR, textStatus, errorThrown) {
				console.log(textStatus, errorThrown);
			}
		});
	}

	RecognitionManager.invokeCallback = function(callbackName, msg) {
		if(RecognitionManager.callbackMap && typeof RecognitionManager.callbackMap[callbackName] === "function"){
			console.log("invokeCallback: " + callbackName + "; msg: " + msg);
			RecognitionManager.callbackMap[callbackName](msg);
		}else{
			console.log("invokeCallback: cannot find" + callbackName);
		}
	}
}
