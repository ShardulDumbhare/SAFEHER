
// ========================================
// VOICE ALERT AI (LOUD SOUND DETECTION)
// ========================================
let audioContext;
let analyser;
let microphone;
let javascriptNode;
let loudSoundDetected = false;

const LOUDNESS_THRESHOLD = 0.08; // tweak if needed
const SOUND_DURATION_MS = 300;   // how long loud sound must persist
let soundStartTime = null;

async function startVoiceDetection() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioContext.createAnalyser();
    analyser.fftSize = 2048;

    microphone = audioContext.createMediaStreamSource(stream);
    javascriptNode = audioContext.createScriptProcessor(2048, 1, 1);

    microphone.connect(analyser);
    analyser.connect(javascriptNode);
    javascriptNode.connect(audioContext.destination);

    javascriptNode.onaudioprocess = function () {
      const array = new Uint8Array(analyser.fftSize);
      analyser.getByteTimeDomainData(array);

      let sum = 0;
      for (let i = 0; i < array.length; i++) {
        const value = (array[i] - 128) / 128;
        sum += value * value;
      }

      const rms = Math.sqrt(sum / array.length);

      if (rms > LOUDNESS_THRESHOLD) {
        if (!soundStartTime) {
          soundStartTime = Date.now();
        }

        if (Date.now() - soundStartTime > SOUND_DURATION_MS && !loudSoundDetected) {
          loudSoundDetected = true;
          console.warn('🚨 Loud sound detected!');
          triggerVoiceEmergency();
        }
      } else {
        soundStartTime = null;
      }
    };

    console.log('🎙️ Voice detection started');
  } catch (err) {
    console.error('Microphone access denied', err);
  }
}

function triggerVoiceEmergency() {
  if (sosActive) return;
    
  alert('🚨 Loud sound detected! Emergency triggered.');
  startSOSAlert();
  loudSoundDetected = false;
    soundStartTime = null;
 
}
  

window.addEventListener('load', () => {
  startVoiceDetection();
});



