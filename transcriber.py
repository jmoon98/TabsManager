import fitz
import easyocr
import cv2
from pathlib import Path


pdf_path = Path("tab_pdfs/guitar_나만_봄.pdf")
pdf_imgs_path = Path("pdf_to_img")
pdf_imgs_path.mkdir(parents=True, exist_ok=True)

reader = easyocr.Reader(['en'])

doc = fitz.open(pdf_path)

for i in range(len(doc)):
    page = doc.load_page(i)
    img = page.get_pixmap()

    this_img_path = pdf_imgs_path / f"p{i}.png"
    img.save(this_img_path)

def detect_and_highlight_letters(page_num: int):
    img_path = f"pdf_to_img/p{page_num}.png"
    result = reader.readtext(img_path)

    img = cv2.imread(img_path)
    if img is not None:
        

        for res in result:
            x1, x2, x3, x4 = res[0][0][0], res[0][1][0], res[0][2][0], res[0][3][0]
            y1, y2, y3, y4 = res[0][0][1], res[0][1][1], res[0][2][1], res[0][3][1]
            cv2.rectangle(img, (x1, y1), (x2, y3), (0, 255, 0), 2)


        cv2.imshow("Read Page", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

detect_and_highlight_letters(0)

