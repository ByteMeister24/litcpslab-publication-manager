# Agent Instructions

## Project

This repository implements a **Publication Management System** that downloads lists of publications along with metadata from various publisher websites and convert them to markdown files based on a user-defined schema.

A combination of author name and author affilitions are used as serach queries to find relevant publications.

---

## Repository Map

- [src/](/src/) — implementation
- [tests](/tests/) — automated tests
- [docs](/docs/) — supporting documentation
- [data](/data/) — raw csv and processed markdown files

Do not infer architectural ownership solely from the current source-tree structure. Use the specifications as the authoritative source when relevant.

---

## Scope and Access

### Read allowed

You are allowed to read files under the following directories:

- [src/](/src/)
- [tests](/tests/)
- [docs](/docs/)
- [data](/data/)

### Approval required

Explicit user approval is required creating, modifying, moving, or deleting files under:

- [src/](/src/)
- [tests](/tests/)
- [docs](/docs/)
- [data](/data/)

### Off limits

Do not edit, update, or delet the following files:

- [gitignore](/.gitignore)
- [environment variables](/.env)

---

## Implementation Rule

Before making any substantive decision:

1. identify the scope of the task
2. locate the relevant project-wide specification
3. locate the relevant feature context, if one exists
4. read only the context needed for that task
5. implement against those authoritative sources

Do not load the full project context by default.
