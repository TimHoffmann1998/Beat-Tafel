let context = new AudioContext();
let gainNode = context.createGain();
gainNode.gain.value = 0.5;
gainNode.connect(context.destination);

let bpm = 90;
let achtel = (60/bpm)*4/8;
let gain = 0;

var audioBuffers = [];
var takt = [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]
var taktpreload = [[],[],[],[]]

let lookahead = 25.0; // How frequently to call scheduling function (in milliseconds)
let scheduleAheadTime = 0.1; // How far ahead to schedule audio (sec)

let currentNote = 0;
let nextNoteTime = 0.0; // when the next note is due.

const gainSlider = document.querySelector('#gainSlider');
const gainOutput = document.querySelector('#gainOutput');
const bpmSlider = document.querySelector('#bpmSlider');
const bpmOutput = document.querySelector('#bpmOutput');
bpmOutput.innerHTML = bpmSlider.value;
gainOutput.innerHTML = gainSlider.value;

bpmSlider.addEventListener('input', function() {
    bpm = Number(this.value);
    bpmOutput.innerHTML = bpm + " bpm";
}, false);

gainSlider.addEventListener('input', function() {
    gain = Number(this.value);
    document.querySelector("#gainOutput").innerHTML = (this.value) + " dB";
}, false);

for (let i = 0; i <= 3; i++){
    getAudioData(i, document.querySelector('#drumtype').value);
}

function getAudioData(i, drumtype) {
    fetch("DRUMS/" + drumtype + "/" + drumtype + (i + 1) + ".wav")
    .then(response => response.arrayBuffer())
    .then(undecodedAudio => context.decodeAudioData(undecodedAudio))
    .then(audioBuffer => {
        audioBuffers[i] = audioBuffer;
    })
    .catch(console.error);
}

document.querySelector('#drumtype').addEventListener('click', function(){
    for (let i = 0; i <= 3; i++){
        getAudioData(i, this.value);
    }
})

function playSound(buffer, time) {
    let source = context.createBufferSource();
    source.buffer = buffer;
    source.connect(gainNode);
    source.start(time);
}

function nextNote() {
    const secondsPerBeat = 60.0 / bpm;

    nextNoteTime += secondsPerBeat/2; // Add beat length to last beat time

    // Advance the beat number, wrap to zero
    currentNote++;
    if (currentNote === 15) {
            currentNote = 0;
    }
}

function  updateGrid(Note, feldnr){
    id = "block" + (feldnr + 1);

    if (Note = 15){
        document.getElementById(id).style.backgroundColor = "red";
    }
    else if (Note = 4){
        document.getElementById(id).style.backgroundColor = "yellow";
    }
    else if (Note = 8){
        document.getElementById(id).style.backgroundColor = "magenta";
    }
    else if (Note = 1){
        document.getElementById(id).style.backgroundColor = "green";
    }
    else if (Note = 10){
        document.getElementById(id).style.backgroundColor = "cyan";
    }
}


function scheduleNote(beatNumber, time) {
    

    if (takt[0][currentNote] === 1) {
        playSound(audioBuffers[0], time)
    }
    if (takt[1][currentNote] === 1) {
        playSound(audioBuffers[1], time)
    }
    if (takt[2][currentNote] === 1) {
        playSound(audioBuffers[2], time)
    }
    if (takt[3][currentNote] === 1) {
        playSound(audioBuffers[3], time)
    }
}

function scheduler() {
    // while there are notes that will need to play before the next interval, schedule them and advance the pointer.
    while (nextNoteTime < context.currentTime + scheduleAheadTime && isPlaying) {
        scheduleNote(currentNote, nextNoteTime);
        nextNote();
    }
    timerID = window.setTimeout(scheduler, lookahead);
}


let isPlaying = false;

document.querySelector("#playButton").addEventListener("click", function(){
        isPlaying = !isPlaying;
        if (isPlaying){
            this.innerHTML = "Stop";
            currentNote = 0;
            document.getElementById('playButton').style.backgroundImage = 'url(stopbutton.png)';
            nextNoteTime = context.currentTime;
            scheduler(); // kick off scheduling
        }    
        else{
            this.innerHTML = "Play";
            document.getElementById('playButton').style.backgroundImage = 'url(playbutton.png)';
        }
})


if (navigator.requestMIDIAccess) {
    navigator.requestMIDIAccess({sysex: false}).then(function (midiAccess) {
        midi = midiAccess;
        var inputs = midi.inputs.values();
        // loop through all inputs
        for (var input = inputs.next(); input && !input.done; input = inputs.next()) {
            // listen for midi messages
            input.value.onmidimessage = onMIDIMessage;
        }
    });
} else {
    alert("No MIDI support in your browser.");
}

function dec2bin(dec){
    bin = (dec >>> 0).toString(2);
    ///console.log(bin)
    while (bin.length < 4){
        bin = 0 + bin 
    }
    ///console.log(bin)
    return bin
}

counter = 0

function onMIDIMessage(event) {
    document.querySelector("#test").innerHTML = event.data[2];
    if (event.data[2] == 127){
        counter = 0;      
    };
    if (counter <= 15 && event.data[2] != 127) {
        for (i = 0; i < 4; i++){
            taktpreload[Math.floor(counter/4)].push(parseInt(dec2bin(event.data[2])[i], 10));
        }
        updateGrid(event.data[2], counter);
        counter += 1;
    };

    if (counter == 16){
        takt = taktpreload;
        console.log(takt);
        taktpreload = [[],[],[],[]];
    };
};