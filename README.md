<div align="center">

<br />

<img src="https://img.shields.io/badge/%F0%9F%93%9A_MASTER_SKILLS-f97316?style=for-the-badge&labelColor=0a0a0f" alt="Master Skills" height="52" />

<h1>Master&nbsp;Skills</h1>

<h3>The unified skill library for <b>Claude</b>, <b>Codex</b>, <b>Cursor</b>, <b>Antigravity</b> &amp; every AI agent.</h3>

<p><i>2,658 skills · 15 domains · one machine-readable catalog · zero dependencies</i></p>

<br />

[![CI](https://github.com/sinhoneyy/master-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/sinhoneyy/master-skills/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/sinhoneyy/master-skills?style=flat-square&color=f97316)](https://github.com/sinhoneyy/master-skills/releases)
[![License](https://img.shields.io/badge/license-MIT-22c55e?style=flat-square)](#-license)
[![Skills](https://img.shields.io/badge/skills-2%2C658-3b82f6?style=flat-square)](skills_index.json)
[![Domains](https://img.shields.io/badge/domains-15-f59e0b?style=flat-square)](#-the-15-domains)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-ec4899?style=flat-square)](#-contributing)

<br />

**[⚡ Install](#-install)** &nbsp;·&nbsp; **[🗂 Domains](#-the-15-domains)** &nbsp;·&nbsp; **[📦 Manifest](#-the-manifest)** &nbsp;·&nbsp; **[▶️ Usage](#️-using-a-skill)** &nbsp;·&nbsp; **[❓ FAQ](#-faq)**

</div>

<br />

```bash
npx skills add sinhoneyy/master-skills
```

<br />

---

## ✨ What is Master Skills

> **One source of truth for agent skills.** Instead of juggling scattered, inconsistent
> collections, you get a single clean catalog — deduplicated, domain-organized, and indexed.

Master Skills is a standardized catalog of **2,658 AI-agent skills**, sorted into
**15 normalized domains**. Every skill is **runtime-agnostic** — it works with **Claude,
Codex, Cursor, Antigravity**, and anything else that loads `SKILL.md` skills. Each one has
a stable id, version, domain, and slash trigger, all described in one authoritative
manifest: [`skills_index.json`](skills_index.json).

<table>
<tr>
<td align="center"><b>2,658</b><br/><sub>unique skills</sub></td>
<td align="center"><b>15</b><br/><sub>domains</sub></td>
<td align="center"><b>0</b><br/><sub>dependencies</sub></td>
<td align="center"><b>1</b><br/><sub>manifest file</sub></td>
</tr>
</table>

---

## ⚡ Install

**Option 1 — one command:**

```bash
npx skills add sinhoneyy/master-skills
```

**Option 2 — clone & point your agent at the folder:**

```bash
git clone https://github.com/sinhoneyy/master-skills.git
# then load the skills/ directory in your agent's skill loader
```

No build step, no install graph — it's a **static catalog**. ✅

---

## 🗂 The 15 domains

<div align="center">

| | Domain | Skills | What's inside |
|:--:| --- | --: | --- |
| 🔌 | `integrations` | **812** | App connectors, automation, webhooks |
| 🧰 | `general` | **421** | Cross-cutting, no single domain |
| ⚙️ | `backend` | **233** | APIs, servers, frameworks, GraphQL |
| 🧠 | `prompt-engineering` | **193** | Prompting, RAG, context, evaluation |
| ☁️ | `devops-cloud` | **160** | Docker, K8s, Terraform, AWS/Azure/GCP, CI/CD |
| 🤖 | `agents` | **154** | Multi-agent, orchestration, autonomous |
| 🎨 | `web-frontend` | **143** | React/Vue/Svelte/Angular, CSS, components |
| 📣 | `content-marketing` | **123** | SEO, copywriting, social, email |
| 🔐 | `security` | **98** | Pentest, vuln analysis, auth, crypto |
| 🖌️ | `design-ux` | **84** | Figma, canvas, brand, UI/UX |
| 🗄️ | `data-db` | **77** | SQL, Postgres/Mongo/Redis, pipelines |
| 🧪 | `testing` | **53** | Unit/E2E/TDD, Playwright, pytest |
| 📄 | `productivity` | **52** | PDF/XLSX/PPTX/DOCX, office, slides |
| 🧬 | `ai-ml` | **41** | Training, embeddings, vectors, NLP |
| 📱 | `mobile` | **14** | iOS, Android, Flutter, Swift, RN |

</div>

<sub>Live counts always reflect [`skills_index.json`](skills_index.json) → `categories`.</sub>

---

## 📦 The manifest

A single JSON document, [`skills_index.json`](skills_index.json), describes the entire library.

<details>
<summary><b>📋 Schema — top level</b></summary>

<br/>

| Field | Type | Description |
| --- | --- | --- |
| `name` | string | Always `"master-skills"` |
| `schemaVersion` | string | Manifest schema version |
| `version` | string | Library version |
| `generated` | string | ISO-8601 UTC build timestamp |
| `skill_count` | number | Total unique skills |
| `categories` | object | `{ domain: count }` |
| `skills` | object[] | One entry per skill |

</details>

<details>
<summary><b>🧩 Schema — per-skill entry</b></summary>

<br/>

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

</details>

```jsonc
{
  "name": "master-skills",
  "schemaVersion": "1.0",
  "skill_count": 2658,
  "categories": { "integrations": 812, "general": 421, "backend": 233, "…": 0 },
  "skills": [
    {
      "id": "api-design-principles",
      "name": "API Design Principles",
      "version": "1.0.0",
      "description": "Guidelines for designing clean, consistent APIs…",
      "category": "backend",
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
├─ 📂 skills/                    # the library, grouped by domain
│   ├─ integrations/<id>/SKILL.md
│   ├─ backend/<id>/SKILL.md
│   └─ …                         # 15 domains
├─ 🗂️ skills_index.json          # the manifest
├─ 📜 CREDITS.md                  # license/source notes + full upstream notices
└─ 📖 README.md
```

---

## ▶️ Using a skill

```
1.  Find it      →  search skills_index.json by id / trigger / category
2.  Open it      →  go to its "path", e.g. skills/backend/api-design-principles/
3.  Invoke it    →  use its "trigger" (/api-design-principles) in your agent
```

Each skill keeps its **full payload** — `SKILL.md`, references, scripts, examples — exactly
as published. Or just point your runtime's skill loader at the whole `skills/` directory.

---

## ❓ FAQ

<details>
<summary><b>How are skills organized?</b></summary>
<br/>
Into 15 normalized domains. A skill's domain comes from its frontmatter when it maps to a
known domain, otherwise a keyword heuristic, falling back to <code>general</code>.
</details>

<details>
<summary><b>How do I find a specific skill?</b></summary>
<br/>
Search <a href="skills_index.json"><code>skills_index.json</code></a> by <code>id</code>,
<code>category</code>, or <code>trigger</code> — it's a flat list designed to be grepped or
loaded programmatically.
</details>

<details>
<summary><b>Is the catalog self-contained?</b></summary>
<br/>
Yes. After cloning, everything you need is in <code>skills/</code> and the manifest — no
network access or build step required to use it.
</details>

---

## 🤝 Contributing

PRs are welcome! Good first contributions:

- ➕ Add new skills under the right `skills/<domain>/` folder
- 🏷️ Improve domain classification so fewer skills land in `general`
- 🧪 Add manifest validation or search tooling

> Every PR is automatically checked: the manifest is validated against the tree, and changed
> `SKILL.md` files are linted for structure — results posted right on your PR.

---

## 📜 License

The Master Skills catalog tooling is **MIT-licensed**. Bundled skills retain their original
upstream licenses — full notices live in [`CREDITS.md`](CREDITS.md).

<div align="center">
<br/>
<sub>Built as one unified catalog. No dependencies. No lock-in.</sub>
<br/><br/>

**[⬆ back to top](#)**

</div>
