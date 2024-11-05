import tkinter as tk
from tkinter import filedialog, messagebox
import librosa
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import scipy.io.wavfile as wav


class AudioForensicTool:
    def _init_(self, master):
        self.master = master
        master.title("Digital Forensic Tool for Audio")
        master.geometry("800x600")
        master.attributes("-fullscreen", True)

        # UI Elements
        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)

        self.label = tk.Label(self.frame, text="Digital Forensic Tool for Audio", font=("Helvetica", 24))
        self.label.pack(pady=20)

        self.load_button = tk.Button(self.frame, text="Load Audio File", command=self.load_file, font=("Helvetica", 18))
        self.load_button.pack(pady=10)

        self.record_button = tk.Button(self.frame, text="Record Audio", command=self.record_audio, font=("Helvetica", 18))
        self.record_button.pack(pady=10)

        self.analyze_button = tk.Button(self.frame, text="Analyze Audio", command=self.analyze_audio, font=("Helvetica", 18))
        self.analyze_button.pack(pady=10)

        self.play_button = tk.Button(self.frame, text="Play Recorded Audio", command=self.play_audio, font=("Helvetica", 18))
        self.play_button.pack(pady=10)

        self.stop_button = tk.Button(self.frame, text="Stop Audio", command=self.stop_audio, font=("Helvetica", 18))
        self.stop_button.pack(pady=10)

        self.quit_button = tk.Button(self.frame, text="Quit", command=master.quit, font=("Helvetica", 18))
        self.quit_button.pack(pady=10)

        self.minimize_button = tk.Button(self.frame, text="Minimize", command=master.iconify, font=("Helvetica", 18))
        self.minimize_button.pack(pady=10)

        self.audio_file = None
        self.recorded_audio = None  # Store recorded audio data
        self.is_playing = False  # Flag to check if audio is currently playing
        self.fs = None  # Sampling frequency for playing audio

    def load_file(self):
        self.audio_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.flac")])
        if self.audio_file:
            messagebox.showinfo("Info", f"Loaded file: {self.audio_file}")
            self.fs, self.loaded_audio = wav.read(self.audio_file)  # Read audio file for playback
        else:
            messagebox.showwarning("Warning", "No file selected.")

    def record_audio(self):
        messagebox.showinfo("Info", "Recording... Press OK to stop.")
        
        # Set recording parameters
        self.fs = 44100  # Sampling frequency
        self.duration = 5  # seconds
        self.recorded_audio = sd.rec(int(self.fs * self.duration), samplerate=self.fs, channels=1, dtype='float64')
        
        sd.wait()  # Wait until recording is finished
        wav.write("recorded_audio.wav", self.fs, self.recorded_audio)  # Save as WAV file
        self.audio_file = "recorded_audio.wav"  # Set the loaded audio file to the recorded file
        messagebox.showinfo("Info", "Recording saved as 'recorded_audio.wav'")

    def play_audio(self):
        if self.recorded_audio is not None:
            messagebox.showinfo("Info", "Playing recorded audio...")
            sd.play(self.recorded_audio, self.fs)  # Play the recorded audio
            self.is_playing = True
            sd.wait()  # Wait until playback is finished
            self.is_playing = False
        elif self.audio_file is not None:
            messagebox.showinfo("Info", "Playing loaded audio...")
            y, sr = librosa.load(self.audio_file, sr=None)
            sd.play(y, sr)  # Play the loaded audio
            self.is_playing = True
            sd.wait()  # Wait until playback is finished
            self.is_playing = False
        else:
            messagebox.showwarning("Warning", "No recorded audio or loaded audio to play.")

    def stop_audio(self):
        if self.is_playing:
            sd.stop()  # Stop audio playback
            messagebox.showinfo("Info", "Audio playback stopped.")
            self.is_playing = False
        else:
            messagebox.showinfo("Info", "No audio is currently playing.")

    def analyze_audio(self):
        if self.audio_file is None:
            messagebox.showwarning("Warning", "Load an audio file first.")
            return

        # Load audio
        y, sr = librosa.load(self.audio_file, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)

        # Display duration and basic statistics
        self.display_statistics(y, sr, duration)

        # Plot waveform and spectrogram
        self.plot_waveform(y)
        self.plot_spectrogram(y, sr)

        # Perform frequency analysis
        self.frequency_analysis(y, sr)

        # Perform silence detection
        self.silence_detection(y, sr)

        # Perform noise detection
        self.noise_detection(y)

    def display_statistics(self, y, sr, duration):
        mean_amplitude = np.mean(y)
        peak_amplitude = np.max(np.abs(y))
        variance = np.var(y)

        stats = (f"Duration: {duration:.2f} seconds\n"
                 f"Mean Amplitude: {mean_amplitude:.4f}\n"
                 f"Peak Amplitude: {peak_amplitude:.4f}\n"
                 f"Variance: {variance:.4f}")

        messagebox.showinfo("Audio Statistics", stats)

    def frequency_analysis(self, y, sr):
        frequencies = np.fft.rfftfreq(len(y), d=1/sr)
        magnitude = np.abs(np.fft.rfft(y))

        plt.figure(figsize=(10, 4))
        plt.plot(frequencies, magnitude)
        plt.title("Frequency Analysis")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude")
        plt.xlim(0, sr / 2)  # Only plot up to Nyquist frequency
        plt.grid()
        plt.show()

    def silence_detection(self, y, sr, silence_threshold=0.01):
        silence_indices = np.where(np.abs(y) < silence_threshold)[0]
        silence_duration = len(silence_indices) / sr

        messagebox.showinfo("Silence Detection", f"Silence duration: {silence_duration:.2f} seconds")

    def noise_detection(self, y, noise_threshold=0.02):
        noise = np.mean(np.abs(y))
        is_noisy = "Yes" if noise > noise_threshold else "No"
        messagebox.showinfo("Noise Detection", f"Is the audio noisy? {is_noisy}")

    def plot_waveform(self, y):
        plt.figure(figsize=(10, 4))
        plt.plot(y)
        plt.title("Waveform")
        plt.xlabel("Samples")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.show()

    def plot_spectrogram(self, y, sr):
        plt.figure(figsize=(10, 4))
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        plt.imshow(D, aspect='auto', origin='lower', cmap='inferno', 
                   extent=[0, len(y)/sr, 0, sr/2])
        plt.title("Spectrogram")
        plt.colorbar(format='%+2.0f dB')
        plt.xlabel("Time (s)")
        plt.ylabel("Frequency (Hz)")
        plt.show()


if __name__ == '__main__':
    root = tk.Tk()
    app = AudioForensicTool(root)
    root.mainloop()