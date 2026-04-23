# Oracle ARM + OpenClaw Agent Runbook

This runbook deploys two isolated agents on Oracle Free Tier:
- plintcart-app-agent (production app operations)
- stewie-personal-agent (personal assistant)

## 1) Region Strategy
Start with these in order:
1. eu-frankfurt-1 (primary)
2. uk-london-1 (backup)
3. af-johannesburg-1 (backup)

If you hit "Out of host capacity":
1. Try 2 OCPU / 12 GB RAM first.
2. Switch Availability Domain.
3. Retry in backup region.
4. Retry during off-peak UTC hours.

## 2) Create Oracle Instance
Recommended baseline:
- Shape: VM.Standard.A1.Flex
- CPU/RAM: 2 OCPU / 12 GB
- OS: Ubuntu 24.04 LTS
- Boot volume: 50 to 100 GB

Open only SSH initially.

## 3) Install Docker on VM
Run on VM:

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker
```

## 4) Copy Deployment Folder
Copy this folder to VM:
- infra/oracle

Then on VM:

```bash
cd oracle
mkdir -p runtime data/app-agent data/stewie logs/app-agent logs/stewie
chmod +x scripts/fetch-secrets.sh
```

## 5) OCI Vault Setup
### 5.1 Create Vault resources
In OCI Console:
1. Create Vault in your compartment.
2. Create a Key.
3. Create Secrets for:
   - OPENROUTER_API_KEY
   - GROQ_API_KEY
   - APP_AGENT_DISCORD_BOT_TOKEN
   - STEWIE_DISCORD_BOT_TOKEN

Store each secret OCID.

### 5.2 Dynamic Group for VM
Create Dynamic Group with matching rule (example):

```text
ALL {instance.compartment.id = '<your_compartment_ocid>'}
```

Use tighter rules if needed (single instance ID).

### 5.3 IAM Policy
Create policy in root/tenancy policy scope (adjust names):

```text
Allow dynamic-group plint-agent-dg to read secret-family in compartment <your_compartment_name>
Allow dynamic-group plint-agent-dg to read vaults in compartment <your_compartment_name>
Allow dynamic-group plint-agent-dg to read keys in compartment <your_compartment_name>
```

## 6) Install OCI CLI on VM

```bash
bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)" -- --accept-all-defaults
export PATH="$HOME/bin:$PATH"
oci --version
```

## 7) Fetch Secrets from Vault (Instance Principal)
Export your secret OCIDs on VM:

```bash
export OCID_OPENROUTER_API_KEY='ocid1.secret.oc1..xxxx'
export OCID_GROQ_API_KEY='ocid1.secret.oc1..xxxx'
export OCID_APP_AGENT_DISCORD_BOT_TOKEN='ocid1.secret.oc1..xxxx'
export OCID_STEWIE_DISCORD_BOT_TOKEN='ocid1.secret.oc1..xxxx'
```

Run bootstrap script:

```bash
./scripts/fetch-secrets.sh
```

Expected output:
- runtime/app-agent.env
- runtime/stewie.env

Both files are chmod 600.

## 8) Build and Start Agents

```bash
docker compose build
docker compose up -d
```

Check status:

```bash
docker compose ps
docker logs -f plintcart-app-agent
docker logs -f stewie-personal-agent
```

## 9) Browser Automation Notes
Browser dependencies are baked into Dockerfile.
For stability:
1. Keep browser tasks in app-agent only.
2. Add explicit task-level rate limits in identity/config.
3. Prefer read-first automation before write actions.

## 10) Secret Rotation Workflow
1. Add new secret version in OCI Vault.
2. Re-run:

```bash
./scripts/fetch-secrets.sh
docker compose restart app-agent stewie
```

3. Verify logs and channel behavior.
4. Retire old secret version.

## 11) Operational Guardrails
1. Keep app-agent and stewie env files separate.
2. Keep identity folders separate.
3. Never commit runtime env files.
4. Restrict inbound ports until domain/reverse proxy phase.

## 12) Domain Later (Phase 2)
When ready:
1. Add Nginx or Caddy reverse proxy.
2. Add TLS (Let's Encrypt).
3. Expose only required endpoints.
4. Keep Discord-driven operations behind channel auth.

## 13) Troubleshooting
### "Out of host capacity"
- Switch AD, lower CPU/RAM, or switch region.

### Vault access denied
- Recheck dynamic group match rule and policy scope.
- Confirm OCI CLI uses instance principal in script.

### Gateway lock / zombie process
If running in Docker, restart container rather than killing host processes:

```bash
docker compose restart app-agent
docker compose restart stewie
```
