@echo off
echo Starting Qdrant vector database...
echo Make sure Docker is running!
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
