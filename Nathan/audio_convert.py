from pydub import AudioSegment

# Convert MP3 to WAV
def convert_mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)  # Load the MP3 file
    audio.export(wav_path, format="wav")     # Export as WAV