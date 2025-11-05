#전체 번역 파이프라인

from model_loader import get_model
from pdf_processor import extract_elements, rebuild_pdf
from utils import convert_coordinates
from PIL import Image
import pdf2image

def run_translation_pipeline(input_pdf_path: str, output_pdf_path: str):

    # --- 1부: 문서 해부 및 정보 추출 ---

    # 1. 모델 가져오기
    yolo_model = get_model("yolo")
    ocr_reader = get_model("ocr_reader")

    # 2. PDF를 이미지로 변환 (YOLO 입력을 위해)
    # (주의: DPI 설정이 좌표 변환의 기준이 됩니다!)
    dpi = 300
    page_images = pdf2image.convert_from_path(input_pdf_path, dpi=dpi)

    all_elements = [] # 최종 PDF에 재조립할 모든 요소를 담을 리스트

    # 3. 페이지별로 처리
    for i, page_image in enumerate(page_images):

        # 4. (모델1) YOLO로 시각 자료(그림, 표, 수식) 위치 탐지
        yolo_results = yolo_model(page_image)[0]
        yolo_boxes = yolo_results.boxes.xyxy.cpu().numpy() # [x1, y1, x2, y2]
        yolo_labels = yolo_results.boxes.cls.cpu().numpy()

        # 5. OCR용 '참조 어휘 사전' 생성
        glossary = {}
        visual_elements = [] # 그림/표/수식 이미지 조각 저장

        for box, label in zip(yolo_boxes, yolo_labels):
            (x1, y1, x2, y2) = box

            # 5a. Pillow로 해당 영역 자르기
            cropped_img = page_image.crop((x1, y1, x2, y2))

            # 5b. (OCR) 그림/표 내부 텍스트 추출 -> '치트 시트' 만들기
            if label in [0, 1]: # 0:figure, 1:table 가정
                words = ocr_reader.readtext(cropped_img, detail=0)
                for word in words:
                    if len(word) > 3: # 너무 짧지 않은 단어만
                        glossary[word] = f"{word}_번역어({word})" # (임시 번역)

            # 5c. PDF 재조립을 위해 원본 이미지와 좌표 저장
            visual_elements.append({
                "type": "image",
                "image_data": cropped_img,
                "coords_pixel": (x1, y1, x2, y2)
            })

        # 6. (PyMuPDF) YOLO 영역을 '제외한' 순수 텍스트 블록과 좌표 추출
        # (이 함수는 pdf_processor.py에 구현 필요)
        text_blocks = extract_elements(input_pdf_path, page_num=i, dpi=dpi, yolo_boxes_pixel=yolo_boxes)

        # --- 2부: 번역 및 재조립 ---

        # 7. (모델2) 텍스트 번역 (Placeholder 기법 적용)
        translated_blocks = translate_text_blocks(text_blocks, glossary) # (이 함수 구현 필요)

        # 8. 최종 재조립 목록에 추가
        all_elements.append({
            "page": i,
            "visuals": visual_elements,
            "texts": translated_blocks
        })

    # 9. (ReportLab) 모든 요소를 합쳐 최종 PDF 생성
    # (이 함수는 pdf_processor.py에 구현 필요)
    rebuild_pdf(output_pdf_path, all_elements, dpi=dpi)

    print(f"번역 완료! {output_pdf_path}에 저장됨.")


def translate_text_blocks(text_blocks, glossary):
    """
    '치트 시트(glossary)'를 이용해 자리 표시자(placeholder)
    기법으로 텍스트를 번역하는 함수
    """
    tokenizer = get_model("tokenizer")
    translator = get_model("translator")

    translated_blocks = []

    for block in text_blocks:
        original_text = block["text"]

        # 1. 원본 텍스트에서 '치트 시트' 단어를 찾아 Placeholder로 교체
        #    (예: "Hybrid" -> "__PLACEHOLDER_0__")
        # ( ... 로직 구현 ... )
        text_for_translation = original_text

        # 2. 번역 모델 실행
        # ( ... 로직 구현 ... )
        translated_text = text_for_translation # (임시)

        # 3. Placeholder를 다시 주석이 달린 한국어로 교체
        #    (예: "__PLACEHOLDER_0__" -> "혼합 모델(Hybrid)")
        # ( ... 로직 구현 ... )
        final_translated_text = translated_text

        translated_blocks.append({
            "text": final_translated_text,
            "coords_point": block["coords_point"] # 원본 좌표 유지!
        })

    return translated_blocks