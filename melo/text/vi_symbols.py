# punctuation = ["!", "?", "…", ",", ".", "'", "-"]
punctuation = [
    "!",
    "?",
    "…",
    ",",
    ".",
    "'",
    "-",
    "¿",
    "¡",
]
pu_symbols = punctuation + ["SP", "UNK"]
pad = "_"


# vietnamese
vi_symbols = [
    "ʃ",
    "k͡p",
    "ŋ",
    "n",
    "ˈa",
    "ɤ",
    "ˈɛ",
    "w",
    "d",
    "k",
    "ˈi",
    "ɣ",
    "l",
    "o",
    "v",
    "ɡ",
    "a",
    "p",
    "ɯ",
    "b",
    "u",
    "z",
    "ɲ",
    "ă",
    "f",
    "t",
    "ˈe",
    "ɛ",
    "x",
    "ɔ",
    "i",
    "c",
    "r",
    "ʔ",
    "m",
    "ŋ͡m",
    "h",
    "tʰ",
    "j",
    "ə",
    "ɤ̆",
    "e",
    "s",
]
num_vi_tones = 8

# combine all symbols
normal_symbols = sorted(set(vi_symbols))
symbols = [pad] + normal_symbols + pu_symbols
sil_phonemes_ids = [symbols.index(i) for i in pu_symbols]

# combine all tones
num_tones = num_vi_tones

# language maps
language_id_map = {
    "VI": 0,
}
num_languages = len(language_id_map.keys())

language_tone_start_map = {
    "VI": 0,
}
