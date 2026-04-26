# Proof of Work Image Checklist (All 5 Posts)

Use this as your publishing checklist for the full week.

## Global Redaction Rules
Before uploading any screenshot, blur or mask:
- API keys and tokens
- Full IDs (server/user/channel). Keep first 4-6 chars only.
- Personal emails and private usernames
- Internal hostnames if they expose infrastructure

## Post 1 (Discord Integration)
- `img-01-working-default-channel.png`
- `img-02-oauth-scopes-and-permissions.png`
- `img-03-second-channel-permission-failure.png`
- `img-04-openclaw-config-before-allowlist.png`
- `img-05-discord-developer-mode-and-ids.png`
- `img-06-openclaw-config-after-id-update.png`
- `img-07-gateway-restart-log.png`
- `img-08-second-channel-success.png`

## Post 2 (Infrastructure)
- `img-09-docker-ps-with-port-mapping.png`
- `img-10-local-curl-200-on-vm.png`
- `img-11-cloud-ingress-rules.png`
- `img-12-host-firewall-rules.png`
- `img-13-origin-not-allowed-log.png`

## Post 3 (Two-Headed Agent)
- `img-14-dual-container-overview.png`
- `img-15-port-mapping-for-each-agent.png`
- `img-16-agent-specific-log-streams.png`
- `img-17-role-boundary-diagram.png`
- `img-18-independent-health-checks.png`

## Post 4 (Permission Hell)
- `img-19-permission-error-eacces-log.png`
- `img-20-runtime-user-and-uid.png`
- `img-21-mounted-path-permissions-before-fix.png`
- `img-22-mounted-path-permissions-after-fix.png`
- `img-23-successful-write-after-fix.png`

## Post 5 (Shadow Networking + Postmortem)
- `img-24-ssh-tunnel-command-and-success.png`
- `img-25-localhost-dashboard-http-200.png`
- `img-26-origin-policy-log-before-fix.png`
- `img-27-branch-cleanup-and-push.png`
- `img-28-plint-vs-plint-ops-structure.png`
- `img-29-secret-ignore-rules.png`
- `img-30-final-pr-merge-view.png`

## Minimum Evidence Standard Per Image
Every image should prove one of these:
1. A failure state (before)
2. A change action (during)
3. A successful result (after)

If an image does not prove one of the three, remove it.
