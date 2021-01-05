let context = new AudioContext();

let bpm = 90;
let achtel = (60/bpm)*4/8;

var audioBuffers = [];
var takt = [[1,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,0], [1,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,0]]
//var takt = [[0,1,0,1,0,1,0,1], [1,0,0,0,1,0,0,0], [0,0,1,0,0,0,1,0], [1,1,0,0,1,1,0,0]]
var taktb = [[1,0,0,0,1,0,0,0], [0,1,0,1,0,1,0,1], [1,1,0,0,1,1,0,0], [0,0,1,0,0,0,1,0]]
var taktTest = []

const bpmControl = document.querySelector('#bpm');
bpmControl.addEventListener('input', function() {
    bpm = Number(this.value);
}, false);

let lookahead = 25.0; // How frequently to call scheduling function (in milliseconds)
let scheduleAheadTime = 0.1; // How far ahead to schedule audio (sec)

let currentNote = 0;
let nextNoteTime = 0.0; // when the next note is due.


for (let i = 0; i < 3; i++)
    getAudioData(i);


function getAudioData(i) {
    fetch("DRUMS/hiphop/hiphop" + (i + 1) + ".wav")
    .then(response => response.arrayBuffer())
    .then(undecodedAudio => context.decodeAudioData(undecodedAudio))
    .then(audioBuffer => {
        audioBuffers[i] = audioBuffer;
    })
    .catch(console.error);
}

function playSound(buffer, time) {
    let source = context.createBufferSource();
    source.buffer = buffer;
    source.connect(context.destination);
    source.start(time);
}

function nextNote() {
    const secondsPerBeat = 60.0 / bpm;

    nextNoteTime += secondsPerBeat/2; // Add beat length to last beat time

    // Advance the beat number, wrap to zero
    currentNote++;
    if (currentNote === 7) {
            currentNote = 0;
    }
}

const notesInQueue = [];

function scheduleNote(beatNumber, time) {

    // push the note on the queue, even if we're not playing.
    notesInQueue.push({ note: beatNumber, time: time });

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
            nextNoteTime = context.currentTime;
            scheduler(); // kick off scheduling
        }    
        else{
            this.innerHTML = "Play";
        }
})

document.querySelector("#switch").addEventListener("click", function(){
    takt = taktb
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

function onMIDIMessage(event) {
    document.querySelector("#test").innerHTML = event.data[2];
    console.log(event.data[2]);

    if (taktTest.length != 16){
        taktTest.push(event.data[2]);
    }
        
    document.querySelector("#test").innerHTML = taktTest;
}
