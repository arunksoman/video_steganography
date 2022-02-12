import os
import shutil
import argparse
from stegano import lsb


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
    help="path to input file")
args = vars(ap.parse_args())

BASE_DIR = os.path.abspath('')
temp = os.path.join(BASE_DIR, 'temp')
temp_video = os.path.join(temp, 'video.mp4')
temp_audio = os.path.join(temp, 'aud.wav')

if not os.path.exists(temp):
    os.mkdir(temp)

# os.system(f"ffmpeg -i {args['input']} -an -c copy {temp_video}")
# os.system(f"ffmpeg -i {args['input']} -c copy {temp_audio}")

# os.system(f"ffmpeg -i {args['input']} -i {temp_audio} -codec copy {temp_video} -y")


# vs = VideoStream(src=args['input']).start()
# vs = cv2.VideoCapture(args['input'], cv2.CAP_MSMF)
def clean_tmp(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        print("[INFO] tmp files are cleaned up")


def decode_str(path):
    decoded_text = ""
    for file_name in os.listdir(path):
        if file_name.endswith('.png'):
            file = os.path.join(temp, file_name)
            text = lsb.reveal(file)
            if text is not None:
                decoded_text += text
                print(text)
            if text is None:
                break
    print(decoded_text)


os.system(f"ffmpeg -hide_banner -loglevel error -i {args['input']} -vf fps=24 temp/%07d.png")


decode_str(temp)
clean_tmp(temp)

