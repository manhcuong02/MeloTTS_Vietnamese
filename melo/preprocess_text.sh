
python preprocess_text.py \
    --metadata /storage2/melotts/dataset/infore/text.list \
    --config_path configs/config-vi.json \
    --device cuda:0 \
    --val-per-spk 10 \
    --max-val-total 500