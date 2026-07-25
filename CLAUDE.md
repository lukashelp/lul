# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository state

This repository is currently empty of source code. It contains only:
- `README.md` — placeholder content ("# lul", "test")
- `LICENSE` — Apache License 2.0
- `.gitignore` — a generic Flash/ActionScript template (`bin/`, `obj/`, `*.swf`, `*.air`, `*.ipa`, `*.apk`, etc.); it does not necessarily reflect the stack that will actually be used here

There is no build system, package manifest, source directory, or test suite yet. There are no established commands to build, lint, or test, and no architecture to document.

## Guidance for future work

When code is added to this repository, update this file with:
- The actual language/framework/toolchain chosen
- Commands to build, lint, and run tests (including running a single test)
- High-level architecture — how the major pieces fit together — once that structure exists

Do not assume a stack from the `.gitignore` alone; confirm with the user or with whatever project files get added before treating this as a Flash/ActionScript project.
