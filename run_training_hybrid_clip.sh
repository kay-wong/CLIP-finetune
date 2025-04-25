#!/bin/bash
PROJ_DIR=/home/kayyenwong/work/CLIP
SCRIPT_DIR=${PROJ_DIR}/hybrid_clip
MODEL_DIR=${PROJ_DIR}/models/clip-tst
TRAIN_FILE=${PROJ_DIR}/data/train/train_1024.json
VALID_FILE=${PROJ_DIR}/data/valid/valid_128.json
IMAGE_ENCODER="openai/clip-vit-base-patch32"
TEXT_ENCODER="cardiffnlp/twitter-roberta-base-jun2022"
#FROM_CHECKPOINT = MODEL_DIR + "/20"

python3 -W ignore ${PROJ_DIR}/run_hybrid_clip.py \
    --output_dir ${MODEL_DIR} \
    --overwrite_output_dir \
    --tokenizer_name=${TEXT_ENCODER} \
    --train_file=${TRAIN_FILE} \
    --validation_file=${VALID_FILE} \
    --do_train --do_eval \
    --num_train_epochs="1" --max_seq_length 24 \
    --per_device_train_batch_size="128" \
    --per_device_eval_batch_size="128" \
    --learning_rate="0.0001" --warmup_ratio 0.1 --weight_decay 0.0 \
    --preprocessing_num_workers 8 \
    --exp_name clip_finetune \
    --eval_when 1 \
    --text_model_name_or_path=${TEXT_ENCODER} \
    --vision_model_name_or_path=${IMAGE_ENCODER} \
    --freeze_backbones
#    --log_comet \
#    --epoch_offset 20 \
#    --run_from_checkpoint ${FROM_CHECKPOINT}
#    --push_to_hub