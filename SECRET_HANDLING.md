# Secret handling and safe-commit checklist

> Before committing or pushing `plint-ops`, follow these steps to ensure no secrets are leaked.

1. Confirm `.gitignore` is present and includes `openclaw.json`, keys and env files.
2. Search the repo for common secret strings:

```powershell
# from repository root
# Find files mentioning 'openclaw' or token fragments
git grep -n "openclaw" || echo 'no matches'
git grep -n "#token=" || echo 'no matches'
# Search for common provider env names
git grep -n "OPENROUTER\|OPENAI_API_KEY\|OPENAI" || true
```

3. If any secret files are tracked (appear in `git ls-files`), remove them from the index and keep them locally:

```powershell
# Example: remove tracked openclaw.json without deleting local file
git rm --cached -- "openclaw.json"
# Commit the removal
git commit -m "remove tracked secret: openclaw.json"
```

4. If secrets were exposed, rotate the credentials with the provider immediately.
5. Create a minimal `README.md` and `LICENSE` (if needed) then make the initial commit.

Optional: add a pre-commit hook to block secrets (recommended):

```bash
# simple pre-commit check (Unix-like)
cat > .git/hooks/pre-commit <<'HOOK'
#!/bin/sh
if git grep -n "openclaw\|#token=\|OPENROUTER\|OPENAI_API_KEY" -- . >/dev/null; then
  echo "Potential secret detected. Commit aborted."
  exit 1
fi
HOOK
chmod +x .git/hooks/pre-commit
```
