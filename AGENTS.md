# Pryntor GPU procurement gate

Before proposing **new paid GPU compute**, follow the company policy: https://docs.google.com/document/d/1oRi8PG4VPBw08cCllV5fwEHGAUgD1PM9pgdLCb9D4qE/edit and the versioned Markdown at https://github.com/LLoliwe/agent-spend-proof/blob/main/docs/GPU_COST_GATE.md .

Use https://gpu.context.dev for **read-only** price discovery only when a job is demonstrably GPU-bound. Compare direct vendor offers, real availability, actual configuration, credits/CPU alternatives and total cost per successful run. Record in PRY-223. No self-hosting, billing, procurement, cloud activation, or unverified savings claims. Preserve existing QA and project controls.

## Optional Pryntor Anatomy skill — interactive technical explainers (PRY-225)

When a task benefits from an interactive, physically grounded SVG, WebGL, or experimental 3D explanatory figure, **make the official Anatomy skill available to the agent** through the centrally audited Pryntor installer:

- Upstream source (MIT): https://github.com/wheresryan22/anatomy
- Pinned revision: `e9488296a44211c42701ff71705b7901470ec78f`
- Canonical installer/runbook: https://github.com/LLoliwe/Anthropic-skills/tree/main/skills/pryntor-anatomy
- Install in an appropriate checkout (when actually needed): `bash /path/to/Anthropic-skills/skills/pryntor-anatomy/install.sh .`
- **Optional, not a runtime dependency.** Do not install or execute remote code automatically on ordinary startup, overwrite an existing agent skill, add GPU spend, or publish designs to third-party galleries. Pin and inspect the source and confirm installed SHA.
- For prototypes: match motion, labels and numerical outputs to an independently testable model; check desktop/mobile, keyboard, reduced motion, contrast, accessibility and actual screenshots. 3D renders are **not** validated engineering, safety, or physics simulations.
- Triage by project relevance; protect customer, merchant, learner and company-private data. No claim of deployment, test pass, customer adoption or revenue without evidence.
