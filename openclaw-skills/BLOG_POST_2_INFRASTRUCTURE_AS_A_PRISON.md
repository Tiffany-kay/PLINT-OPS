# Infrastructure as a Prison: Why My Open Ports Still Did Not Work

I used to think opening a port was the same as making a service accessible. It is not. That is the short version of a very annoying lesson I learned while trying to make OpenClaw reachable from the outside world.

The service itself was alive. The container was running. Local checks on the VM looked fine. But the moment I moved from "running" to "reachable from my browser," the setup started failing in a way that felt unfair until I looked at the full path. The real problem was not one big blocker. It was a chain of small ones: cloud ingress, host firewall, service bind, and origin policy all had to agree.

That is why the debugging felt like walking through a building with too many locked doors. Every time I fixed one layer, another layer would remind me it was still in charge. Once I started testing the path end-to-end instead of assuming one open port was enough, the problem got much easier to understand.

## Screenshots in This Post
- `img-09-docker-ps-with-port-mapping.png` - the container and port mapping
- `img-10-local-curl-200-on-vm.png` - the service responding locally on the VM
- `img-11-cloud-ingress-rules.png` - the ingress rule side of the story
- `img-12-host-firewall-rules.png` - the host firewall side of the story
- `img-13-origin-not-allowed-log.png` - the browser/origin failure that kept showing up

The useful takeaway was simple: open ports are not the finish line. The finish line is a browser request making it all the way through the chain and getting a real response back.
