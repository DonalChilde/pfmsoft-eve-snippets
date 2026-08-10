# Solo Dev Git Workflow — dev/main Reference

A reference for the day-to-day loop and the dev → main release process.
Philosophy: explicit over implicit — every step below is a deliberate action, not something left to happen automatically.

## Day-to-day loop (feature work)

1. **Open an issue first.** Title, description, labels (`bug`, `enhancement`, `refactor`). Write it for future-you with zero context.
2. **Branch off `dev`, not `main`.**
   ```
   git checkout dev
   git pull
   git checkout -b 58-short-description
   ```
3. **Work in VS Code with Copilot.** Use it for boilerplate, scaffolding, repetitive patterns. Make the architectural/design decisions yourself. Review every suggestion before accepting.
4. **Commit frequently with real messages.** Small, descriptive commits — not `wip`.
5. **Push and open a PR into `dev`.**
   ```
   git push -u origin 58-short-description
   ```
   Reference the issue: `Closes #58`. Request Copilot as a PR reviewer.
6. **Review the diff yourself**, then **squash-merge** into `dev`. Delete the branch.
7. Issue auto-closes via `Closes #58`.

## Branch protection

- Protect **both** `dev` and `main` — not just `main`. Require PRs and passing CI on each.
- `dev` is where daily work lands; it needs the same guardrails or the PR workflow above loses its value.

## Release: promoting dev → main

This is a deliberate step, not a fast-forward push.

1. Open a PR from `dev` into `main`. Optionally track it as its own issue ("Release vX.Y.Z") so the release history is searchable the same way feature work is.
2. **Do not squash this merge.** Use a regular merge commit (`--no-ff`) so `main`'s history still shows the individual features that shipped. Squashing here collapses the whole release into one commit and loses per-feature traceability on `main`.
3. Bump the version number and update the CHANGELOG as part of this PR — not a separate afterthought commit.
   ```
   ./bump.sh patch
   ```
4. After merging, in the main branch, **tag the release**:
   ```
   git tag v0.3.0
   git push origin v0.3.0
   ```
   or
   ```
   ./tag.sh
   ```
5. Require CI to pass on this PR too. `main` should always be deployable.

## Hotfix exception path

The one case where you push to `main` outside a release cycle.

1. Branch directly off `main`:
   ```
   git checkout main
   git checkout -b hotfix/short-description
   ```
2. Fix, PR into `main`, merge (tag if it warrants a patch version).
3. **Merge the same fix back into `dev`.** This is the step that gets missed — if you skip it, the next `dev` → `main` release silently un-fixes the hotfix.

## Setting up "require PRs" on a branch (GitHub)

Branch protection rule (or ruleset), set up separately for `dev` and `main`:

1. Repo → **Settings** → **Branches** → **Add branch protection rule**.
2. Branch name pattern: `main` (repeat later for `dev`).
3. Check **"Require a pull request before merging."** Blocks direct pushes — everything goes through a PR.
   - "Require approvals" — 0 if solo and you don't want to block on self-approval; 1 if you want GitHub to force a formal self-approval click before merging (a forcing function to actually re-read the diff).
4. Optionally check **"Require status checks to pass before merging"** if CI (GitHub Actions) is set up — select the required checks. This is what actually enforces "main should always be deployable."
5. Optionally check **"Do not allow bypassing the above settings"** — without this, admins (you) can still push directly around the rule. Checking it closes that loophole.
6. Save. Repeat for the other branch.

CLI version (`gh api`), per branch:

```
gh api repos/{owner}/{repo}/branches/main/protection \
  --method PUT \
  --field required_pull_request_reviews[required_approving_review_count]=0 \
  --field enforce_admins=true \
  --field required_status_checks=null \
  --field restrictions=null
```

Note: with required approvals at 0, there's no real review gate — just the structural "must open a PR" requirement. Approvals=1 (and self-approving) adds a genuine forced pause before merge.

## Quick reference table

| Situation             | Branch from | PR into                      | Merge style                         |
| --------------------- | ----------- | ---------------------------- | ----------------------------------- |
| New feature / bug fix | `dev`       | `dev`                        | Squash                              |
| Release               | —           | `main`                       | Regular (`--no-ff`) + tag           |
| Hotfix                | `main`      | `main`, then back into `dev` | Regular, then squash/merge into dev |
