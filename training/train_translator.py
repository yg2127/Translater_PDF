# 번역기 파인튜닝 학습 코드

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments
from datasets import load_dataset # (AI-Hub 데이터를 로드하는 로직 필요)

def main():
    model_name = "Helsinki-NLP/opus-mt-en-ko"

    # 1. 모델과 토크나이저 로드
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # 2. AI-Hub 데이터셋 로드 및 전처리
    #    (이 부분은 데이터 형식에 맞게 직접 구현해야 합니다)
    # train_dataset = ...
    # eval_dataset = ...

    # 3. 학습 설정 (Training Arguments)
    training_args = TrainingArguments(
        output_dir="./translator_model_output",
        evaluation_strategy="epoch",
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3,
        save_total_limit=2,
        save_strategy="epoch",
        learning_rate=2e-5,
    )

    # 4. 트레이너(Trainer) 생성 및 학습 시작
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
    )

    trainer.train()

    print("번역 모델 파인튜닝 완료!")
    trainer.save_model("./final_translator_model") # 최종 모델 저장

if __name__ == "__main__":
    main()