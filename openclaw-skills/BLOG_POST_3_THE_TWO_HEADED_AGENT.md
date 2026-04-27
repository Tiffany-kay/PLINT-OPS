# The Two-Headed Agent: Running Stewie and App-Agent Without Port Wars

Once I split the system into two agents, the whole setup started making more sense. Stewie handled the conversational side, and the app-agent handled the task side. That sounds obvious now, but at the time it felt like I was trying to make two different personalities share one desk and one notebook.

The problems showed up quickly when the boundaries were vague. Ports overlapped, logs blended together, and I could not tell whether I was debugging the bot, the backend, or the glue between them. The moment I gave each service its own space and treated them like separate responsibilities instead of one giant blob, the setup became much easier to reason about.

What helped most was not just assigning different ports. It was giving each agent a clear job, a clear name, and a clear way to fail on its own without dragging the other one down with it. That made the system calmer, and it made me calmer too.

## Screenshots in This Post
- `img-14-dual-container-overview.png` - both containers running with distinct names
- `img-15-port-mapping-for-each-agent.png` - separate port mapping
- `img-16-agent-specific-log-streams.png` - logs separated by service
- `img-17-role-boundary-diagram.png` - the simple role map I used
- `img-18-independent-health-checks.png` - each service passing on its own

The real lesson here is that two agents only work when the boundaries are obvious. Once the boundaries are obvious, the debugging gets a lot less emotional.
