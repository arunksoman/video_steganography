import cv2
from imutils.video import VideoStream
import argparse
import imutils
import cv2
import numpy as np
from stegano import lsb
from PIL import Image
import os
import glob
import shutil

# python .\hide.py -i .\input.mp4 -s test -o output


def clean_tmp(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        print("[INFO] tmp files are cleaned up")

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
    help="path to input file")
ap.add_argument("-s", "--string", required=True,
    help="string to hide")
ap.add_argument("-o", "--output", required=True,
    help="output directory")
args = vars(ap.parse_args())

BASE_DIR = os.path.abspath('')
temp = os.path.join(BASE_DIR, 'temp')
temp_video = os.path.join(temp, 'video.mp4')
temp_audio = os.path.join(temp, 'aud.wav')

if not os.path.exists(temp):
    os.mkdir(temp)


vs = VideoStream(src=args['input']).start()
# fourcc = cv2.VideoWriter_fourcc(*'MJPG')
def hide_image(path):
    os_path = os.path.join(path, "*.png")
    png_images = glob.glob(os_path)
    print(png_images)
    for index, letter in enumerate(args['string']):
        print(f"[Info] String hided {letter}")
        img = lsb.hide(png_images[index], letter)
        img.save(png_images[index])
    
file_name_count = 0
while True:
    frame = vs.read()
    if frame is None:
        break
    frame = imutils.resize(frame, width=300, height=400)
    file_name = f"{str(file_name_count).zfill(7)}.png"
    file_name = os.path.join(temp, file_name)
    cv2.imwrite(file_name, frame)
    cv2.imshow('input', frame)
    file_name_count += 1
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
cv2.destroyAllWindows()
vs.stop()
# os.system(f"ffmpeg -i temp/%07d.png -c:v mjpeg -framerate 30 -pix_fmt yuv420p {args['output']}.avi -y")
hide_image(temp)
# os.system(f"ffmpeg -i temp/%07d.png -c:v mjpeg -framerate 30 -pix_fmt yuv420p {args['output']}.avi -y")
os.system("ffmpeg -hide_banner -loglevel error -i temp/%07d.png -vcodec png -framerate 24 video.mp4 -y")
clean_tmp(temp)
# writer.release()
# ffmpeg -r 1/5 -i .\temp\%07d.png -vcodec png temp/video.mp4 -y
# ffmpeg -i tmp/video.mov -i tmp/audio.mp3 -codec copy video.mov -y
