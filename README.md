# plint-ops

This repository contains operational infrastructure and agent-related code separated from the public product repository.

- **Purpose**: Keep infra, deployment scripts, agent configs, and runbooks here.
- **Safety**: DO NOT commit secrets (API keys, `openclaw.json`, tokens, private keys).
- **First steps for maintainers**: see `SECRET_HANDLING.md` for required pre-commit checks.