import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import logging
from soundfile import SoundFile
from modules.OutputData import plt2npa
from modules.OutputData import OutputAudioData

logger = logging.getLogger(__name__)

def AnalyzeAudio(data_dir, input):
    # Load the audio file with librosa (sr=None to maintain the original sampling rate)
    try:
        myfile = SoundFile(input)
    except Exception as e:
        logger.error(f"Error loading audio: {e}")
        raise Exception("AnalyzeAudio failed")
    else:
        logger.info(f"Audio loaded successfully from {input}")
    y, sr = librosa.load(myfile, sr=None)
    # Create a time axis
    time = np.linspace(0, len(y) / sr, num=len(y))

    abs_stft = np.abs(librosa.stft(y))
    
    # Audio waveform (intensity vs time)
    plt.figure(figsize=(14, 4))
    plt.plot(time, y)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Waveform: Amplitude vs Time")
    plt.grid(True)
    img_waveform = plt2npa(plt)
    plt.close()
    
    # Spectrogram (frequency vs. time)
    D = librosa.amplitude_to_db(abs_stft, ref=np.max)
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log', cmap='magma')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram (Log Frequency)')
    img_spectrum = plt2npa(plt)
    plt.close()
    
    # Frequency distribution by Fourier transform
    # Fourier transform of the whole (displaying frequency components)
    fft = np.fft.fft(y)
    magnitude = np.abs(fft)
    frequency = np.fft.fftfreq(len(magnitude), 1/sr)
    max_mag = np.argmax(magnitude)
    # Display only one side (positive frequency components only)
    half_len = len(frequency) // 2
    plt.figure(figsize=(14, 4))
    plt.plot(frequency[:half_len], magnitude[:half_len])
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title("Frequency Spectrum (via FFT)")
    plt.grid(True)
    img_fft = plt2npa(plt)
    plt.close()

    # Peak amplitude envelope
    amplitude_envelope = np.max(abs_stft, axis=0)
    plt.figure(figsize=(14, 4))
    plt.plot(librosa.frames_to_time(np.arange(len(amplitude_envelope)), sr=sr), amplitude_envelope, label="Max Amplitude")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (db)")
    plt.title("Peak Amplitude Envelope")
    img_env = plt2npa(plt)
    plt.close()

    OutputAudioData(data_dir, img_waveform, img_spectrum, img_fft, img_env, magnitude[max_mag], frequency[max_mag], np.max(amplitude_envelope), np.mean(amplitude_envelope))