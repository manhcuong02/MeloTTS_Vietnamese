<div align="center">
  <div>&nbsp;</div>
  <img src="logo.png" width="300"/> <br>
  <a href="https://trendshift.io/repositories/8133" target="_blank"><img src="https://trendshift.io/api/badge/repositories/8133" alt="myshell-ai%2FMeloTTS | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
</div>


## Introduction

### About MeloTTS

[MeloTTS](https://github.com/myshell-ai/MeloTTS) is a high-quality, open-source text-to-speech system developed by MyShell AI. It is built on top of the VITS/VITS2 architecture and uses BERT-based linguistic features to produce natural-sounding speech. MeloTTS supports multiple languages and is designed to be fast enough for real-time CPU inference.

**Strengths of the original MeloTTS:**
- High naturalness and expressiveness in synthesized speech
- Fast inference — runs in real-time even on CPU
- Lightweight and easy to deploy
- Supports multiple languages (English, Chinese, Japanese, Korean, Spanish, French)
- Permissive MIT license, suitable for both commercial and non-commercial use

**Limitations of the original MeloTTS:**
- Not natively optimized for Vietnamese phonology (tones, phonemes)
- The default English/multilingual phonemizer does not handle Vietnamese tones and diacritics correctly
- No built-in support for Vietnamese-specific linguistic preprocessing

### MeloTTS Vietnamese

**MeloTTS Vietnamese** is a version of MeloTTS specifically optimized for the Vietnamese language. It inherits the high-quality and fast-inference characteristics of the original model while introducing targeted improvements to handle the unique phonological properties of Vietnamese — including its 6 tones, complex vowel system, and syllable structure.

This model is designed to produce natural, accurate Vietnamese speech and can be easily fine-tuned on custom Vietnamese datasets.

## Technical Features
- Uses [underthesea](https://github.com/undertheseanlp/underthesea) for Vietnamese text segmentation
- Integrates [PhoBERT](https://github.com/VinAIResearch/PhoBERT) (vinai/phobert-base-v2) to extract Vietnamese linguistic features
- Full support for Vietnamese language characteristics:
  - 45 symbols (phonemes)
  - 8 tones (7 tonal marks and 1 unmarked tone)
  - All defined in `melo/text/symbols.py`
- Text-to-phoneme conversion:
  - Based on the [Text2PhonemeSequence](https://github.com/thelinhbkhn2014/Text2PhonemeSequence) library
  - An improved higher-performance version is available at [Text2PhonemeFast](https://github.com/manhcuong02/Text2PhonemeFast)

## Fine-tuning from Base Model
This model was fine-tuned from the base [MeloTTS](https://github.com/myshell-ai/MeloTTS) model by:
- Replacing phonemes not found in English/Vietnamese with Vietnamese-specific phonemes
- Specifically replacing Korean phonemes with their corresponding Vietnamese equivalents
- Adjusting model parameters to match Vietnamese phonetic characteristics
- GitHub: [MeloTTS Vietnamese](https://github.com/manhcuong02/MeloTTS_Vietnamese)

## Training Data
- The model was trained on the Infore dataset, consisting of approximately 25 hours of speech
- **Note on data quality:** This dataset has several limitations including suboptimal voice quality, missing punctuation, and imprecise phonetic transcriptions. However, when trained on internal/private high-quality data, results are significantly better.

## Downloading the Model
The pre-trained model can be downloaded from Hugging Face:
- [MeloTTS Vietnamese on Hugging Face](https://huggingface.co/nmcuong/MeloTTS_Vietnamese)

---

## Usage Guide

### Part 1: Inference

#### 1. Clone the Repository and Install Dependencies

```bash
git clone https://github.com/manhcuong02/MeloTTS_Vietnamese.git
cd MeloTTS_Vietnamese
pip install -r requirements.txt
```

#### 2. Download the Pre-trained Model

Download the model checkpoint and config from [Hugging Face](https://huggingface.co/nmcuong/MeloTTS_Vietnamese) and place them in your desired directory.

#### 3. Run Inference

Refer to the notebook `test_infer.ipynb` for a full example. Basic usage:

```python
from melo.api import TTS

# Speed is adjustable
speed = 1.0

# You can set device to 'cpu', 'cuda', 'cuda:0', or 'mps'
device = "cuda:0"  # Will automatically use GPU if available

# Load the Vietnamese TTS model
model = TTS(
    language="VI",
    device=device,
    config_path="/path/to/config.json",
    ckpt_path="/path/to/G_model.pth",
)
speaker_ids = model.hps.data.spk2id

# Convert text to speech
text = "Nhập văn bản tại đây"
output_path = "output.wav"
model.tts_to_file(text, speaker_ids["speaker_name"], output_path, speed=speed, quiet=True)
```

---

### Part 2: Training & Fine-tuning

#### 1. Data Preparation

The full data preparation process is detailed in `docs/training.md`. At minimum, you need:
- Audio files (recommended sample rate: 44100 Hz)
- A metadata file in the following format:
  ```
  path/to/audio_001.wav |<speaker_name>|<language_code>|<text_001>
  path/to/audio_002.wav |<speaker_name>|<language_code>|<text_002>
  ```

#### 2. Data Preprocessing

Run the preprocessing script to prepare training data:

```bash
python melo/preprocess_text.py \
  --metadata /path/to/text_training.list \
  --config_path /path/to/config.json \
  --device cuda:0 \
  --val-per-spk 10 \
  --max-val-total 500
```

Alternatively, use the shell script `melo/preprocess_text.sh` with appropriate parameters.

#### 3. Start Training

Follow the training instructions in `docs/training.md`.

---

## Code & Fine-tuning

The Vietnamese adaptation, code implementation, and fine-tuning of this model were developed by **Nguyễn Mạnh Cường**.

- GitHub: [manhcuong02](https://github.com/manhcuong02)
- Repository: [MeloTTS Vietnamese](https://github.com/manhcuong02/MeloTTS_Vietnamese)

---

## Audio Examples

Listen to sample outputs from the model:

### Sample 1
> *"Buổi sáng ở thành phố bắt đầu bằng tiếng xe cộ nhộn nhịp và ánh nắng nhẹ xuyên qua những tòa nhà cao tầng."*

<audio controls src="https://huggingface.co/nmcuong/MeloTTS_Vietnamese/resolve/main/samples/sample.wav"></audio>

### Sample 2
> *"Người đi làm vội vã, học sinh ríu rít trò chuyện, còn quán cà phê góc phố thì thoang thoảng mùi thơm dễ chịu."*

<audio controls src="https://huggingface.co/nmcuong/MeloTTS_Vietnamese/resolve/main/samples/sample-2.wav"></audio>

### Sample 3
> *"Cuối cùng, hãy thử thì thầm một câu thật nhẹ nhàng, rồi bất ngờ chuyển sang giọng nói to, rõ và đầy năng lượng."*

<audio controls src="https://huggingface.co/nmcuong/MeloTTS_Vietnamese/resolve/main/samples/sample-3.wav"></audio>

---

## License
This project is licensed under the [MIT License](LICENSE), consistent with the original MeloTTS project. It may be used for both commercial and non-commercial purposes.

## Acknowledgements

This implementation is based on [TTS](https://github.com/coqui-ai/TTS), [VITS](https://github.com/jaywalnut310/vits), [VITS2](https://github.com/daniilrobnikov/vits2), and [Bert-VITS2](https://github.com/fishaudio/Bert-VITS2). We appreciate their outstanding work.
