"""
- script for collecting frames from downloaded YouTube videos
- saves every 20th frame, to directory FRAMES
"""

import argparse
from pathlib import Path
import cv2

FRAMES_PATH = Path("FRAMES")
FRAMES_PATH.mkdir(parents=True, exist_ok=True)
VID_PATH = Path("YT_DOWNLOADS")
parser = argparse.ArgumentParser()
parser.add_argument("--new_vid_name", type=str, default="")

def collect_frames(path: str):
    cap = cv2.VideoCapture(path)
    frame_idx = 1
    frame_num = 1

    # save current video's frames...
    while cap.isOpened():
        ret, frame = cap.read()  # reads the next frame; if frame is read correctly, ret is True

        if not ret:
            # end of video or error...
            break

        if frame_idx % 20 == 0:
            frame_path = FRAMES_PATH / (f"{Path(path).stem}_{frame_num}.jpg")
            cv2.imwrite(frame_path, frame)

        frame_idx += 1
        frame_num += 1
    cap.release()


if __name__ == "__main__":
    args = parser.parse_args()
    if len(args.new_vid_name) == 0:
        for video in VID_PATH.iterdir():
            vid_path = f"{VID_PATH}/{video.name}"
            collect_frames(vid_path)
            
    else:
        vid_path = f"{VID_PATH}/{args.new_vid_name}.mp4"
        collect_frames(vid_path)
            
    