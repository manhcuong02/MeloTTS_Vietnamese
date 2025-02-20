
python preprocess_text.py \
    --metadata /home/misa/home/misa/MeloTTS_Vietnamese/dataset/NHLy/text_training.list \
    --config_path /home/misa/home/misa/MeloTTS_Vietnamese/dataset/NHLy/config.json \
    --device cuda:0 \
    --val-per-spk 10 \
    --max-val-total 500