import os
from random import shuffle
from datasets import load_dataset
from transformers import AutoTokenizer
import argparse

def arg_init():
    """
    初始化命令行参数解析器并解析参数。
    :return: 预处理参数
    """
    parser = argparse.ArgumentParser(description='pre-process parameters.')
    parser.add_argument('--cache_dir', type=str, default='./cache/', help='Directory for caching data.')
    parser.add_argument('--model_path', type=str, default='./ModernCBert-Large/', help='Path to the pre-trained model.')
    parser.add_argument('--data_path', type=str, default='./CCI3-HQ/', help='Path to the input data.')
    parser.add_argument('--output_path', type=str, default='./pretrain/CCI3-HQ/', help='Path to save the processed dataset.')
    parser.add_argument('--max_seq_len', type=int, default=4096, help='Maximum sequence length.')
    parser.add_argument('--batch_size', type=int, default=4096, help='batch_size.')
    parser.add_argument('--num_proc', type=int, default=4096, help='num_proc.')

    args = parser.parse_args()

    return args

def get_jsonl_files(data_path):
    """
    获取指定目录下所有以.jsonl结尾的文件路径。
    :param data_path: 数据目录路径
    :return: 包含.jsonl文件路径的列表
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"The data path {data_path} does not exist.")
    files = os.listdir(data_path)
    return [os.path.join(data_path, file) for file in files if file.endswith('.jsonl')]

def map_func(tok, examples):
    """
    对输入的文本数据进行处理，生成输入ID序列。
    :param tok: 分词器
    :param examples: 输入的文本数据
    :return: 处理后的输入ID数据
    """
    tokenized_inputs = tok(
        examples["text"], return_special_tokens_mask=True, truncation=True, max_length=tok.model_max_length
    )
    
    return tokenized_inputs

def main():
    args = arg_init()
    cache_dir = args.cache_dir
    model_path = args.model_path
    data_path = args.data_path
    output_path = args.output_path
    batch_size = args.batch_size
    num_proc = args.num_proc

    tok = AutoTokenizer.from_pretrained(model_path)
    # 获取数据文件
    files = get_jsonl_files(data_path)
    data_files = {"pretrain": files}
    raw_datasets = load_dataset(
        'json',
        data_files=data_files,
        cache_dir=cache_dir,
    )
    # 处理数据集
    dataset = raw_datasets.map(
        lambda examples: map_func(tok, examples),
        batched=True,
        batch_size=batch_size,
        num_proc=num_proc,
        remove_columns=['text']
    )
    dataset.save_to_disk(output_path)


if __name__ == '__main__':
    main()