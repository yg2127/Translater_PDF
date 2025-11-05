# yolo 모델 학습 코드

from ultralytics import YOLO

def main():
    # 1. YOLOv11의 사전 학습된 'n' (nano) 모델을 로드합니다.
    model = YOLO('yolov11n.pt')

    # 2. 학습을 시작합니다.
    #    data.yaml 파일은 PubLayNet + 수식 데이터의 경로와 클래스 정보를 담고 있어야 합니다.
    #    이 스크립트가 실행되면 학습이 시작되고, 완료되면
    #    runs/detect/train/weights/best.pt 파일이 생성됩니다.
    results = model.train(
        data='training/data/data.yaml',
        epochs=100,
        imgsz=640,
        batch=16,
        name='yolo_paper_translator' # 학습 결과 폴더 이름
    )

    print("YOLO 모델 학습 완료!")
    print(f"학습된 모델은 {results.save_dir}/weights/best.pt 에 저장되었습니다.")

if __name__ == "__main__":
    main()