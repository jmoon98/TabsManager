"""
- simple script for visualizing bounding box (help with preparation of training data)
- click two points on the image display (top left and bottom right), will show the resulting bounding box and print out the coords
"""

import cv2
import math
from pathlib import Path

scale = -1

def on_click(event, x, y, flags, param):
    global scale, box_nums
    if event == cv2.EVENT_LBUTTONDOWN and scale > 0 and len(box_nums) < 2:
        orig_x, orig_y = x / scale, y / scale
        print(f"CLICK preview=({x},{y})  ->  orig=({orig_x:.1f},{orig_y:.1f})  scale={scale:.4f}")
        box_nums.append((orig_x, orig_y))
        
screen_w, screen_h = 1920, 1080 

box_nums = []

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", on_click)

img_path = Path("FRAMES/AwmPen5FcRI_320.jpg")
img = cv2.imread(img_path)
img_h, img_w = img.shape[:2]

scale = min(screen_w/img_w, screen_h/img_h, 1.0)
preview = cv2.resize(img, (int(img_w*scale), int(img_h*scale)), interpolation=cv2.INTER_AREA)

while True:
    cv2.imshow("Frame", preview)
    key = cv2.waitKey(20) & 0xFF

    if len(box_nums) == 2:
        cv2.rectangle(preview, (math.floor(box_nums[0][0]), math.floor(box_nums[0][1])), 
                      (math.floor(box_nums[1][0]), math.floor(box_nums[1][1])), (0, 0, 255), 2)

    if key == ord('q'):
        break

print(box_nums)

cv2.destroyAllWindows()
