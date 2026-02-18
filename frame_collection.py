"""
- script for collecting frames from downloaded YouTube videos
- saves every 20th frame, to directory FRAMES
"""

from pathlib import Path
import cv2

FRAMES_PATH = Path("FRAMES")
FRAMES_PATH.mkdir(parents=True, exist_ok=True)
VID_PATH = Path("YT_DOWNLOADS")

if __name__ == "__main__":
    for video in VID_PATH.iterdir():
        cap = cv2.VideoCapture(f"{VID_PATH}/{video.name}") 
        frame_idx = 1
        frame_num = 1

        # save current video's frames...
        while cap.isOpened():
            ret, frame = cap.read()  # reads the next frame; if frame is read correctly, ret is True

            if not ret:
                # end of video or error...
                break

            if frame_idx % 20 == 0:
                frame_path = FRAMES_PATH / (f"{video.name}_{frame_num}.jpg")
                cv2.imwrite(frame_path, frame)

            frame_idx += 1
            frame_num += 1
            
        cap.release()