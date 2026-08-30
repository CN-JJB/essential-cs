# Repository Architecture

The repository is Markdown-first. The website, if built later, is a generated view rather than the canonical source.

## Intended top-level areas

- `book/` — canonical teaching explanations.
- `course/` — learner path, stages, checkpoints, reading/lab/project sequencing.
- `labs/` — runnable experiments that reveal mechanisms.
- `project/` — evolving Mini Cloud App and System Defense.
- `research/` — Module Research Dossiers and source investigations.
- `meta/` — curriculum engineering: status, decisions, maps, policies, prompts, audits, handoffs.
- `instructors/` — optional teacher/study-group support later.
- `.github/` — Issue/PR templates and CI/workflow infrastructure.

## Source rules

- Standard Markdown is canonical for educational prose.
- Code lives in separate runnable files/projects where practical.
- Editable diagram source should be preserved (Mermaid/SVG/etc.) when practical.
- MDX, notebooks, and interactives are used only when they add educational value.
- Avoid duplicating canonical explanations across `book/`, `course/`, `labs/`, and `project/`.

Directories should gain local `AGENTS.md` files only when specialized instructions materially help; avoid instruction sprawl.
