<div align="center">
  <div>&nbsp;</div>
  <img src="logo.png" width="300"/> <br>
  <a href="https://trendshift.io/repositories/8133" target="_blank"><img src="https://trendshift.io/api/badge/repositories/8133" alt="myshell-ai%2FMeloTTS | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
</div>

## Introduction
MeloTTS Vietnamese is a version of MeloTTS optimized for the Vietnamese language. This version inherits the high-quality characteristics of the original model but has been specially adjusted to work well with the Vietnamese language.

## Technical Features
- Uses [underthesea](https://github.com/undertheseanlp/underthesea) for Vietnamese text segmentation
- Integrates [PhoBert](https://github.com/VinAIResearch/PhoBERT) (vinai/phobert-base-v2) to extract Vietnamese language features
- Fully supports Vietnamese language characteristics:
  - 45 symbols (phonemes)
  - 8 tones (7 tonal marks and 1 unmarked tone)
  - All defined in `melo/text/symbols.py`
- Text-to-phoneme conversion source:
  - Based on [Text2PhonemeSequence](https://github.com/thelinhbkhn2014/Text2PhonemeSequence) library
  - An improved version with higher performance has been developed at [Text2PhonemeFast](https://github.com/manhcuong02/Text2PhonemeFast)

## Fine-tuning from Base Model
This model was fine-tuned from the base MeloTTS model by:
- Replacing phonemes not found in English and Vietnamese with Vietnamese phonemes
- Specifically replacing Korean phonemes with corresponding Vietnamese phonemes
- Adjusting parameters to match Vietnamese phonetic characteristics

## Training Data
- The model was trained on the Infore dataset, consisting of approximately 25 hours of speech
- Note on data quality: This dataset has several limitations including poor voice quality, lack of punctuation, and inaccurate phonetic transcriptions. However, when trained on internal data, the results were much better.

## Downloading the Model
The pre-trained model can be downloaded from Hugging Face:
- [MeloTTS Vietnamese on Hugging Face](https://huggingface.co/nmcuong/MeloTTS_Vietnamese)

## Usage Guide

### Data Preparation
The data preparation process is detailed in `docs/training.md`. Basically, you need:
- Audio files (recommended to use 44100Hz format)
- Metadata file with the format:
  ```
  path/to/audio_001.wav |<speaker_name>|<language_code>|<text_001>
  path/to/audio_002.wav |<speaker_name>|<language_code>|<text_002>
  ```

### Data Preprocessing
To process data, use the command:
```bash
python melo/preprocess_text.py --metadata /path/to/text_training.list --config_path /path/to/config.json --device cuda:0 --val-per-spk 10 --max-val-total 500
```
or use the script `melo/preprocess_text.sh` with appropriate parameters.

### Using the Model
Refer to the notebook `test_infer.ipynb` to learn how to use the model:
```python
# colab_infer.py
from melo.api import TTS

# Speed is adjustable
speed = 1.0

# CPU is sufficient for real-time inference.
# You can set it manually to 'cpu' or 'cuda' or 'cuda:0' or 'mps'
device = "cuda:0"  # Will automatically use GPU if available

# English
model = TTS(
    language="VI",
    device=device,
    config_path="/path/to/config.json",
    ckpt_path="/path/to/G_model.pth",
)
speaker_ids = model.hps.data.spk2id

# Convert text to speech
text = "Nhập văn bản tại đây"
speaker_ids = model.hps.data.spk2id
output_path = "output.wav"
model.tts_to_file(text, speaker_ids["speaker_name"], output_path, speed=1.0, quiet=True)
```

## Audio Examples
Listen to sample outputs from the model:

### Sample Audio
<audio controls>
  <source src="samples/sample.wav" type="audio/wav">
  Your browser does not support the audio element. <a href="samples/sample.wav">Click here to download/listen to the audio</a>
</audio>


## License
This project follows the MIT License, like the original MeloTTS project, allowing use for both commercial and non-commercial purposes.

## Acknowledgements

This implementation is based on [TTS](https://github.com/coqui-ai/TTS), [VITS](https://github.com/jaywalnut310/vits), [VITS2](https://github.com/daniilrobnikov/vits2) and [Bert-VITS2](https://github.com/fishaudio/Bert-VITS2). We appreciate their awesome work.
