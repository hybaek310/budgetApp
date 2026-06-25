---
name: csv-cli-accounting
description: Work on the CSV-based Python CLI budget app in this repository, including TDD-driven implementation, test design, and complexity-aware refactoring.
---

# CSV CLI Accounting

Use this skill when working on this repository's Python CLI budget app.

## Core workflow

1. Read the existing CLI, CSV parsing, and test files.
2. Write or update tests before implementation.
3. Keep functions small, typed, and easy to review.
4. Check cyclomatic complexity before finalizing changes.
5. Run the relevant test commands after each change set.

## Project rules

- Use type hints for every function and method.
- Keep each function at 50 lines or fewer.
- Keep cyclomatic complexity at 10 or below.
- Prefer small pure functions over large branching functions.

## Validation

- Primary test command: `pytest`
- Complexity check: `radon cc`
- Before committing, send the diff to the `qa_engineer` subagent for review.

## When to use this skill

- Adding a CLI command
- Changing CSV parsing or validation
- Updating transaction summaries or reports
- Refactoring code to satisfy TDD or complexity constraints
