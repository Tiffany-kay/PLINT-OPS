# I Connected Discord to OpenClaw in 48 Hours… by Ignoring the Docs First 🤡

**Subtitle:** A beginner-friendly, funny, and practical guide to fixing OpenClaw + Discord setup mistakes (permissions, allowlists, IDs, and gateway restarts).

---

## Cover Image Suggestion
- Use text: **“48 HOURS. ONE MISSING STEP.”**
- Visual: split screen of Discord errors on one side and working Stewie reply on the other.

---

## Quick Context
I’m learning agentic AI as a beginner and running OpenClaw locally (no heavy server setup).

I originally connected OpenClaw to WhatsApp, but Discord looked way more organized for task separation:
- `#research`
- `#build`
- `#ops`
- `#random-panic`

So I connected Discord and named my bot **Stewie**.

Everything looked perfect.

Everything was not perfect.

---

## What You’ll Learn
By the end of this post, you’ll know how to avoid the exact mistakes I made:
1. Over-trusting YouTube setup shortcuts
2. Misunderstanding Discord permissions
3. Missing OpenClaw guild allowlist setup
4. Forgetting Developer Mode and IDs
5. Not restarting gateway after config updates

---

## The Story: How I Broke It Before I Fixed It

### Phase 1 — YouTube confidence boost ✅
I started with a YouTube tutorial instead of documentation.

To be fair, it guided me through:
- Discord Developer Portal
- bot creation
- OAuth URL generation
- getting token
- inviting bot to server

I pinged Stewie in my default channel and got replies.

I started planning my “I am now an integration engineer” victory speech.

**Image 1 (Place right here):** `img-01-working-default-channel.png`  
*Caption:* “The trap: one channel worked, so I assumed the entire setup was correct.”

---

### Phase 2 — The Administrator permission trap ❌
The video used **Administrator** permission for the bot.

I thought that meant “all good forever.”

But in my second channel, Stewie kept saying he couldn’t create/access channels properly. I was sending emotional “hello?” messages and receiving permission failures.

The OpenClaw docs recommend specific scopes/permissions, not random overpowered settings.

**Image 2 (Place right here):** `img-02-oauth-admin-selected.png`  
*Caption:* “I gave Admin and still failed. Power is not precision.”

**Image 3 (Place right here):** `img-03-permission-error-in-channel.png`  
*Caption:* “Second channel energy: me typing, bot refusing, chaos loading.”

---

### Phase 3 — I forgot the guild allowlist 🤦‍♀️
This is where my 48-hour debug arc began.

I eventually read the docs and noticed OpenClaw guild workspace setup includes a **guild allowlist** step.

My default channel happened to work, but broader guild behavior wasn’t fully configured.

**Image 4 (Place right here):** `img-04-config-before-guild-allowlist.png`  
*Caption:* “Before fix: only part of the workspace behavior was effectively enabled.”

---

### Phase 4 — Developer Mode + IDs were missing
The tutorial skipped a critical step:
- Enable Discord Developer Mode
- Copy required IDs
- Share IDs for OpenClaw setup flow

I had to provide IDs and then inspect config changes.

I noticed only the initially working channel context was reflected. I added my second channel ID too.

Still no response.

**Image 5 (Place right here):** `img-05-developer-mode-toggle.png`  
*Caption:* “The hidden boss level: IDs.”

**Image 6 (Place right here):** `img-06-config-after-adding-ids.png`  
*Caption:* “Config looked better. Bot still ghosted me. Character development.”

---

### Phase 5 — The gateway restart plot twist 🔁
After all that, it still didn’t work.

Final fix? Restart gateway.

Yes. Restart.

I lost 48 hours to what eventually became a one-command ending.

**Image 7 (Place right here):** `img-07-gateway-restart-command-log.png`  
*Caption:* “The command that ended my villain arc.”

**Image 8 (Place right here):** `img-08-second-channel-working.png`  
*Caption:* “Second channel finally working. I forgave technology (temporarily).”

---

## The Practical Fix Checklist (Copy This)
If your first channel works but others don’t, run this order:

1. Verify Discord app + bot are created correctly
2. Enable privileged intents (especially Message Content)
3. Confirm OAuth scopes include:
   - `bot`
   - `applications.commands`
4. Use explicit bot permissions from docs (least privilege, not assumptions)
5. Enable Developer Mode in Discord
6. Copy and provide correct IDs:
   - Server ID
   - User ID
   - relevant channel IDs (if needed)
7. Configure guild allowlist in OpenClaw
8. Restart gateway after config changes
9. Re-test in both default and non-default channels

---

## Minimal Commands To Remember
```bash
openclaw config set channels.discord.enabled true --strict-json
openclaw gateway
```

If already running as a service/background process:

```bash
openclaw gateway restart
```

> Note: Keep bot tokens secret. Use env-backed config and never paste secrets in chat/public screenshots.

---

## Beginner Lessons I Learned the Hard Way
- YouTube can start you fast; docs finish the job correctly.
- “One channel works” is not a full integration test.
- IDs are not optional details.
- Allowlists are real gatekeepers.
- Restarting services is a valid debugging skill, not a personality flaw.

---

## Series Roadmap: The 5-Post Version (Raw Data, Polished Delivery)
If you want this story to stand out, publish it as a 5-post series with a sober technical tone plus controlled humor.

### Post 1: Infrastructure as a Prison
**Angle:** Oracle Cloud is powerful, but networking defaults can feel like a fortress that forgot who lives inside it.

**Core points:**
- Ingress rules that look right but still block your flow
- VCN/subnet/security-list mismatch traps
- Why "open port" does not always mean reachable service

**Tone line:** "I thought I was deploying an agent. Turns out I was applying for parole."

### Post 2: The Two-Headed Agent
**Angle:** Running `app-agent` and `stewie` together is orchestration, not duplication.

**Core points:**
- Isolated containers and identities
- Port collisions as "two services, one door"
- Why role boundaries matter for reliability and security

**Tone line:** "They were not fighting emotionally. They were fighting over port real estate."

### Post 3: Permission Hell
**Angle:** `EACCES` is not a random curse; it is ownership and mount semantics enforcing Linux reality.

**Core points:**
- File ownership vs runtime user mismatch
- Mounted config files that look editable but are effectively locked
- Fixing write paths so the bot can persist state safely

**Tone line:** "My bot had thoughts, but no write access to its diary."

### Post 4: Shadow Networking
**Angle:** Browser security is doing its job; we had to approach the dashboard through trusted paths.

**Core points:**
- Why raw public IP + auth + origin checks can fail
- SSH tunneling as the sane, secure bridge
- Device identity, secure context, and token handling in plain language

**Tone line:** "We did not break browser security. We stopped arguing with it."

### Post 5: Clean Post-Mortem
**Angle:** Great engineering is not "no mess." It is disciplined cleanup that makes the final repo intentional.

**Core points:**
- Splitting product vs ops concerns
- Redacting secrets and removing noisy artifacts
- Presenting a clean, credible Git history

**Tone line:** "The build was chaotic. The repo does not have to confess everything."

---

## Git Push Plan (Do Not Leak Keys)
Use GPT-5.4 mini for grunt cleanup, but do not allow blind edits to `.gitignore`.

### Critical pre-push check
```bash
git status
```

If you see `openclaw.json` or any file containing Discord tokens (`MTQ5...`) or OpenRouter keys in `modified`/`untracked`, stop immediately.

Then:
1. Add those paths/patterns to `.gitignore`
2. Re-run `git status`
3. Only proceed when secrets are no longer staged or tracked

Security reminder: We did not spend hours securing the gateway just to leak keys in one push.

### Split workflow right now
Initialize the ops repository:

```bash
mkdir ~/plint-ops
cp -r ~/agents/ ~/plint-ops/
cd ~/plint-ops
git init
```

Clean the product repository:
1. Remove `agents` and `openclaw-skills` from the main product repo.
2. Keep product-facing code and docs focused on shipping the app.

---

## My Final Setup (Now Working)
- OpenClaw running locally
- Discord connected for structured channel-based task workflows
- Stewie responds in intended channels after correct permissions, allowlist, IDs, and gateway restart

I came for easy orchestration.
I stayed for unexpected humility.

---

## Image Placement Plan (Fast Reference)
1. Working default channel reply
2. OAuth page showing Admin-based approach (what went wrong)
3. Second-channel permission error
4. Config before guild allowlist completion
5. Developer Mode toggle
6. Config after IDs/allowlist updates
7. Gateway restart logs
8. Successful second-channel reply
9. (Optional) Final channel structure screenshot

---

## Screenshot Safety Checklist
Before publishing, blur or redact:
- bot token
- full server/user/channel IDs (partially mask at minimum)
- personal avatar/email
- internal project names if private

---

## SEO Pack
**SEO Title Options (pick one):**
1. I Connected Discord to OpenClaw Wrong for 48 Hours So You Don’t Have To
2. From Admin Permission to Actual Permission: My OpenClaw Discord Debug Story
3. Beginner Guide: Fixing OpenClaw Discord Channel Issues After a Broken Setup
4. How I Broke and Fixed Discord Integration for OpenClaw (With Real Errors)
5. I Followed YouTube, Ignored Docs, and Debugged OpenClaw for 2 Days

**Meta Description:**
I connected Discord to OpenClaw as a beginner, made classic setup mistakes, and spent 48 hours debugging. Here’s what broke, why, and the exact sequence that fixed every channel.

**Suggested Tags:**
- `openclaw`
- `discord`
- `debugging`
- `beginners`
- `aiagents`

---

## Social Promo Copy
### X (Twitter)
I spent 48 hours debugging OpenClaw + Discord because I trusted a video before docs 😭

One channel worked, second channel ghosted me, and the fix was: permissions + allowlist + IDs + gateway restart.

I wrote a beginner-friendly breakdown with real mistakes and exact fixes:
[insert link]

### LinkedIn
I published a beginner-friendly technical write-up on integrating Discord with OpenClaw, including real mistakes that caused multi-channel failures.

Key lessons:
- Administrator permission ≠ correct integration setup
- Guild allowlist + correct IDs are critical
- Gateway restart may be required for config changes to apply

I included the full debug sequence and a practical checklist.
Read it here: [insert link]

---

## CTA (Use at End of Article)
If your first Discord channel works but others fail, drop your symptom in the comments and I’ll share the exact debug order I now use.
