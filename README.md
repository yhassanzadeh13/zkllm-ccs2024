# zkLLM: Zero Knowledge Proofs for Large Language Models

Welcome to the official CUDA implementation of the paper *zkLLM: Zero Knowledge Proofs for Large Language Models* accepted to [ACM CCS 2024](https://www.sigsac.org/ccs/CCS2024/home.html), authored by [Haochen Sun](https://cs.uwaterloo.ca/~h299sun/), Jason Li, and [Hongyang Zhang](https://hongyanz.github.io/) from the University of Waterloo. The long version of the paper is [available on arXiv](https://arxiv.org/abs/2404.16109).

**Warning:** This repository has NOT undergone security auditing and is NOT ready for industrial applications.

## Open-Sourcing Progress

Our open-sourcing process includes:
- [x] The wheel of tensors over the `BLS12-381` elliptic curve.
- [x] Implementation of `tlookup` and `zkAttn`, two major technical components of *zkLLM*.
- [x] The proof of all components of the entire inference process.
- [ ] Work in progress: Fully automated verifiable inference pipeline for LLMs.

## Requirements and Setup

zkLLM is implemented in CUDA. We recommend using CUDA 12.1.0, installed within a `conda` virtual environment. To set up the environment:

```bash
conda create -n zkllm-env python=3.11
conda activate zkllm-env 
conda install cuda -c nvidia/label/cuda-12.1.0
```

Also, to load the LLMs and run the experiments, you will need `torch`, `transformers` and `datasets`:

```bash
pip install torch torchvision torchaudio transformers datasets
```

## An Example with LLaMa-2

The followings is the example of LLaMa-2. The details for other models may vary.

First, download the models ([`meta-llama/Llama-2-7b-hf`](https://huggingface.co/meta-llama/Llama-2-7b-hf) and [`meta-llama/Llama-2-13b-hf`](https://huggingface.co/meta-llama/Llama-2-13b-hf)) from Hugging Face using `download-models.py`. You would need to log in to your Hugging Face account and share your contact information on the model pages to access the models. You would also need a valid [access token](https://huggingface.co/settings/tokens) for your account. Then, run the following commands:

```bash 
python download-models.py meta-llama/Llama-2-7b-hf replace_this_with_your_access_token
python download-models.py meta-llama/Llama-2-13b-hf replace_this_with_your_access_token
```

Then, generate the public parameters and commit to the models:

```bash
model_size=7 # 7 or 13 (billions of parameters)
python llama-ppgen.py $model_size
python llama-commit.py $model_size 16 # the default scaling factor is (1 << 16). Others have not been tested.
```

Once committed, load your model and input and assemble the proof by recurrently running the followings for all layers:

```bash
input_bin=input_file_name.bin # binary format of int32 numpy arrays, see ioutils.cuh, ioutils.cu and fileio_utils.py for details
self_attn_output_bin=self_attn_output_file_name.bin # binary format of int32 numpy arrays, see ioutils.cuh, ioutils.cu and fileio_utils.py for details
ffn_input_bin=ffn_input_file_name.bin # binary format of int32 numpy arrays, see ioutils.cuh, ioutils.cu and fileio_utils.py for details
output_bin=output_file_name.bin # binary format of int32 numpy arrays, see ioutils.cuh, ioutils.cu and fileio_utils.py for details
model_size=7 # 7 or 13 (billions of parameters)
layer_number=0 # start with 0 and then go to deeper layers
sequence_length=2048 # the sequence length to prove

python llama-self-attn.py --input_file $input_bin --output_file $self_attn_output_bin $model_size $layer_number $seqence_length
python llama-ffn.py --input_file $ffn_input_bin --output_file $output_bin $model_size $layer_number $seqence_length
```

We are actively working on further automating this process.

You may need to manually set the CUDA architecture used. For example, if you are using an NVIDIA RTX A6000, set `ARCH` to `sm_86` in `Makefile`. Modify the `Makefile` if necessary.

## Contacts

For any questions, comments, or discussions regarding potential collaborations (e.g., further development of the codebase for industrial-level applications), please feel free to [email](mailto:haochen.sun@uwaterloo.ca) Haochen Sun.


## Acknowledgements

zkLLM utilizes the CUDA implementation of BS12-381 curve, [`ec-gpu`](https://github.com/filecoin-project/ec-gpu), developed by [Filecoin](https://filecoin.io/). We extend our gratitude to Tonghe Bai and Andre Slavecu, both from University of Waterloo, for their contributions during the early stages of codebase development.
