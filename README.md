# jacobliberman.github.io

## Resume updates (automated)

- **Source of truth:** `resume/resume.json` (everything on the page: meta, header, contact, sections, footer). **Shell:** global HTML frame and asset links live in `resume/shell.template.html` (change rarely).
- **On push:** the [Build resume](.github/workflows/build-resume.yml) workflow runs when those files (or the build script) change on `main`/`master`, regenerates root `index.html`, and commits it if needed.
- **Local preview:** `python scripts/build_resume.py` (stdlib only; no install step).

If the workflow cannot push, check **Settings → Actions → General → Workflow permissions** and allow **Read and write** for the default `GITHUB_TOKEN`.
