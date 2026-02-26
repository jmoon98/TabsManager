from ultralytics import YOLO
from skimage.metrics import structural_similarity as ssim
import cv2
import math
from pathlib import Path

model = YOLO("models/best.pt")
cap = cv2.VideoCapture("YT_DOWNLOADS/model_test/Vn-xPCD8Big.mp4")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

crop_cnt = 0
collected_imgs = []
frame_num = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_num += 1
    if frame_num % 5 == 0:
        res = model.predict(frame, verbose=False)
        annotated_frame = res[0].plot()
        cv2.imshow("DETECTIONS", annotated_frame)

        boxes = res[0].boxes
        for box in boxes.xywhn:  # need to handle videos with multiple tab areas!! 
            xc, yc, w, h = box
            x1 = math.floor(xc*frame.shape[1] - w*frame.shape[1]/2)
            x2 = math.ceil(xc*frame.shape[1] + w*frame.shape[1]/2)
            y1 = math.floor(yc*frame.shape[0] - h*frame.shape[0]/2)
            y2 = math.ceil(yc*frame.shape[0] + h*frame.shape[0]/2)
        crop = frame[y1:y2, x1:x2]

        collected_imgs_len = len(collected_imgs)
        if collected_imgs_len == 0:
            collected_imgs.append(crop)
            cv2.imwrite(f"output/crop_{crop_cnt}.jpg", crop)
            crop_cnt += 1
        else:
            last_img = collected_imgs[collected_imgs_len-1]
            last_img_size = last_img.shape[0]*last_img.shape[1]
            crop_size = crop.shape[0]*crop.shape[1]

            if last_img_size > crop_size:
                crop = cv2.resize(crop, (last_img.shape[1], last_img.shape[0]))
            else:
                last_img = cv2.resize(last_img, (crop.shape[1], crop.shape[0]))


            score, _ = ssim(crop, last_img, full=True, channel_axis=2)
            if score < 0.3:  # need to tweak the threshold value here
                collected_imgs.append(crop)
                cv2.imwrite(f"output/crop_{crop_cnt}.jpg", crop)
                crop_cnt += 1
    

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

