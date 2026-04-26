# Shadow Networking to Clean Postmortem: The Week I Stopped Fighting Security Controls

## Positioning
Post 5 of 5 in the OpenClaw Discord debugging series.

## TL;DR
The final fixes were not hacks. They were disciplined operations: secure tunnel usage, origin-aware access, repository cleanup, and secret hygiene.

## Part 1: Shadow Networking
Direct public access kept failing due to origin/auth constraints. SSH tunneling provided a stable, secure bridge for local dashboard access.

Operational rules that worked:
1. Use explicit local-to-remote port forwarding.
2. Keep tunnel and gateway logs visible in separate terminals.
3. Validate with localhost requests before browser workflow.
4. Keep origin expectations aligned with gateway configuration.

## Part 2: Clean Postmortem and Repo Split
After stabilization, cleanup mattered as much as fixes:
- Product code stayed in `plint`.
- Ops artifacts moved to `plint-ops`.
- Secret handling was documented.
- Ignore rules were hardened.

## Proof of Work (Required Assets)
Add these files:

1. `img-24-ssh-tunnel-command-and-success.png`
   - Proof: tunnel command and successful bind.
2. `img-25-localhost-dashboard-http-200.png`
   - Proof: local dashboard reachable.
3. `img-26-origin-policy-log-before-fix.png`
   - Proof: pre-fix origin rejection log.
4. `img-27-branch-cleanup-and-push.png`
   - Proof: branch and push workflow.
5. `img-28-plint-vs-plint-ops-structure.png`
   - Proof: clear split between product and ops repos.
6. `img-29-secret-ignore-rules.png`
   - Proof: `.gitignore` secret patterns.
7. `img-30-final-pr-merge-view.png`
   - Proof: PR merged to `main`.

## Image Placement Map
- Put Images 24-26 in networking section.
- Put Images 27-29 in cleanup section.
- Put Image 30 in final outcomes section.

## Practical Takeaway
Reliable engineering means two things at once:
- shipping a fix,
- leaving behind a clean operational story that another engineer can trust.

## SEO
- Suggested title: Shadow Networking to Clean Postmortem: How I Stabilized OpenClaw and Cleaned the Repo
- Meta description: A practical final post on SSH tunneling, origin policy, secret safety, and repo separation after production debugging.
- Tags: `security`, `devops`, `openclaw`, `git`, `postmortem`
