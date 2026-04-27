# The Two-Headed Agent: Why Stewie and App-Agent Kept Fighting Over the Same House

At some point in the build I stopped thinking about OpenClaw as one thing. It was not one thing.

It was Stewie on one side, the app-agent on the other, and me in the middle trying to figure out why they kept stepping on each other’s toes.

That is the part nobody tells you when you are wiring up two agents at once: the problem is not usually the code. The problem is the boundaries. When the boundaries are vague, everything starts to look haunted. Ports overlap, logs mix together, and suddenly you are not sure whether the bot is broken, the backend is broken, or your mental model is the broken part.

The fix was not glamorous. I gave each service its own port, its own log stream, and its own job. Once I stopped pretending they could share the same emotional space, the whole system calmed down.

## The Receipts

The screenshots show the mess and the fix in the order I lived it:

- `img-14-dual-container-overview.png` — both containers visible and running
- `img-15-port-mapping-for-each-agent.png` — separate ports instead of shared chaos
- `img-16-agent-specific-log-streams.png` — logs split by service so I could think again
- `img-17-role-boundary-diagram.png` — the simple role split I should have started with
- `img-18-independent-health-checks.png` — each service proving itself on its own

## What I Learned

Two agents only work when their responsibilities are clear enough that the failure is obvious.

Once Stewie was handling the conversational side and app-agent was handling the task side, debugging got much less personal. The whole thing stopped feeling like two services were fighting and started feeling like a system with rules.

That is usually what good orchestration looks like. It is not louder. It is clearer.

## The Commands That Helped

```bash
docker ps --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}"
docker logs stewie_gateway --tail 50
docker logs app_agent_gateway --tail 50
```

```bash
netstat -ano | findstr 18789
netstat -ano | findstr 18889
```

When I needed to confirm each agent separately, I tested the endpoint one at a time instead of assuming the combined setup was healthy.
