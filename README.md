# Awesome Agent Workspaces [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> Tools, patterns and resources for agent workspaces that survive past a single session.

Most agent tooling chases capability. Smarter agents, faster agents, agents that need less supervision. This list is about the other half, the part that decides whether any of that capability is still there tomorrow. Persistent memory, context management, evaluation, guardrails, orchestration discipline, observability, security. The scaffolding that turns a chat window into a workspace you can hand work to and come back to.

**In scope:** memory systems an agent reads and writes across sessions, context management and compaction, evaluation and benchmarks aimed at agents rather than raw model output, hooks and guardrails, orchestration and delegation discipline, skills and instruction-file management, observability and telemetry, security and permissions, and reference architectures that show a whole working setup.

**Out of scope:** generic agent frameworks, prompt collections, model lists, and one-shot demos. Those are well covered elsewhere and they are not what breaks when a workspace has to last.

**The bar.** Every entry clears three tests. It is *maintained*, meaning real activity within roughly the last twelve months. It is *documented*, meaning a reader can tell what it does, and how it differs from the entry above it, without cloning it. And it is genuinely about *workspace durability* rather than agent capability. Every entry earns its place. The list is deliberately small, and it will stay small. Rejected submissions are recorded in [REJECTIONS.md](REJECTIONS.md) with a reason, because the bar is the product.

A weekly CI check ([`scripts/check_maintained.py`](scripts/check_maintained.py)) flags any entry quieter than 90 days as a signal to review, well before it would actually cross the twelve-month bar above.

## Contents

- [Memory systems](#memory-systems)
- [Context management](#context-management)
- [Evaluation and benchmarks](#evaluation-and-benchmarks)
- [Hooks and guardrails](#hooks-and-guardrails)
- [Orchestration and delegation](#orchestration-and-delegation)
- [Skills and instruction management](#skills-and-instruction-management)
- [Observability and telemetry](#observability-and-telemetry)
- [Security and permissions](#security-and-permissions)
- [Reference architectures](#reference-architectures)
- [Learning resources](#learning-resources)

## Memory systems

- [mem0](https://github.com/mem0ai/mem0) - Extracts and consolidates facts out of conversations so an agent carries a compact memory forward instead of a growing transcript.
- [Graphiti](https://github.com/getzep/graphiti) - Builds temporal knowledge graphs that record when a fact became true and when it stopped being true, rather than overwriting it.
- [Letta](https://github.com/letta-ai/letta-code) - Gives agents memory blocks they edit themselves, continuing the MemGPT line of work on paging state through a fixed context window.
- [Hindsight](https://github.com/vectorize-io/hindsight) - Ships its agent memory alongside a public benchmark suite and a paper, so the retention claims can be checked rather than taken on trust.
- [Basic Memory](https://github.com/basicmachines-co/basic-memory) - Keeps memory as plain Markdown files on disk that a person can read, edit and diff next to the agent that wrote them.

## Context management

- [LLMLingua](https://github.com/microsoft/LLMLingua) - Compresses prompts and KV-cache to fit more useful context into the same window, with the compression ratios measured rather than asserted.
- [Claude Context](https://github.com/zilliztech/claude-context) - Indexes a codebase for semantic search over MCP so an agent retrieves the few relevant files instead of loading the tree.
- [Continuous Claude](https://github.com/parcadei/Continuous-Claude-v3) - Uses hooks to hold working state in ledgers and handoff files, so a task survives compaction and isolated sub-agent context windows.

## Evaluation and benchmarks

- [Inspect](https://github.com/UKGovernmentBEIS/inspect_ai) - Splits an evaluation into datasets, solvers and scorers, which makes an agent eval a reproducible artifact instead of a one-off script.
- [promptfoo](https://github.com/promptfoo/promptfoo) - Runs declarative prompt and agent test suites in CI, and turns the same targets into a red-teaming harness.
- [SWE-bench](https://github.com/SWE-bench/SWE-bench) - Scores agents on resolving real GitHub issues, using each repository's own test suite as the grader.
- [Harbor](https://github.com/harbor-framework/harbor) - Evaluates entire agent harnesses such as Claude Code and Codex CLI, not just the model underneath, across thousands of parallel sandboxes.

## Hooks and guardrails

- [Claude Code Hooks Mastery](https://github.com/disler/claude-code-hooks-mastery) - Worked examples of every Claude Code hook event, which is the gap between having read the hook docs and knowing what actually fires when.
- [cc-safety-net](https://github.com/kenryu42/cc-safety-net) - A hook that blocks destructive Git and filesystem commands and secret-file reads before they execute, across a dozen agent CLIs.
- [Guardrails](https://github.com/guardrails-ai/guardrails) - Wraps model input and output in validators that can block, retry or repair a response before it reaches anything downstream.
- [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) - Expresses conversational policy as programmable rails, so the constraint lives in a reviewable file instead of buried in prompt text.

## Orchestration and delegation

- [herdr](https://github.com/herdrdev/herdr) - Runs agent terminals inside a background server, so sessions outlive a closed lid or a reboot and a stuck agent is visibly marked as blocked.
- [Multica](https://github.com/multica-ai/multica) - Puts agents and people on one board where work is assigned, progress reported, blockers raised and output handed back for review.
- [Kiro Crew](https://github.com/kirodotdev/KiroCrew) - A development workspace built to continue past one session, with unattended multi-step tasks, recurring jobs and heartbeats that watch until something needs attention.
- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) - Imposes a planning and hand-off discipline across defined agent roles before any implementation is allowed to start.
- [AI-DLC Workflows](https://github.com/awslabs/aidlc-workflows) - Steering rules that break an agent's development work into verifiable, self-correcting stages with human checkpoints between them.

## Skills and instruction management

- [AGENTS.md](https://github.com/agentsmd/agents.md) - One open, predictable filename for the project instructions every coding agent reads, instead of a different dotfile for each vendor.
- [Agent Skills](https://github.com/anthropics/skills) - The Skills format plus reference implementations, which packages a procedure as a loadable file rather than another paragraph of prompt.
- [Superpowers](https://github.com/obra/superpowers) - Composable skills shipped with the bootstrap instructions that make an agent actually reach for them, across a dozen different agent CLIs.
- [agnix](https://github.com/agent-sh/agnix) - A linter and language server for the instruction layer itself, validating CLAUDE.md, AGENTS.md, SKILL.md, hook definitions and MCP config.

## Observability and telemetry

- [Langfuse](https://github.com/langfuse/langfuse) - Self-hostable tracing, datasets and prompt management, which keeps the trace store on infrastructure you control.
- [OpenLLMetry](https://github.com/traceloop/openllmetry) - Emits agent and model calls as OpenTelemetry spans so traces land in whatever monitoring stack already exists.
- [OpenTelemetry Semantic Conventions](https://github.com/open-telemetry/semantic-conventions) - Defines the vendor-neutral gen-ai span, metric and event attributes, agent and MCP conventions included, that make traces comparable across tools.
- [signal-sweep](https://github.com/signal-sweep/signal-sweep) - Sweeps public threads for questions a project's own documentation already answers, and gates every reply behind explicit per-comment human approval *(maintained by the list author)*.

## Security and permissions

- [Snyk Agent Scan](https://github.com/snyk/agent-scan) - Discovers the agents, MCP servers and skills installed on a machine and scans them for prompt injection and known vulnerabilities.
- [SkillSpector](https://github.com/NVIDIA/SkillSpector) - Inspects agent skills for malicious patterns, prompt injection and data-exfiltration paths before you install them, not after.
- [Claude Code Security Review](https://github.com/anthropics/claude-code-security-review) - A GitHub Action that reviews a pull request's diff for security problems, scoped to what actually changed.

## Reference architectures

- [agent-workspace-architecture](https://github.com/jimy-r/agent-workspace-architecture) - A redacted snapshot of one working agent workspace: roles library, typed memory, hooks, scheduled agents, delegation queue, self-audits and token budgeting *(maintained by the list author)*.
- [LifeOS](https://github.com/danielmiessler/LifeOS) - An opinionated personal harness built around durable context about its operator, published with its documentation and install path rather than described in a talk.
- [GBrain](https://github.com/garrytan/gbrain) - The memory and retrieval layer behind one operator's production agent fleet, including overnight consolidation and citation repair.

## Learning resources

- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) - Twelve principles for LLM software that survives production, written against the failure modes rather than against the demos.
- [Awesome Context Engineering](https://github.com/Meirtz/Awesome-Context-Engineering) - A survey of context engineering across papers, frameworks and implementation guides.
- [Awesome Agentic Patterns](https://github.com/nibzard/awesome-agentic-patterns) - A catalogue of recurring agentic patterns, named and described closely enough to argue about.
- [Awesome Claude Code](https://github.com/hesreallyhim/awesome-claude-code) - The broad resource list for Claude Code, useful as the wide net this list is deliberately not.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) first. One pull request per entry, and the three tests above decide it. Self-submissions are welcome and held to the same bar. Every rejection gets a one-line reason in the rejection log.

All entries verified 2026-08-27. Dead links and inactive projects are pruned by CI and by review.

To the extent possible under law, the maintainer has waived all copyright and related or neighboring rights to this work under [CC0 1.0](LICENSE).
