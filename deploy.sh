#!/bin/bash
set -e

docker compose build euf_summariser
docker compose push euf_summariser

echo "✅ Image pushed. Now run on server:"
echo "    docker compose pull euf_summariser && docker compose up -d"
