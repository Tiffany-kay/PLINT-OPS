# Permission Hell: Why EACCES Was a System Design Problem, Not a Random Error

At some point in the week I ran into a classic `EACCES` problem, and it had that special kind of frustration that only permission errors can give you. The service looked fine. The config looked fine. The failure only showed up when the process actually tried to write something.

That was the part that finally clicked for me: the process could see the path, but it could not own the path. So the setup was not really broken in a dramatic way. It was just misaligned with how the runtime user and the mounted files were supposed to work together.

Once I stopped trying to treat it like a random glitch and looked at the UID, the mount, and the writable paths, the fix became obvious. The process needed a place it could actually write to, and the ownership had to match the user running the container. After that, the errors stopped feeling mysterious.

## Screenshots in This Post
- `img-19-permission-error-eacces-log.png` - the first failure message
- `img-20-runtime-user-and-uid.png` - the runtime user identity
- `img-21-mounted-path-permissions-before-fix.png` - the bad ownership state
- `img-22-mounted-path-permissions-after-fix.png` - the corrected permissions
- `img-23-successful-write-after-fix.png` - the write working again

The lesson here was simple: permissions are not a side detail. They are part of the system design, and if you get them wrong, the whole app reminds you in the least polite way possible.
