# Infrastructure as a Prison: Why My Open Ports Still Did Not Work

## Positioning
Post 2 of 5 in the OpenClaw Discord debugging series.

## TL;DR
Cloud networking can look open and still block real traffic. My deployment failed because security lists, subnet rules, and service bindings were not aligned end-to-end.

## The Core Problem
I opened ports and expected immediate access. But availability depends on a chain:

1. Instance firewall
2. VCN and subnet rules
3. Security list and ingress source
4. Service bind host and container mapping
5. Upstream origin and browser policy constraints

If one link is wrong, the system appears online but remains unusable.

## What Actually Happened
- Container showed healthy.
- Local health checks passed.
- Remote access behaved inconsistently.
- Dashboard requests failed due to origin and exposure constraints.

## Reliable Diagnosis Sequence
1. Confirm container process is running.
2. Confirm service binds expected host/port.
3. Confirm local VM curl to service endpoint returns `200`.
4. Confirm instance firewall allows inbound target port.
5. Confirm cloud ingress rule source and port range match client.
6. Confirm no competing process on same host port.
7. Confirm origin allowlist for control UI.

## Proof of Work (Required Assets)
Use these files as evidence in the post:

1. `img-09-docker-ps-with-port-mapping.png`
   - Proof: container and mapped ports are visible.
2. `img-10-local-curl-200-on-vm.png`
   - Proof: service works locally on VM.
3. `img-11-cloud-ingress-rules.png`
   - Proof: ingress rules and source CIDR.
4. `img-12-host-firewall-rules.png`
   - Proof: host-level port allowance.
5. `img-13-origin-not-allowed-log.png`
   - Proof: error logs confirming policy mismatch.

## Image Placement Map
- Put Images 9-10 in the "symptoms" section.
- Put Images 11-12 in the "network chain" section.
- Put Image 13 in the "root cause" section.

## Practical Takeaway
"Port open" is not success. "User path works from browser to service" is success.

## SEO
- Suggested title: Infrastructure as a Prison: Why Open Ports Still Failed My OpenClaw Deployment
- Meta description: A practical cloud networking postmortem covering ingress, firewall, service bind, and origin policy failures.
- Tags: `devops`, `networking`, `openclaw`, `cloud`, `debugging`
