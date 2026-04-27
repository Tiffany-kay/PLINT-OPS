# Shadow Networking to Clean Postmortem: The Week I Stopped Fighting Security Controls

The last part of the story was not about hacking around anything. It was about respecting the controls that were already there and using them properly. Public access kept getting blocked by origin and auth expectations, so I stopped forcing it and used SSH tunneling as the clean bridge to the dashboard instead.

That shift mattered. The moment I started validating access locally first, the debugging became much more predictable. I could see the tunnel, the gateway, and the browser behavior separately instead of guessing at everything at once. Once the access path was stable, I turned to cleanup.

Cleanup was not an afterthought. It was the final part of the fix. I kept the product repo focused on the app, moved the operational material into `plint-ops`, documented secret handling, and tightened the ignore rules so I would not have to revisit the same mess later. That part is boring in the best possible way.

## Screenshots in This Post
- `img-24-ssh-tunnel-command-and-success.png` - the tunnel running correctly
- `img-25-localhost-dashboard-http-200.png` - the dashboard responding locally
- `img-26-origin-policy-log-before-fix.png` - the origin rejection before the fix
- `img-27-branch-cleanup-and-push.png` - the branch cleanup step
- `img-28-plint-vs-plint-ops-structure.png` - the product/ops split
- `img-29-secret-ignore-rules.png` - the secret safety rules
- `img-30-final-pr-merge-view.png` - the final PR merge view

The bigger lesson was not that security controls are annoying. It is that stable systems come from working with them instead of pretending they are optional.
