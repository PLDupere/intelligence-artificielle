## Prérequis

- python 3.13.15
- numpy
- pandas
- matplotlib
- scipy
- Scikit-Learn 
- sparsify
- torch
- transformers 
- datasets 
- accelerate
- eai-sparsify
- trl 

## Installation de Ollama
docker run -d --gpus all -v ollama:/root/.ollama -p 11434:11434 --name ollama_GPU ollama/ollama
docker exec -it ollama ollama pull llama3.1
docker exec -it ollama ollama list
docker exec -it ollama ollama run llama3.1

# Installation Jupyter

docker run -d --name my-jupyter-1050 --restart unless-stopped --gpus all --ipc=host -p 8888:8888 -v /home/dupp/GIT/intelligence-artificielle:/workspace pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime bash -lc "python -m pip install jupyterlab && jupyter lab --allow-root --ip=0.0.0.0 --port=8888 --no-browser --notebook-dir=/workspace"

docker logs my-jupyter-1050


# Creation Network
docker network create ai-net
docker network connect ai-net ollama_GPU
docker network connect ai-net my-jupyter-1050

# References
- 
- https://walkinglabs.github.io/hands-on-modern-rl/en/chapter17_dpo/metrics
- https://huggingface.co/learn/cookbook/en/llm_judge
- https://catalog.ngc.nvidia.com/orgs/nvidia/-/containers/pytorch/-?_lr=1