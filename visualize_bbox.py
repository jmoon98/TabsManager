"""
- simple script for visualizing bounding box (help with preparation of training data)
- click two points on the image display (top left and bottom right), will show the resulting bounding box and print out the coords
"""

import cv2
import math
from pathlib import Path

scale = -1
num_clicks = 0

def on_click(event, x, y, flags, param):
    global scale, box_nums, img_h, img_w, normalized_box_nums, num_clicks
    
    if event == cv2.EVENT_LBUTTONDOWN and scale > 0:
        num_clicks += 1
        orig_x, orig_y = x / scale, y / scale
        print(f"CLICK preview=({x},{y})  ->  orig=({orig_x:.1f},{orig_y:.1f})  scale={scale:.4f}")
        box_nums.append((orig_x, orig_y))
        normalized_box_nums.append((orig_x/img_w, orig_y/img_h))
        
screen_w, screen_h = 1920, 1080 

box_nums = []
normalized_box_nums = []

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

    num_boxes = num_clicks // 2
    if num_boxes > 0:
        cv2.rectangle(preview, (math.floor(box_nums[2*(num_boxes-1)][0]), math.floor(box_nums[2*(num_boxes-1)][1])), 
                      (math.floor(box_nums[2*(num_boxes-1)+1][0]), math.floor(box_nums[2*(num_boxes-1)+1][1])), (0, 0, 255), 2)

    if key == ord('q'):
        break

print(normalized_box_nums)

cv2.destroyAllWindows()

with open(f"txt_TEST/{img_path.stem}_test.txt", "w") as f:
    
    for i in range(0, len(normalized_box_nums), 2):  # iterate through list of top left and bottom right coordinates
        f.write("0 ")
        top_l = normalized_box_nums[i]
        bot_r = normalized_box_nums[i+1]
        x_c, y_c = (bot_r[0] + top_l[0])/2, (bot_r[1] + top_l[1])/2
        box_w, box_h = bot_r[0] - top_l[0], bot_r[1] - top_l[1]
        f.write(f"{x_c} {y_c} {box_w} {box_h}\n")
