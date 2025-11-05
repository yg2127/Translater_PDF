#FastAPI API 서버

import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import tempfile
import os

from pipeline import run_translation_pipeline
from model_loader import load_models

# FastAPI 앱 생성
app = FastAPI()

# 1. (중요) 서버가 시작될 때 AI 모델을 미리 로드합니다.
@app.on_event("startup")
def startup_event():
    load_models()
    print("AI 모델 로딩 완료!")

# 2. PDF 번역 API 엔드포인트
@app.post("/translate-pdf/")
async def translate_pdf_endpoint(file: UploadFile = File(...)):

    # 1. 업로드된 PDF를 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_in:
        temp_in.write(await file.read())
        input_pdf_path = temp_in.name

    # 2. 번역된 PDF가 저장될 경로 설정
    output_pdf_path = temp_in.name.replace(".pdf", "_translated.pdf")

    try:
        # 3. (핵심) 전체 번역 파이프라인 실행
        run_translation_pipeline(input_pdf_path, output_pdf_path)

        # 4. 번역된 PDF 파일을 사용자에게 반환
        return FileResponse(
            path=output_pdf_path,
            media_type='application/pdf',
            filename=f"{file.filename.replace('.pdf', '')}_translated.pdf"
        )
    except Exception as e:
        return {"error": str(e)}
    finally:
        # 5. 임시 파일 삭제
        if os.path.exists(input_pdf_path):
            os.remove(input_pdf_path)
        if os.path.exists(output_pdf_path):
            os.remove(output_pdf_path)

# 서버 실행 (로컬 테스트용)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)