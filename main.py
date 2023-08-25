import pyaudio
import numpy as np
import wave
import matplotlib.pyplot as plt
import struct

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print("recording...")
frames = []
frames_p = np.empty(RATE * RECORD_SECONDS)
time = np.arange(0, RATE * RECORD_SECONDS)

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
    data = np.frombuffer(data, dtype=np.int16)
    frames_p[i * CHUNK : (i + 1) * CHUNK] = data[:]
    #print(np.frombuffer(data, dtype='B'))
    #print(data[0:16], '\n')
    #print(struct.unpack('>f', data[:4]))

print("finished recording")

# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

#frames = np.reshape(frames, (1, int(RATE * RECORD_SECONDS)))
plt.plot(time[:1000], frames_p[:1000])
plt.show()