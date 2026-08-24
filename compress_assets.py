import os
import subprocess
from PIL import Image
import shutil

ASSETS_DIR = 'assets'

def compress_image(filepath):
    try:
        # Save a backup of the original
        ext = os.path.splitext(filepath)[1]
        temp_filepath = filepath + '_tmp' + ext
        with Image.open(filepath) as img:
            img.save(temp_filepath, quality=85, optimize=True)
        
        # Replace if smaller
        orig_size = os.path.getsize(filepath)
        new_size = os.path.getsize(temp_filepath)
        if new_size < orig_size:
            os.replace(temp_filepath, filepath)
            print(f"Compressed Image: {filepath} ({orig_size // 1024}KB -> {new_size // 1024}KB)")
        else:
            os.remove(temp_filepath)
            print(f"Skipped Image (already optimized): {filepath}")
    except Exception as e:
        print(f"Failed to compress {filepath}: {e}")

def compress_video(filepath):
    try:
        temp_filepath = filepath + '.tmp.mp4'
        # CRF 28 is a good balance for web videos to reduce size while keeping decent quality
        command = [
            'ffmpeg', '-y', '-i', filepath,
            '-vcodec', 'libx264', '-crf', '28', '-preset', 'fast',
            '-acodec', 'copy', temp_filepath
        ]
        
        # Suppress output
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists(temp_filepath):
            orig_size = os.path.getsize(filepath)
            new_size = os.path.getsize(temp_filepath)
            if new_size < orig_size:
                os.replace(temp_filepath, filepath)
                print(f"Compressed Video: {filepath} ({orig_size // 1024}KB -> {new_size // 1024}KB)")
            else:
                os.remove(temp_filepath)
                print(f"Skipped Video (already optimized): {filepath}")
    except Exception as e:
        print(f"Failed to compress {filepath}: {e}")

def main():
    for root, dirs, files in os.walk(ASSETS_DIR):
        for file in files:
            filepath = os.path.join(root, file)
            ext = os.path.splitext(filepath)[1].lower()
            
            if ext in ['.jpg', '.jpeg', '.png']:
                compress_image(filepath)
            elif ext in ['.mp4', '.mov']:
                compress_video(filepath)

if __name__ == '__main__':
    main()
