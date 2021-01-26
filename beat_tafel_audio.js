let context = new AudioContext();
let gainNode = context.createGain();
gainNode.gain.value = 0.5;
gainNode.connect(context.destination);

let bpm = 90;

var audioBuffers = [];
var takt = [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]
var taktpreload = [[],[],[],[]]

let timeout = (60/bpm)/20; // Wie oft die Schedule Funktion aufgerufen werden soll (darf nicht zu groß sein, um Ungenauigkeiten zu verhindern)

let currentNote = 0; // Auf welchem Taktschlag wir uns gerade befinden
let nextNoteTime = 0.0; // Wann die nächste Note gespielt werden soll.

let isPlaying = false;

// Slider Setup
const gainSlider = document.querySelector('#gainSlider');
const gainOutput = document.querySelector('#gainOutput');
const bpmSlider = document.querySelector('#bpmSlider');
const bpmOutput = document.querySelector('#bpmOutput');
bpmOutput.innerHTML = bpmSlider.value + " bpm";
gainOutput.innerHTML = gainSlider.value + " dB";

bpmSlider.addEventListener('input', function() {
    bpm = Number(this.value);
    bpmOutput.innerHTML = bpm + " bpm";
}, false);

gainSlider.addEventListener('input', function() {
    gainlinear = 10**(this.value/10);
    gainNode.gain.value = gainlinear;
    document.querySelector("#gainOutput").innerHTML = (this.value) + " dB";
}, false);

//Laden der Soundateien in einen AudioBuffer Array
function getAudioData(i, drumtype) {
    fetch("DRUMS/" + drumtype + "/" + drumtype + (i + 1) + ".wav")
    .then(response => response.arrayBuffer())
    .then(undecodedAudio => context.decodeAudioData(undecodedAudio))
    .then(audioBuffer => {
        audioBuffers[i] = audioBuffer;
    })
    .catch(console.error);
}

for (let i = 0; i <= 3; i++){
    getAudioData(i, document.querySelector('#drumtype').value);
}

//Änderung der Sounddateien bei Änderung des Schlagzeugsounds im Dropdown Menü
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

    nextNoteTime += secondsPerBeat/4; // Beatlänge (sechzehntel) auf die Zeit der nächsten Note addieren

    // Zum nächsten Beat im Takt gehen und wenn der Takt voll ist wieder bei 0 anfangen
    currentNote++;
    if (currentNote === 16) {
            currentNote = 0;
    }
}

function playNotes(beatNumber, time) {
    //Visuelle Darstellung des Taktes
    if (beatNumber == 0){
        document.getElementById("zeit" + beatNumber).style.backgroundColor = "orange";
        document.getElementById("zeit" + 15).style.backgroundColor = "white";
    }else if (beatNumber%4 == 0){
        document.getElementById("zeit" + beatNumber).style.backgroundColor = "orange";
        document.getElementById("zeit" + (beatNumber-1)).style.backgroundColor = "white";
    }else {
        document.getElementById("zeit" + beatNumber).style.backgroundColor = "blue";
        document.getElementById("zeit" + (beatNumber-1)).style.backgroundColor = "white";
    }
    

    //Wenn im Taktarray an der momentanen Taktposition eine 1 steht, wird die jeweilige Note gespielt
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
    // die nächste Note wird geplant, wenn die currentTime inkl. der Planungszeit größer wird als die Zeit in der die Note gespielt werden soll
    // dann werden die Noten gespielt und die Zeit für eine Achtel wird auf die nextNoteTime addiert.
    // zum Schluss wird die Funktion pausiert, damit das Programm währenddessen andere Dinge ausführen kann
    while (nextNoteTime < context.currentTime && isPlaying) {
        playNotes(currentNote, nextNoteTime);
        nextNote();
    }
    timerID = window.setTimeout(scheduler, timeout);
}

document.querySelector("#playButton").addEventListener("click", function(){
        isPlaying = !isPlaying;
        if (isPlaying){
            document.getElementById('playButton').style.backgroundImage = 'url(Icons/stopbutton.png)';
            this.innerHTML = "Stop";
            currentNote = 0;
            nextNoteTime = context.currentTime;  // die erste note wird gespielt, wenn auf Play gedrückt wird
            scheduler(); // Start des Schedulers
        }    
        else{
            this.innerHTML = "Play";
            document.getElementById('zeit' + (currentNote - 1)).style.backgroundColor = 'white';
            document.getElementById('playButton').style.backgroundImage = 'url(Icons/playbutton.png)';
        }
})

//Update der visuellen Darstellung der Beattafel
function  updateGrid(Note, feldnr){
    id = "block" + (feldnr + 1);

    if (Note == 15){
        document.getElementById(id).style.backgroundColor = "red";
    }
    else if (Note == 4){
        document.getElementById(id).style.backgroundColor = "yellow";
    }
    else if (Note == 8){
        document.getElementById(id).style.backgroundColor = "magenta";
    }
    else if (Note == 1){
        document.getElementById(id).style.backgroundColor = "green";
    }
    else if (Note == 10){
        document.getElementById(id).style.backgroundColor = "cyan";
    }
    else if (Note == 0){
        document.getElementById(id).style.backgroundColor = "grey";
    }
}

// Midi initialisierung
if (navigator.requestMIDIAccess) {
    navigator.requestMIDIAccess({sysex: false}).then(function (midiAccess) {
        midi = midiAccess;
        var inputs = midi.inputs.values();
        // Durch alle Inputs loopen
        for (var input = inputs.next(); input && !input.done; input = inputs.next()) {
            // auf Midi Nachrichten warten
            input.value.onmidimessage = onMIDIMessage;
        }
    });
} else {
    alert("No MIDI support in your browser.");
}

function dec2bin(dec){
    bin = (dec >>> 0).toString(2);
    while (bin.length < 4){
        bin = 0 + bin 
    }
    return bin
}

counter = 0

function onMIDIMessage(event) {
    document.querySelector("#test").innerHTML = event.data[2];
    //Initialwert: hier starten die Taktnachrichten
    if (event.data[2] == 127){
        counter = 0;      
    };
    //16 Nachrichten zählen und einzelne Bits in Taktarray schieben
    if (counter <= 15 && event.data[2] != 127) {
        for (i = 0; i < 4; i++){
            taktpreload[Math.floor(counter/4)].push(parseInt(dec2bin(event.data[2])[i], 10));
        }
        updateGrid(event.data[2], counter);
        counter += 1;
    };

    //Takt übernehmen und zurücksetzen
    if (counter == 16){
        takt = taktpreload;
        taktpreload = [[],[],[],[]];
    };
};