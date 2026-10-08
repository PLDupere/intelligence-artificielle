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


docker run -d --gpus all -v ollama:/root/.ollama -p 11434:11434 --name ollama_GPU ollama/ollama
docker exec -it ollama_GPU ollama list
docker exec -it ollama_GPU ollama pull llama3.1
docker exec -it ollama_GPU ollama run llama3.1

docker exec -it ollama_GPU nvidia-smi
docker exec -it ollama_GPU nvidia-smi



https://deepwiki.com/jameschrisa/Ollama_Tuning_Guide/3.2-gpu-optimization

ctrl+shift + p
Dev Containers: Attach to Running Container...

# Dockerfile


docker build -t smollm:base --build-arg MODEL_DIR=models/base_model .
docker build -t smollm:pruned --build-arg MODEL_DIR=models/pruned_model .
docker build -t smollm:quantized --build-arg MODEL_DIR=models/quantized_model .

docker run -d --name smollm-base -p 8000:8000 smollm:base
docker run -d --name smollm-pruned -p 8001:8000 smollm:pruned
docker run -d --name smollm-quantized -p 8002:8000 smollm:quantized