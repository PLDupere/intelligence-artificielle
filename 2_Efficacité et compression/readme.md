# Projet expérimental — Compression et efficacité d’un LLM

## Prérequis
- python 3.13.15
- pytorch
- ollama
- jupyter
- numpy
- pandas
- matplotlib
- scipy
- Scikit-Learn 
- transformers
- accelerate 
- huggingface_hub 
- psutil

Un compte Hugging Face et un token d’accès peuvent être nécessaires pour télécharger les modèles:
https://huggingface.co/login?next=%2Fsettings%2Ftokens

## Références
- https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct
- https://huggingface.co/docs/transformers/quantization/bitsandbytes?bnb=4-bit
- https://huggingface.co/docs/transformers/en/perplexity
- https://docs.pytorch.org/tutorials/intermediate/pruning_tutorial.html
- https://docs.pytorch.org/docs/stable/generated/torch.cuda.memory_allocated.html
- https://psutil.io/#psutil.Process.memory_info
