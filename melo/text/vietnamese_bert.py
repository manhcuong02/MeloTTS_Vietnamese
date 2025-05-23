import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM
import sys

# ! Đây là mô hình phân biệt chữ hoa, chữ thường
model_id = "vinai/phobert-base-v2"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForMaskedLM.from_pretrained(model_id)


def get_bert_feature(text, word2ph, device="cpu"):
    if (
        sys.platform == "darwin"
        and torch.backends.mps.is_available()
        and device == "cpu"
    ):
        device = "mps"
    elif not torch.cuda.is_available():
        device = "cpu"

    model.to(device)

    with torch.no_grad():
        inputs = tokenizer(text, return_tensors="pt")

        for i in inputs:
            inputs[i] = inputs[i].to(device)
        res = model(**inputs, output_hidden_states=True)
        res = torch.cat(res["hidden_states"][-3:-2], -1)[0].cpu()

    assert inputs["input_ids"].shape[-1] == len(
        word2ph
    ), f"{inputs['input_ids'].shape[-1]} != {len(word2ph)}"
    
    word2phone = word2ph
    phone_level_feature = []
    for i in range(len(word2phone)):
        repeat_feature = res[i].repeat(word2phone[i], 1)
        phone_level_feature.append(repeat_feature)

    phone_level_feature = torch.cat(phone_level_feature, dim=0)

    return phone_level_feature.T
