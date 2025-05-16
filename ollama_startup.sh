#!/bin/bash
set -e

# Start Ollama server in the background
ollama serve &
OLLAMA_PID=$!

# Wait for the server to be ready
echo "⏳ Waiting for Ollama server to be ready..."
for i in {1..30}; do
    if ollama list > /dev/null 2>&1; then
        echo "✅ Ollama server is ready."
        break
    fi
    sleep 1
done

# Pull the model if not already available
if ! ollama list | grep -q mistral; then
    echo "📦 Pulling Mistral model..."
    ollama pull mistral
fi

# Keep server running in foreground
wait $OLLAMA_PID
