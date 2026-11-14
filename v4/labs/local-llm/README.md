# Local LLM Lab — Ollama + Qwen

A minimal local inference setup using Docker. The default model is Qwen2.5 0.5B, selected as a small starting point for memory-constrained machines.

## Start
```bash
docker compose up -d
docker compose exec ollama ollama pull qwen2.5:0.5b
docker compose exec ollama ollama run qwen2.5:0.5b
```

The API is bound to localhost only: `http://127.0.0.1:11434`.

## Test the API
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:0.5b",
  "prompt": "Explain what a Kubernetes Deployment does.",
  "stream": false
}'
```

## Resource notes
- Start with a small quantized model and monitor memory use.
- A 4 GB RAM host is extremely constrained: the OS, Docker daemon and model runtime all need memory. Avoid running a web UI and multiple models alongside the inference server.
- Close unnecessary services and use swap only as a safety net; heavy swapping makes inference very slow.
- Larger models need substantially more memory. Do not assume that a model will fit just because its download completes.

## Security
- The API has no authentication by default. Keep the port bound to loopback.
- Do not expose Ollama directly to the public internet.
- Treat prompts and generated output as potentially sensitive local data.
