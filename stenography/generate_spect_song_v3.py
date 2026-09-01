import librosa
'''4. I have never heard of the library `librosa`. What does it do?
As we're in an stenography topic I suppose it is some kind of mixture
between library and virtuosa... so I assume the purpose is to read 
strange file types in diverse files in python.'''
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def generate_spectrogram(file_path, output_path):
    print(f"[*] Cargando audio: {file_path}")
    try:
        y, sr = librosa.load(file_path)

        '''5. What does "stft" stand for? As we're analizing audio
        I am practically sure that tft stands for -Time Fourier Transform.
        But the s... maybe Sample? '''        
        D = librosa.stft(y)
        S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
        
        plt.figure(figsize=(15, 7))
        
        img = librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='log')
        
        plt.colorbar(img, format='%db')
        plt.title(f'Spectrogram of {file_path}')
        plt.tight_layout()
        
        plt.savefig(output_path)
        print(f"[+] Espectrograma guardado exitosamente en: {output_path}")
        
    except Exception as e:
        print(f"[-] Error al generar el espectrograma: {e}")

if __name__ == "__main__":
    generate_spectrogram('song.wav', 'spectrogram_song2.png')
'''7. In the image generated there was a command that say something
along the lines of `utflag{spo3trogr4mophone3}`. As it was quite squeezed
to the top I wasn't really able to see it clearly, but that is what I read.
I imagine it is some kind of convenction, as "spot3trogr4monophon3: seems to
be hinting at something sound related.'''
