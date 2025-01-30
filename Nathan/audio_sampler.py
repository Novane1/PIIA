import librosa
import numpy as np
from pydub import AudioSegment
import io

def extract_best_quality_sample(audio_file_path, output_file_path, sample_length_sec=15):
    # Load audio using librosa
    audio, sr = librosa.load(audio_file_path, sr=None)

    # Segment audio into 15-second chunks
    total_duration = len(audio) / sr
    segments = []
    
    for start in range(0, int(total_duration), sample_length_sec):
        end = min(start + sample_length_sec, total_duration)
        segment = audio[int(start*sr):int(end*sr)]
        segments.append(segment)
    
    # Extract energy features for each segment (simple measure of quality)
    best_segment = None
    highest_energy = -np.inf
    
    for segment in segments:
        # Compute the energy of the segment (you could use other metrics like SNR, pitch, etc.)
        energy = np.sum(segment ** 2)
        
        if energy > highest_energy:
            highest_energy = energy
            best_segment = segment

    # Normalize the segment to avoid clipping
    best_segment = np.int16(best_segment / np.max(np.abs(best_segment)) * 32767)

    # Convert the best segment back to AudioSegment (pydub)
    audio_segment = AudioSegment(
        best_segment.tobytes(),
        frame_rate=sr,
        sample_width=2,  # 2 bytes for 16-bit PCM
        channels=1
    )

    # Export the best segment to a .wav file
    audio_segment.export(output_file_path, format="wav")

    return output_file_path
