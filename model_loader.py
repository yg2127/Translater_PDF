#AI 모델 로딩

from ultralytics import YOLO
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import easyocr

# 이 변수들에 로드된 모델을 저장하여 전역적으로 사용합니다.
MODELS = {}

def load_models():
    """서버 시작 시 모든 AI 모델을 한 번에 로드합니다."""

    # 1. YOLOv11 모델 로드
    MODELS["yolo"] = YOLO('models/best_yolo.pt')

    # 2. 번역 모델 (Helsinki-NLP) 로드
    translator_name = "Helsinki-NLP/opus-mt-en-ko"
    MODELS["translator"] = AutoModelForSeq2SeqLM.from_pretrained(translator_name)
    MODELS["tokenizer"] = AutoTokenizer.from_pretrained(translator_name)

    # 3. EasyOCR 리더 로드 (GPU 사용)
    MODELS["ocr_reader"] = easyocr.Reader(['en'], gpu=True)

    print("YOLO, Translator, OCR 모델 로딩 완료.")

# 로드된 모델을 쉽게 가져다 쓸 수 있도록 함수 제공
def get_model(name):
    return MODELS.get(name)