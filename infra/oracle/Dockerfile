FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Core runtime + browser automation dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    jq \
    tini \
    chromium-browser \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Install OpenClaw using the official Linux installer URL from docs.
# If this URL changes, update it before build.
RUN curl -fsSL https://openclaw.ai/install.sh | bash

# Non-root runtime user for safer container isolation.
RUN useradd -m -u 10001 openclaw
USER openclaw
WORKDIR /workspace

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["openclaw", "gateway"]
