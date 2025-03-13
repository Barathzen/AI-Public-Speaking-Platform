import librosa
import numpy as np
import io
from pydub import AudioSegment

def analyze_speech(audio_file):
    try:
        # Convert uploaded audio file to WAV format
        audio = AudioSegment.from_file(io.BytesIO(audio_file.read()))
        audio = audio.set_channels(1).set_frame_rate(22050)  # Convert to mono & 22kHz

        # Convert to NumPy array
        wav_data = np.array(audio.get_array_of_samples()).astype(np.float32) / 32768.0  # Normalize [-1,1]

        # Extract audio features
        energy = np.mean(np.abs(wav_data))  # Energy (Average absolute amplitude)
        energy_scaled = round(energy * 100, 2)  # Convert to a 0-100 scale for easier interpretation

        # Extract pitch using a better method (librosa.yin)
        pitch_values = librosa.yin(wav_data, fmin=50, fmax=300, sr=22050)
        pitch_mean = np.mean(pitch_values[pitch_values > 0]) if len(pitch_values) > 0 else 0  # Ignore zeros
        
        # Compute vocal variety (standard deviation of pitch)
        pitch_std = np.std(pitch_values[pitch_values > 0]) if len(pitch_values) > 0 else 0

        # Determine vocal expression based on energy & pitch variability
        if energy_scaled > 50 and pitch_mean > 120 and pitch_std > 30:
            mood = "Great energy and vocal variety! Keep it up!"
        elif energy_scaled < 20 and pitch_mean < 80:
            mood = "Too low energy, try increasing volume and expression."
        elif pitch_std < 15:
            mood = "Your pitch is too monotonous, try varying your tone."
        else:
            mood = "Good effort, but add more vocal expression!"

        return {
            "energy": energy_scaled,  # Now on a 0-100 scale
            "pitch": round(pitch_mean, 2),
            "pitch_variability": round(pitch_std, 2),
            "feedback": mood
        }

    except Exception as e:
        return {"error": str(e)}
