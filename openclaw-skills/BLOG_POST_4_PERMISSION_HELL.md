# Permission Hell: Why EACCES Was a System Design Problem, Not a Random Error

## Positioning
Post 4 of 5 in the OpenClaw Discord debugging series.

## TL;DR
Permission failures were caused by ownership and mount semantics, not by bad luck. The runtime user could not write where the process expected to persist state.

## Symptom Pattern
- Config looked correct.
- Service started.
- Runtime actions failed with write errors.
- Restarting did not help because ownership stayed wrong.

## Root Cause
The container runtime user and mounted file ownership did not match. The process could read, but not persist updates.

## Stable Fix Pattern
1. Confirm runtime UID/GID.
2. Check ownership and permissions on mounted paths.
3. Move writable data to a path owned by runtime user.
4. Avoid editing mounted configs from incorrect user context.
5. Re-run with least privilege and explicit writable directories.

## Proof of Work (Required Assets)
Add these files:

1. `img-19-permission-error-eacces-log.png`
   - Proof: real `EACCES` or write-denied log.
2. `img-20-runtime-user-and-uid.png`
   - Proof: container user identity (`id`, `whoami`).
3. `img-21-mounted-path-permissions-before-fix.png`
   - Proof: `ls -la` on mounted path before fix.
4. `img-22-mounted-path-permissions-after-fix.png`
   - Proof: permission state after fix.
5. `img-23-successful-write-after-fix.png`
   - Proof: successful state/config write operation.

## Image Placement Map
- Put Images 19-21 in incident timeline.
- Put Image 22 in remediation section.
- Put Image 23 in verification section.

## Practical Takeaway
Permissions are architecture. If write paths are not designed intentionally, reliability collapses under load.

## SEO
- Suggested title: Permission Hell: Solving EACCES in OpenClaw With Correct Ownership and Mount Design
- Meta description: A practical Linux/container permission debugging guide for OpenClaw deployments.
- Tags: `linux`, `permissions`, `containers`, `openclaw`, `sre`
