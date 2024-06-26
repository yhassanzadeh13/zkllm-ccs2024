import os, sys
import argparse
import torch
import numpy as np

parser = argparse.ArgumentParser(description='LLaMa-2 Self-Attention')
parser.add_argument('model_size', type=int, choices = [7, 13], help='The size of the model to use. Default is 13')
parser.add_argument('layer', type=int, help='The layer to use for ffn')
parser.add_argument('seq_len', type=int, help='The sequence length to use for ffn')
parser.add_argument('--input_file', required = True, type=str, help='The input file to use for ffn')
parser.add_argument('--output_file', default = 'llama-ffn-output.bin', type=str, help='The output file to use for ffn')

from transformers import AutoTokenizer, AutoModelForCausalLM
import fileio_utils


if __name__ == '__main__':
    compilation_error = os.system('make ffn')
    if compilation_error:
        print("Error compiling ffn")
        exit(1)
    args = parser.parse_args()
    model_card = f"meta-llama/Llama-2-{args.model_size}b-hf"

    model = AutoModelForCausalLM.from_pretrained(model_card, local_files_only = True, cache_dir = "./model-storage")
    layer = model.model.layers[0]
    embed_dim, hidden_dim = layer.mlp.up_proj.in_features, layer.mlp.up_proj.out_features

    workdir = f'./zkllm-workdir/Llama-2-{args.model_size}b'
    layer_prefix = f'layer-{args.layer}'

    if not os.path.isfile(args.input_file):
        fileio_utils.save_int(torch.randn(args.seq_len, embed_dim, device = 0), 1 << 16, args.input_file)
    
    os.system(f'./ffn {args.input_file} {args.seq_len} {embed_dim} {hidden_dim} {workdir} {layer_prefix} {args.output_file}')

