# Shadow Networking to Clean Postmortem: How I Stopped Fighting Security Controls

There was a point in the build where direct access kept failing and I had to admit something annoying: the browser was not the enemy. The security controls were doing exactly what they were supposed to do.

That does not make them less frustrating. It just makes them correct.

So I stopped trying to bully the dashboard into working through the wrong path and switched to SSH tunneling and localhost-based access. The second I did that, the whole problem became more legible. I could see the tunnel, the gateway, and the browser behavior separately instead of trying to decode one giant failure blob.

Once the access path was stable, the cleanup work started to matter just as much. I separated the product repo from the ops repo, documented the secret handling, and tightened the ignore rules so I would not leak my own infrastructure while trying to ship the story.

## The Receipts

The images for this one are the proof trail:

- `img-24-ssh-tunnel-command-and-success.png` — the tunnel working the way it should
- `img-25-localhost-dashboard-http-200.png` — the dashboard answering locally
- `img-26-origin-policy-log-before-fix.png` — the origin rejection before I fixed the path
- `img-27-branch-cleanup-and-push.png` — the cleanup and push step
- `img-28-plint-vs-plint-ops-structure.png` — the product/ops split
- `img-29-secret-ignore-rules.png` — the ignore rules that keep the repo honest
- `img-30-final-pr-merge-view.png` — the final merge view once it was all clean

## What I Learned

The fastest way to stop fighting security controls is to work with them instead of pretending they are optional.

The real win was not just getting the dashboard open. It was ending with a setup I could explain, trust, and hand to someone else without shame.

## The Commands That Helped

```bash
ssh -i ~/.ssh/your-key.pem -N -L 18789:127.0.0.1:18789 ubuntu@YOUR_VM_IP
curl -I http://127.0.0.1:18789
```

```bash
git status
git add .gitignore openclaw-skills
git commit -m "docs: clean blog series and screenshot index"
git push origin cleanup-20260424
```

```bash
git grep -n "openclaw.json\|#token=\|OPENROUTER_API_KEY" -- .
```

That last check kept me from accidentally turning a cleanup story into a secret-leak story.
