import pyaudio
import wave
from pydub import AudioSegment
import os

# Settings
RECORD_SECONDS = 10
WAV_OUTPUT_FILENAME = "recording.wav"
MP3_OUTPUT_FILENAME = "recording.mp3"
CHANNELS = 1
RATE = 96000
CHUNK = 1024
FORMAT = pyaudio.paInt24

def record_audio():
    audio = pyaudio.PyAudio()

    # List devices to help user identify USB mic (optional)
    print("Available audio input devices:")
    for i in range(audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        print(f"{i}: {info['name']}")

    # Prompt user to choose the device index of their USB mic
    device_index = int(input("Enter the device index for your USB microphone: "))

    print("Recording started...")
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        input_device_index=device_index,
                        frames_per_buffer=CHUNK)

    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save as WAV
    with wave.open(WAV_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

def convert_wav_to_mp3(wav_filename, mp3_filename):
    print("Converting to MP3...")
    audio = AudioSegment.from_wav(wav_filename)
    audio.export(mp3_filename, format="mp3")
    print(f"Saved MP3 as: {mp3_filename}")

if __name__ == "__main__":
    record_audio()
    convert_wav_to_mp3(WAV_OUTPUT_FILENAME, MP3_OUTPUT_FILENAME)

    # Optional: remove WAV to keep only MP3
    #os.remove(WAV_OUTPUT_FILENAME)
