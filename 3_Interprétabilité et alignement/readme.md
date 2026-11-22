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


https://catalog.ngc.nvidia.com/orgs/nvidia/-/containers/pytorch/-?_lr=1

docker run -d --name my-jupyter-1050 --restart unless-stopped --gpus all --ipc=host -p 8888:8888 -v /home/dupp/GIT/intelligence-artificielle:/workspace pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime bash -lc "python -m pip install jupyterlab && jupyter lab --allow-root --ip=0.0.0.0 --port=8888 --no-browser --notebook-dir=/workspace"

docker logs my-jupyter-1050




docker run -d --name my-jupyter --restart unless-stopped --gpus all -p 8888:8888 -v /home/dupp/GIT/intelligence-artificielle:/workspace nvcr.io/nvidia/pytorch:26.10-py3 jupyter lab --allow-root --ip=0.0.0.0 --port=8888 --no-browser --notebook-dir=/workspace

docker logs my-jupyter



docker network create ai-net
docker network connect ai-net ollama_GPU
docker network connect ai-net my-jupyter-1050
