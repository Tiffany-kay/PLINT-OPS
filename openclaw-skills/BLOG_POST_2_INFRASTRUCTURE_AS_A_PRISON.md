# Infrastructure as a Prison: How Oracle Cloud Gaslit Me About Open Ports

I used to think mapping a port in Docker and exposing it was the finish line.

That was before Oracle Cloud introduced me to its layered trust issues.

This was the part of the OpenClaw build where my autonomous agents (`app-agent` and `stewie`) were fully alive on an ARM VM in Frankfurt, but the dashboard still behaved like the service did not exist.

Containers were running. Local checks passed. The VM looked healthy. Browser access was a graveyard.

What made this frustrating was not one obvious mistake. It was a chain of nearly-correct systems that each needed one more thing before they would cooperate.

Debugging it felt less like engineering and more like escaping a prison where every unlocked door reveals another locked door.

## The Layers of Hell (With Receipts)

### 1. The False Sense of Security
`img-09-docker-ps-with-port-mapping.png` and `img-10-local-curl-200-on-vm.png`

This is the part that wastes the most time.

Docker says `0.0.0.0:18789->18789`. Local curl returns `HTTP 200`. Netstat agrees the port is listening.

Inside the VM, everything looks perfect.

From my browser outside the VM: timeout.

The service was not down. It was trapped behind the next layer.

### 2. The Oracle VCN Trap
`img-11-cloud-ingress-rules.png`

Oracle defaults are secure, but they are not friendly.

You have to explicitly allow ingress for the exact ports and source range. I added rules for the required ports and expected immediate success.

Still failed.

Because VCN ingress only gets traffic to your instance boundary. It does not guarantee your OS will accept or route it.

### 3. The Ubuntu Betrayal
`img-12-host-firewall-rules.png`

Even with cloud rules fixed, host firewall policy can silently drop packets.

That was my next wall.

I had to verify and adjust local firewall/iptables behavior so inbound traffic could actually reach the process.

Cloud open does not mean host open.

It just means the argument moved one layer deeper.

### 4. The Browser Gaslighting Finale
`img-13-origin-not-allowed-log.png`

After network path fixes, I expected instant victory.

Instead: `origin not allowed` and secure-context behavior around raw IP access.

At this point the packets were arriving, but policy rejected the session. The gateway and browser were both enforcing rules, and my access pattern did not satisfy them.

The practical fix was to use the correct trusted access path (SSH tunnel/localhost flow) and align allowed origins with how I was actually connecting.

This was the last lock.

## The Commands That Actually Helped

These are the kinds of commands that made the problem visible and then fixed it.

### Check the container and port mapping
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
docker logs stewie_gateway --tail 80
```

### Confirm the service is really alive on the VM
```bash
curl -i http://127.0.0.1:18789
netstat -ano | findstr 18789
```

### Open the host firewall path on Ubuntu
```bash
sudo ufw status verbose
sudo ufw allow 18789/tcp
sudo ufw allow 18889/tcp
```

If `ufw` was not the active firewall, I checked and adjusted `iptables` instead:

```bash
sudo iptables -L -n -v
sudo iptables -I INPUT -p tcp --dport 18789 -j ACCEPT
sudo iptables -I INPUT -p tcp --dport 18889 -j ACCEPT
```

### Restart the service after config or firewall changes
```bash
docker restart stewie_gateway
docker restart app_agent_gateway
```

### Verify the browser access path
```bash
ssh -i ~/.ssh/your-key.pem -N -L 18789:127.0.0.1:18789 ubuntu@YOUR_VM_IP
```

Then I opened the dashboard through `http://localhost:18789` instead of fighting the raw public IP.

## What Actually Solved It

1. Confirm local service health from inside the VM first.
2. Open the right Oracle ingress rules for the exact ports.
3. Verify host firewall policy on the VM, not just cloud policy.
4. Stop using random access paths; use one consistent path (tunnel/localhost) for dashboard control.
5. Align gateway origin rules with the real access origin.

## Quick Oracle Console Rule

If you want the exact shape of the Oracle ingress rule, it looked like this in concept:

```text
Source CIDR: 0.0.0.0/0
Protocol: TCP
Destination Port: 18789
Destination Port: 18889
```

The important part was not the console clicks. It was making the cloud layer, host layer, and browser layer agree on the same path.

That sequence turned chaos into a stable path.

## The Real Takeaway

Open ports are not a switch you flip. They are a negotiation across layers.

The finish line is not "container running." The finish line is a browser request surviving cloud ingress, host firewall, service bind, and origin policy, then returning a real payload.

If someone says "it works on the VM," ask one follow-up:

"Works from where?"
