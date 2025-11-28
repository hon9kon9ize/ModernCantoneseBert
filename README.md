# ModernCantoneseBert

A Cantonese BERT model based on the ModernBERT architecture, pre-trained on Cantonese text data.

## Model Description

ModernCantoneseBert is a BERT model specifically designed for Cantonese language understanding. It leverages the ModernBERT architecture from HuggingFace Transformers and is trained using masked language modeling (MLM) on Cantonese text data.

## Quick Start

### Installation

```bash
pip install transformers torch
```

### Usage

Use the model for fill-mask tasks with the HuggingFace Transformers library:

```python
from transformers import pipeline

mask_filler = pipeline(
    "fill-mask",
    model="hon9kon9ize/ModernCantoneseBert-Base"
)

mask_filler("雞蛋六隻，糖呢就兩茶匙，仲有[MASK]橙皮添。")
```

**Output:**

```python
[{'score': 0.19885674118995667,
  'token': 2494,
  'token_str': '啲',
  'sequence': '雞 蛋 六 隻 ， 糖 呢 就 兩 茶 匙 ， 仲 有 啲 橙 皮 添 。'},
 {'score': 0.12493402510881424,
  'token': 1617,
  'token_str': '個',
  'sequence': '雞 蛋 六 隻 ， 糖 呢 就 兩 茶 匙 ， 仲 有 個 橙 皮 添 。'},
 {'score': 0.051472704857587814,
  'token': 1804,
  'token_str': '兩',
  'sequence': '雞 蛋 六 隻 ， 糖 呢 就 兩 茶 匙 ， 仲 有 兩 橙 皮 添 。'},
 {'score': 0.03404267504811287,
  'token': 11419,
  'token_str': '隻',
  'sequence': '雞 蛋 六 隻 ， 糖 呢 就 兩 茶 匙 ， 仲 有 隻 橙 皮 添 。'},
 {'score': 0.028425632044672966,
  'token': 1572,
  'token_str': '係',
  'sequence': '雞 蛋 六 隻 ， 糖 呢 就 兩 茶 匙 ， 仲 有 係 橙 皮 添 。'}]
```

Another example:

```python
mask_filler("香港特首係李家[MASK]。")
```

**Output:**

```python
[{'score': 0.3403128683567047,
  'token': 10162,
  'token_str': '超',
  'sequence': '香 港 特 首 係 李 家 超 。'},
 {'score': 0.04880792275071144,
  'token': 10360,
  'token_str': '輝',
  'sequence': '香 港 特 首 係 李 家 輝 。'},
 {'score': 0.013930004090070724,
  'token': 11425,
  'token_str': '雄',
  'sequence': '香 港 特 首 係 李 家 雄 。'},
 {'score': 0.01386457122862339,
  'token': 1407,
  'token_str': '人',
  'sequence': '香 港 特 首 係 李 家 人 。'},
 {'score': 0.01234334148466587,
  'token': 3774,
  'token_str': '庭',
  'sequence': '香 港 特 首 係 李 家 庭 。'}]
```

## Training

### Data Preprocessing

1. Prepare your JSONL data files with a `text` field
2. Run the preprocessing script:

```bash
python preprocess.py \
    --model_path ./ModernCBert-Large/ \
    --data_path ./data/ \
    --output_path ./pretrain/data/ \
    --max_seq_len 4096
```

### Training the Tokenizer

```bash
python train_tokenizer.py \
    --files "./data/*.txt" \
    --out ./tokenizer/ \
    --name bert-wordpiece
```

### Training the Model

```bash
python run_mlm.py \
    --model_name_or_path <path_to_model> \
    --tokenizer_name <path_to_tokenizer> \
    --train_file <path_to_preprocessed_data> \
    --do_train \
    --do_eval \
    --output_dir ./output/
```

## License

This project is licensed under the Apache License 2.0.
