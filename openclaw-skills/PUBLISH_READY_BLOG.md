# I Connected Discord to OpenClaw Wrong for 48 Hours. Here Is the Exact Fix Path.

## Subtitle
A beginner-friendly, technical post on why one Discord channel worked, others failed, and how permissions, allowlists, IDs, and gateway restart fixed it.

## TL;DR
My first channel worked, so I assumed the integration was done. It was not. The real issue was incomplete setup across Discord permissions, OpenClaw guild allowlist, missing IDs, and a required gateway restart.

## Why This Post Exists
If your bot replies in one channel but fails in another, you do not have a random bug. You usually have a configuration mismatch.

This post gives a concrete debug order so you do not waste the same 48 hours.

## What Broke
1. I trusted a shortcut tutorial more than docs.
2. I over-relied on Administrator permission.
3. I skipped guild allowlist details.
4. I had missing Discord IDs in config.
5. I changed config without restarting gateway.

## What Fixed It
Use this exact order:

1. Validate Discord app and bot setup.
2. Enable required intents (especially Message Content).
3. Verify OAuth scopes: `bot`, `applications.commands`.
4. Apply least-privilege permissions from docs.
5. Enable Discord Developer Mode.
6. Capture and configure IDs:
   - Server ID
   - Bot user ID
   - Channel IDs that must respond
7. Configure OpenClaw guild allowlist.
8. Restart gateway.
9. Re-test in at least two channels.

## Minimal Commands
```bash
openclaw config set channels.discord.enabled true --strict-json
openclaw gateway restart
```

## Lessons Learned
- One working channel is not integration success.
- Administrator permission does not replace correct bot scopes and channel rules.
- Allowlists and IDs are system boundaries, not optional metadata.
- Restarting gateway is part of applied debugging, not superstition.

## Proof of Work (Required Assets)
Add these 8 images in this order. Keep the filenames exactly as written:

1. `img-01-working-default-channel.png`
   - Proof: bot replies in the first channel.
2. `img-02-oauth-scopes-and-permissions.png`
   - Proof: OAuth scopes and selected bot permissions.
3. `img-03-second-channel-permission-failure.png`
   - Proof: failure in non-default channel before fix.
4. `img-04-openclaw-config-before-allowlist.png`
   - Proof: config state before guild allowlist completion.
5. `img-05-discord-developer-mode-and-ids.png`
   - Proof: Developer Mode enabled and IDs copied.
6. `img-06-openclaw-config-after-id-update.png`
   - Proof: config includes required IDs.
7. `img-07-gateway-restart-log.png`
   - Proof: restart command or log line with restart event.
8. `img-08-second-channel-success.png`
   - Proof: successful reply in second channel after fix.

## Image Placement Map
- Place Images 1-3 in the problem narrative section.
- Place Images 4-6 in the configuration section.
- Place Image 7 in the restart section.
- Place Image 8 in the validation/results section.

## Redaction Rules Before Publish
Mask or blur:
- Bot token
- Full server/user/channel IDs (leave first 4-6 chars visible only)
- API keys and headers
- Personal email/avatar if visible

## Closing
I did not need more tools. I needed a stricter debug order.

If your first channel works but others fail, follow the checklist above in sequence and you will usually resolve it quickly.

## SEO
- Suggested title: I Connected Discord to OpenClaw Wrong for 48 Hours. Here Is the Exact Fix Path.
- Meta description: A practical OpenClaw and Discord debug guide: permissions, IDs, allowlist, gateway restart, and a complete proof-backed fix sequence.
- Tags: `openclaw`, `discord`, `debugging`, `aiagents`, `devops`
