
python preprocess_text.py \
    --metadata /path/to/text_training.list \
    --config_path /path/to/config.json \
    --device cuda:0 \
    --val-per-spk 10 \
    --max-val-total 500
