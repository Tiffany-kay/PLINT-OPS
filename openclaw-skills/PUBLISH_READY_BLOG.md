# I Connected Discord to OpenClaw Wrong for 48 Hours. Here Is the Exact Fix Path.

I thought I had the Discord setup handled. One channel was talking to Stewie, so naturally I assumed the rest of the server would behave the same way. It did not. The integration looked fine at first, but the missing pieces were scattered across permissions, IDs, the guild allowlist, and a gateway restart I should have done much earlier.

The strange part is how convincing the setup looked when I first tested it. The default channel replied, which made the whole thing feel finished. Then I moved to another channel and the cracks showed immediately. That was the moment I stopped treating it like a random bug and started treating it like an incomplete configuration.

What fixed it was not clever. It was a proper cleanup of the basics: I rechecked the Discord app setup, used the right OAuth scopes, enabled Developer Mode, copied the IDs I had skipped, updated the OpenClaw guild allowlist, and restarted the gateway so the new config could actually take effect. The problem was never dramatic. It was just spread across a few small things that all had to line up.

The screenshots in this post tell that story in order. First the working default channel, then the failure in the second channel, then the config changes, and finally the successful reply after the restart. If you are stuck on the same thing, follow the same order. It saves time and keeps you from chasing ghosts.

## Screenshots in This Post
- `img-01-working-default-channel.png` - the first channel replying normally
- `img-02-oauth-scopes-and-permissions.png` - the OAuth setup I used
- `img-03-second-channel-permission-failure.png` - the failure that showed up next
- `img-04-openclaw-config-before-allowlist.png` - config before the allowlist was right
- `img-05-discord-developer-mode-and-ids.png` - Developer Mode and copied IDs
- `img-06-openclaw-config-after-id-update.png` - config after the IDs were added
- `img-07-gateway-restart-log.png` - the restart that made the change stick
- `img-08-second-channel-success.png` - the second channel finally working

If you want the short version, it was not a permissions problem alone and it was not an OpenClaw problem alone. It was a small stack of things that all needed to be correct at the same time.
