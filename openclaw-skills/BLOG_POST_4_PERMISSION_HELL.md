# Permission Hell: Why `EACCES` Felt Like the Container Was Gaslighting Me

There are errors that are annoying, and then there are permission errors that feel personal.

This one started like a lie. The service booted. The config looked right. Everything seemed normal until the first time the runtime tried to write something and the container basically shrugged and said no.

That was the ugly part: the app was not dead. It could see the path. It just could not use it. The runtime user and the mounted files were not aligned, so every write attempt turned into a reminder that ownership matters more than optimism.

Once I stopped treating it like random container drama and looked at the actual UID, mount ownership, and writable paths, the fix became plain. The process needed somewhere it could write, and that path needed to belong to the user actually running the service.

## The Receipts

The screenshots show the whole situation without me having to relive it twice:

- `img-19-permission-error-eacces-log.png` — the write failure that started the headache
- `img-20-runtime-user-and-uid.png` — the runtime identity I had to check
- `img-21-mounted-path-permissions-before-fix.png` — the wrong ownership state
- `img-22-mounted-path-permissions-after-fix.png` — the corrected permission setup
- `img-23-successful-write-after-fix.png` — the moment the write finally worked

## What I Learned

Permissions are not a side quest.

They are part of the design. If the runtime cannot write where it needs to write, the app will fail in the most boring and stubborn way possible. And once you fix it properly, the whole system gets quieter immediately.

## The Commands That Helped

```bash
id
whoami
ls -la /home/node/.openclaw
ls -la /home/node/.openclaw/workspace
```

```bash
sudo chown -R 10001:10001 /home/node/.openclaw/workspace
sudo chmod -R u+rwX /home/node/.openclaw/workspace
```

If the writable path itself was wrong, I moved the state to a path the runtime user could actually own and write to.
