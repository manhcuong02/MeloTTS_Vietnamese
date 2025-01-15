import json
import os
import re
import string
from typing import List, Tuple, Union

from transformers import AutoTokenizer
from underthesea import word_tokenize

from melo.text2phonemesequence import Text2PhonemeSequence
from .symbols import symbols, vi_symbols

current_file_path = os.path.dirname(__file__)

vi_config = os.path.join(current_file_path, "..", "configs/config-vi.json")

with open(vi_config, "r", encoding="utf-8") as f:
    config = json.load(f)

device = config["device"]

_g2p = Text2PhonemeSequence(language="vie-n", device=device)

tone_letters = {
    "˨ˀ˩": 1,
    "˧˩˨": 2,
    "˧˨": 3,
    "˧˧": 4,
    "˧ˀ˥": 5,
    "˨˦": 6,
    "˦˥": 7,
}


def post_replace_ph(ph):
    rep_map = {
        "：": ",",
        "；": ",",
        "，": ",",
        "。": ".",
        "！": "!",
        "？": "?",
        "\n": ".",
        "·": ",",
        "、": ",",
        "...": "…",
    }
    if ph in rep_map.keys():
        ph = rep_map[ph]
    if ph in symbols:
        return ph
    if ph not in symbols:
        ph = "UNK"
    return ph


punctuation = string.punctuation

model_id = "vinai/phobert-base-v2"
tokenizer = AutoTokenizer.from_pretrained(model_id)


def refine_ph(phs: List[str]) -> Tuple[List[str], List[int]]:
    tone = 0
    new_phs = []
    tones = []

    for t in tone_letters:
        if t in phs:
            tone = tone_letters[t]

    for ph in phs:
        if ph in vi_symbols:
            new_phs.append(ph)
            tones.append(tone)
        elif ph not in tone_letters:
            new_phs.append(ph)
            tones.append(0)

    return new_phs, tones


def distribute_phone(n_phone, n_word):
    phones_per_word = [0] * n_word
    for task in range(n_phone):
        min_tasks = min(phones_per_word)
        min_index = phones_per_word.index(min_tasks)
        phones_per_word[min_index] += 1
    return phones_per_word


def refine_syllables(word_segment: str) -> Tuple[List[str], List[int]]:

    words = word_segment.split("_")
    phones = []
    tones = []
    for word in words:
        ph = _g2p.infer_sentence(word)
        phs = ph.split(" ")
        phs = [p for p in phs if p.strip() != ""]
        phs, tns = refine_ph(phs)
        phones += phs
        tones += tns

    return phones, tones


def handle_secondary_punctuation(text: str) -> str:
    # Replace secondary punctuation with a comma
    pattern = r"""(?<=[A-Za-z\d\s*])([`~()_;{}\[\]<>"|])(?=\s|$)"""

    text = re.sub(pattern, ", ", text)

    pattern = r"""([`~(;{\[<"|])(?=[A-Za-z\d]|\s|$)"""
    text = re.sub(pattern, ", ", text)

    return text


def text_normalize(text: str) -> str:
    """
    Mặc định dữ liệu gốc đã được làm sạch, bởi vì MISA đang dùng một bộ chuẩn hóa riêng.
    Phải tiền xử lý riêng thay vì sử dụng trong hàm này.
    """
    # Replace các dấu câu không phổ biến sang dấu phẩy
    text = handle_secondary_punctuation(text)

    word_segment = word_tokenize(text, format="text")
    
    # ! Hiện tại mô hình phobert-base-v2 phân biệt chữ in hoa và chữ in thường
    # word_segment = word_segment.lower() 
    return word_segment


def g2p(text: str, pad_start_end=True, tokenized=False):
    if not tokenized:
        tokens = tokenizer.tokenize(text)
    else:
        tokens = text.split()

    # Xử lý tokens sau khi đã được tokenize
    # Tuy nhiên, nhận thấy rằng giữa word_tokenize của underthesea
    # và tokenizer của PhoBERT không có sự khác biệt.
    # Nên không cần xử lý thêm.
    # !Có thể xem xét lại

    token_groups = []
    flag = False
    for t in tokens:
        if flag:
            token_groups[-1].append(t.replace("@", ""))
            flag = False
        elif t.endswith("@"):
            token_groups.append([t.replace("@", "")])
            flag = True
        else:
            token_groups.append([t])

    phones = []
    tones = []
    word2ph = []

    for group in token_groups:
        token = "".join(group)
        phone_len = 0
        word_len = len(group)
        if token in punctuation:
            phones.append(token)
            tones.append(0)
            phone_len += 1
        else:
            phs, tns = refine_syllables(token)
            phones += phs
            tones += tns
            phone_len += len(phs)

        aaa = distribute_phone(phone_len, word_len)
        word2ph += aaa

    phones = [post_replace_ph(i) for i in phones]
    if pad_start_end:
        phones = ["_"] + phones + ["_"]
        tones = [0] + tones + [0]
        word2ph = [1] + word2ph + [1]
    return phones, tones, word2ph

def get_bert_feature(text, word2ph, device=None):
    from . import vietnamese_bert

    return vietnamese_bert.get_bert_feature(text, word2ph, device=device)
