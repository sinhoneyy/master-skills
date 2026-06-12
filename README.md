<div align="center">

<img src="https://img.shields.io/badge/%F0%9F%93%9A-Master%20Skills-f97316?style=for-the-badge&labelColor=0a0a0f" alt="Master Skills" height="46" />

# Master Skills

### The unified skill library for Claude, Codex, Cursor, Antigravity & other AI agents.

**2,658** skills · **15** domains — one machine-readable catalog.

[![License](https://img.shields.io/badge/license-MIT-22c55e.svg?style=flat-square)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-2,658-3b82f6.svg?style=flat-square)](skills_index.json)
[![Domains](https://img.shields.io/badge/domains-15-f97316.svg?style=flat-square)](#-the-15-domains)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-ec4899.svg?style=flat-square)](#-contributing)

[Install](#-install) · [Domains](#-the-15-domains) · [Manifest](#-the-manifest-skills_indexjson) · [Layout](#-repository-layout) · [FAQ](#-faq)

</div>

---

## 📖 Table of contents

- [What is Master Skills](#-what-is-master-skills)
- [Install](#-install)
- [The 15 domains](#-the-15-domains)
- [The manifest (`skills_index.json`)](#-the-manifest-skills_indexjson)
- [Repository layout](#-repository-layout)
- [Using a skill](#-using-a-skill)
- [FAQ](#-faq)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📚 What is Master Skills

Master Skills is a single, standardized catalog of **2,658 AI agent skills**, deduplicated
and organized into **15 normalized domains**. The skills are runtime-agnostic — they work
with **Claude, Codex, Cursor, Antigravity, and any other agent** that loads `SKILL.md`-based
skills. Every skill
has a stable id, version, domain, and slash trigger, all described in one authoritative
manifest you can ship to any agent runtime.

Instead of juggling many scattered, inconsistent skill collections, you get one source of
truth: a clean `skills/` tree grouped by domain and a queryable `skills_index.json`.

---

## 🚀 Install

One command:

```bash
npx skills add sinhoneyy/master-skills
```

Or clone the repo and point your agent's skill loader at the `skills/` folder. No build
step, no dependencies — it's a static catalog.

---

## 🗂 The 15 domains

Skills are bucketed into a bounded, normalized set of domains:

| Domain | Skills | What's inside |
| --- | ---: | --- |
| `integrations` | 812 | App connectors, automation, webhooks |
| `general` | 421 | Cross-cutting skills with no single domain |
| `backend` | 233 | APIs, servers, frameworks, GraphQL |
| `prompt-engineering` | 193 | Prompting, RAG, context, evaluation |
| `devops-cloud` | 160 | Docker, Kubernetes, Terraform, AWS/Azure/GCP, CI/CD |
| `agents` | 154 | Multi-agent, orchestration, autonomous patterns |
| `web-frontend` | 143 | React/Vue/Svelte/Angular, CSS, components |
| `content-marketing` | 123 | SEO, copywriting, social, email |
| `security` | 98 | Pentest, vuln analysis, auth, crypto, threat modeling |
| `design-ux` | 84 | Figma, canvas, brand, UI/UX |
| `data-db` | 77 | SQL, Postgres/Mongo/Redis, pipelines, analytics |
| `testing` | 53 | Unit/E2E/TDD, Playwright, pytest |
| `productivity` | 52 | PDF/XLSX/PPTX/DOCX, office, slides |
| `ai-ml` | 41 | Training, embeddings, vectors, NLP |
| `mobile` | 14 | iOS, Android, Flutter, Swift, React Native |

The authoritative, always-current counts live in [`skills_index.json`](skills_index.json)
under `categories`.

---

## 📦 The manifest (`skills_index.json`)

A single JSON document at the repo root describes the entire library.

### Top level

| Field | Type | Description |
| --- | --- | --- |
| `name` | string | Always `"master-skills"` |
| `schemaVersion` | string | Manifest schema version |
| `version` | string | Library version |
| `generated` | string | ISO-8601 UTC build timestamp |
| `skill_count` | number | Total unique skills |
| `categories` | object | `{ domain: count }` |
| `skills` | object[] | One entry per skill (below) |

### Per-skill entry

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Stable, slugified skill id |
| `name` | string | Human-readable name |
| `version` | string | Skill version (default `1.0.0`) |
| `description` | string | One-line summary |
| `category` | string | Assigned domain |
| `tags` | string[] | Tags, if any |
| `trigger` | string | Slash trigger, `/`+id |
| `path` | string | `skills/<domain>/<id>` |

```jsonc
{
  "name": "master-skills",
  "schemaVersion": "1.0",
  "version": "0.1.0",
  "skill_count": 2658,
  "categories": { "integrations": 812, "general": 421, "backend": 233, "…": 0 },
  "skills": [
    {
      "id": "api-design-principles",
      "name": "API Design Principles",
      "version": "1.0.0",
      "description": "Guidelines for designing clean, consistent APIs…",
      "category": "backend",
      "tags": [],
      "trigger": "/api-design-principles",
      "path": "skills/backend/api-design-principles"
    }
  ]
}
```

---

## 📁 Repository layout

```
master-skills/
├─ skills/                     # the library, grouped by domain
│  ├─ integrations/<id>/SKILL.md
│  ├─ backend/<id>/SKILL.md
│  └─ …                        # 15 domains
├─ skills_index.json           # the manifest
├─ CREDITS.md                  # license/source notes + full upstream notices
└─ README.md
```

---

## ▶️ Using a skill

Each skill keeps its full payload — `SKILL.md`, references, scripts, examples. To use one:

1. Find it in [`skills_index.json`](skills_index.json) by `id`, `trigger`, or `category`.
2. Open its folder at the listed `path`, e.g. `skills/backend/api-design-principles/`.
3. Invoke it by its `trigger` (e.g. `/api-design-principles`) in your agent, or point your
   runtime's skill loader at the `skills/` directory.

---

## ❓ FAQ

**How are skills organized?**
Into 15 normalized domains. A skill's domain comes from its frontmatter when it maps to a
known domain, otherwise from a keyword heuristic, falling back to `general`.

**How do I find a specific skill?**
Search [`skills_index.json`](skills_index.json) by `id`, `category`, or `trigger` — it's a
flat list designed to be grepped or loaded programmatically.

**Is the catalog self-contained?**
Yes. After cloning, everything you need is in `skills/` and the manifest — no network
access or build step required to use it.

---

## 🧭 Roadmap

- [ ] Curated lightweight pack (core domains only)
- [ ] Manifest validation tooling
- [ ] Search/filter UI wired to `skills_index.json`
- [ ] Per-skill content de-duplication (by hash)

---

## 🤝 Contributing

PRs are welcome. Good first contributions:

- Add new skills under the appropriate `skills/<domain>/` folder.
- Improve domain classification so fewer skills land in `general`.
- Add manifest validation or search tooling.

---

## 📜 License

The Master Skills catalog tooling is MIT-licensed. Bundled skills retain their original
upstream licenses — full notices are in [`CREDITS.md`](CREDITS.md).
