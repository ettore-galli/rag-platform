#!/usr/bin/env bash
vars=(
    MODEL_PATH 
    OLLAMA_MODEL_NAME 
)

for var in "${vars[@]}"; do
    echo "$var=${!var}"
done