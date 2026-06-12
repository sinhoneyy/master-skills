#!/usr/bin/env node
// master-skills installer — copies skills into the path your host expects.
// Zero dependencies (Node built-ins only).
//
//   npx master-skills --claude
//   npx master-skills --cursor --category security,backend
//   npx master-skills --path ./my-skills --risk safe,none

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const PKG = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const SKILLS = path.join(PKG, "skills");
const INDEX = path.join(PKG, "skills_index.json");

// Default install path + first-use hint per host. Override any with --path.
const TOOLS = {
  claude:      { path: "~/.claude/skills",     use: ">> /<name> …" },
  cursor:      { path: "~/.cursor/skills",     use: "@<name> …" },
  gemini:      { path: "~/.gemini/skills",     use: "Use <name> to …" },
  codex:       { path: "~/.codex/skills",      use: "Use <name> to …" },
  antigravity: { path: "~/.antigravity/skills", use: "Use @<name> to …" },
  agy:         { path: "~/.agy/skills",        use: "/<name> …" },
  kiro:        { path: "~/.kiro/skills",       use: "@<name> …" },
  opencode:    { path: ".agents/skills",       use: "opencode run @<name> …" },
  adal:        { path: ".adal/skills",         use: "Use <name> to …" },
};

const C = { dim: "\x1b[2m", b: "\x1b[1m", g: "\x1b[32m", y: "\x1b[33m", r: "\x1b[31m", x: "\x1b[0m" };

function parseArgs(argv) {
  const out = { tool: null, path: null, category: null, risk: null, dry: false, help: false, list: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--help" || a === "-h") out.help = true;
    else if (a === "--list") out.list = true;
    else if (a === "--dry-run") out.dry = true;
    else if (a === "--path") out.path = argv[++i];
    else if (a === "--category") out.category = argv[++i];
    else if (a === "--risk") out.risk = argv[++i];
    else if (a.startsWith("--") && TOOLS[a.slice(2)]) out.tool = a.slice(2);
    else if (a.startsWith("--")) { console.error(`Unknown flag: ${a}`); process.exit(1); }
  }
  return out;
}

const expand = (p) => p.startsWith("~") ? path.join(os.homedir(), p.slice(1)) : p;

function readRisk(id) {
  try {
    const t = fs.readFileSync(path.join(SKILLS, id, "SKILL.md"), "utf8");
    const m = t.match(/^---[\s\S]*?\nrisk:\s*["']?([a-zA-Z]+)/m);
    return m ? m[1].toLowerCase() : "unknown";
  } catch { return "unknown"; }
}

function help() {
  console.log(`${C.b}master-skills${C.x} — 2,658 skills for any AI agent\n`);
  console.log(`${C.b}Usage${C.x}\n  npx master-skills --<tool> [--category a,b] [--risk safe,none] [--dry-run]`);
  console.log(`  npx master-skills --path <dir> [...filters]\n`);
  console.log(`${C.b}Tools${C.x}`);
  for (const [t, c] of Object.entries(TOOLS))
    console.log(`  ${C.g}--${t.padEnd(12)}${C.x}${C.dim}→ ${c.path}${C.x}`);
  console.log(`  ${C.g}--path <dir>${C.x}   ${C.dim}custom install location${C.x}\n`);
  console.log(`${C.b}Filters${C.x}`);
  console.log(`  --category   integrations,backend,security,…  (15 domains)`);
  console.log(`  --risk       safe,none,unknown\n`);
  console.log(`${C.dim}Default tool paths are best-effort; use --path to match your host exactly.${C.x}`);
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || (!args.tool && !args.path && !args.list)) return help();

  const index = JSON.parse(fs.readFileSync(INDEX, "utf8"));

  if (args.list) {
    const cats = Object.entries(index.categories).sort((a, b) => b[1] - a[1]);
    console.log(`${C.b}Categories${C.x} (${index.skill_count} skills)`);
    for (const [c, n] of cats) console.log(`  ${c.padEnd(20)} ${C.dim}${n}${C.x}`);
    return;
  }

  const dest = expand(args.path || TOOLS[args.tool].path);
  const cats = args.category ? new Set(args.category.split(",").map(s => s.trim())) : null;
  const risks = args.risk ? new Set(args.risk.split(",").map(s => s.trim().toLowerCase())) : null;

  let selected = index.skills;
  if (cats) selected = selected.filter(s => cats.has(s.category));
  if (risks) selected = selected.filter(s => risks.has(readRisk(s.id)));

  if (!selected.length) { console.error(`${C.r}No skills matched your filters.${C.x}`); process.exit(1); }

  console.log(`${C.b}master-skills${C.x} → ${dest}`);
  console.log(`${C.dim}installing ${selected.length} skill(s)${cats ? ` · category=${[...cats].join(",")}` : ""}${risks ? ` · risk=${[...risks].join(",")}` : ""}${C.x}\n`);

  if (args.dry) {
    selected.slice(0, 20).forEach(s => console.log(`  ${C.dim}would copy${C.x} ${s.id}`));
    if (selected.length > 20) console.log(`  ${C.dim}… and ${selected.length - 20} more${C.x}`);
    return;
  }

  fs.mkdirSync(dest, { recursive: true });
  let n = 0;
  for (const s of selected) {
    fs.cpSync(path.join(SKILLS, s.id), path.join(dest, s.id), { recursive: true });
    n++;
    if (n % 250 === 0) process.stdout.write(`${C.dim}  ${n}/${selected.length}\r${C.x}`);
  }

  console.log(`${C.g}✔${C.x} installed ${C.b}${n}${C.x} skills to ${dest}`);
  if (args.tool) console.log(`${C.dim}first use: ${TOOLS[args.tool].use}${C.x}`);
}

main();
