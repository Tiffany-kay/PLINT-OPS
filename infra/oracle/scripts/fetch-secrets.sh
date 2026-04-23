#!/usr/bin/env bash
set -euo pipefail

# Fetches secrets from OCI Vault using Instance Principal auth
# and writes runtime env files used by docker compose.

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
RUNTIME_DIR="${BASE_DIR}/runtime"

mkdir -p "${RUNTIME_DIR}"

# Required: secret OCIDs in environment before running this script.
# Example:
# export OCID_OPENROUTER_API_KEY=ocid1.secret.oc1..aaaa
# export OCID_APP_AGENT_DISCORD_BOT_TOKEN=ocid1.secret.oc1..bbbb

required_vars=(
  OCID_OPENROUTER_API_KEY
  OCID_GROQ_API_KEY
  OCID_APP_AGENT_DISCORD_BOT_TOKEN
  OCID_STEWIE_DISCORD_BOT_TOKEN
)

for var in "${required_vars[@]}"; do
  if [[ -z "${!var:-}" ]]; then
    echo "Missing required environment variable: ${var}" >&2
    exit 1
  fi
done

fetch_secret() {
  local secret_ocid="$1"
  oci secrets secret-bundle get \
    --auth instance_principal \
    --secret-id "${secret_ocid}" \
    --query 'data."secret-bundle-content".content' \
    --raw-output | base64 --decode
}

APP_OPENROUTER="$(fetch_secret "${OCID_OPENROUTER_API_KEY}")"
APP_GROQ="$(fetch_secret "${OCID_GROQ_API_KEY}")"
APP_DISCORD="$(fetch_secret "${OCID_APP_AGENT_DISCORD_BOT_TOKEN}")"
STEWIE_DISCORD="$(fetch_secret "${OCID_STEWIE_DISCORD_BOT_TOKEN}")"

cat > "${RUNTIME_DIR}/app-agent.env" <<EOF
TZ=Africa/Nairobi
OPENROUTER_API_KEY=${APP_OPENROUTER}
GROQ_API_KEY=${APP_GROQ}
DISCORD_BOT_TOKEN=${APP_DISCORD}
CHROME_BIN=/usr/bin/chromium-browser
PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
EOF

cat > "${RUNTIME_DIR}/stewie.env" <<EOF
TZ=Africa/Nairobi
OPENROUTER_API_KEY=${APP_OPENROUTER}
GROQ_API_KEY=${APP_GROQ}
DISCORD_BOT_TOKEN=${STEWIE_DISCORD}
CHROME_BIN=/usr/bin/chromium-browser
PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
EOF

chmod 600 "${RUNTIME_DIR}/app-agent.env" "${RUNTIME_DIR}/stewie.env"

echo "Vault secrets fetched and runtime env files created in ${RUNTIME_DIR}."
