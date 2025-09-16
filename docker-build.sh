#!/bin/bash

# Docker build script for TACO evaluation environment
# Following EvalHub Docker patterns

set -e  # Exit on any error

DOCKER_IMAGE_NAME="evalhub-taco"
DOCKER_TAG="latest"
BUILD_CONTEXT="."

echo "=== Building TACO Docker Image ==="
echo "Image: ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
echo "Build context: ${BUILD_CONTEXT}"
echo "=================================="

# Build the Docker image
docker build \
    -t "${DOCKER_IMAGE_NAME}:${DOCKER_TAG}" \
    -f Dockerfile \
    "${BUILD_CONTEXT}"

BUILD_EXIT_CODE=$?

if [ $BUILD_EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Docker image built successfully!"
    echo ""
    echo "Image: ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
    echo ""
    echo "Usage examples:"
    echo ""
    echo "1. Run TACO evaluation:"
    echo "   docker run --rm -v \$(pwd)/taco_results:/app/taco_results \\"
    echo "     ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} \\"
    echo "     python generate.py \\"
    echo "       --experiment_id test-exp \\"
    echo "       --base_url http://host.docker.internal:8000/v1 \\"
    echo "       --model_name Qwen/Qwen3-8B \\"
    echo "       --api_key your_api_key \\"
    echo "       --output_dir /app/taco_results \\"
    echo "       --difficulties ALL \\"
    echo "       --skills ALL \\"
    echo "       --n_samples 1"
    echo ""
    echo "2. Interactive shell:"
    echo "   docker run --rm -it ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} bash"
    echo ""
    echo "3. Test the installation:"
    echo "   docker run --rm ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} python -c \"import datasets, openai, httpx; print('Dependencies OK')\""
    echo ""
    echo "Note: Use host.docker.internal:PORT to access vLLM running on host from container"
else
    echo ""
    echo "❌ Docker build failed!"
    echo "Check the build output above for errors."
    exit 1
fi