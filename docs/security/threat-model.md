---
title: "Threat Model"
tags: [security, docs]
project: docs-hub
updated: 2025-08-15
---
--8<-- "_snippets/disclaimer.md"

# Documentation and Scripts Threat Model

## Assets

- Public documentation site
- Build and deployment scripts
- Source repository and configuration

The diagram below illustrates how documentation moves from contributors through the build pipeline to public users.

![Documentation flows from developers and their repository through CI to a static site that is hosted for public users.](threat-model.svg)

*Flow of documentation from developers to users via CI and hosting.*

**Boundary legend:**

- **Contributors** — Developer space and repository where docs originate.
- **CI** — Automated system that builds the documentation site.
- **Public** — Hosting environment delivering the static site to users.

**Diagram description:** Developers work within the Contributors boundary and commit documentation to the repository. After review, changes cross into the CI boundary where the system builds the docs into a static site. The resulting site then crosses the trust boundary into the Public environment for hosting and user access.

## Potential Threats

| Threat | Impact | Likelihood | Severity | Mitigation | Status |
|--------|--------|------------|----------|------------|--------|
| Unauthorized doc changes or defacement | Medium | Medium | 🟧 Medium | Version control and review | Monitored |
| Script injection | High | Low | 🟥 High | - Restrict permissions<br>- Validate deps | Mitigated |
| Credential leak | High | Low | 🟥 High | - Scan for secrets<br>- Rotate credentials | Mitigated |

**Severity legend**

| Symbol | Severity |
|--------|----------|
| 🟩 | Low |
| 🟧 | Medium |
| 🟥 | High |

### Verification Steps

- **Unauthorized modification or defacement of docs**
  - Confirm each pull request has at least one reviewer.
  - Run [`scripts/setup_hooks.sh`](../../scripts/setup_hooks.sh) to enable repository-specific hooks.
- **Malicious code injection in scripts**
  - Verify script files have appropriate execute permissions.
  - Audit dependencies with `npm audit` (see [package.json](../../package.json)) and `pip install --require-hashes -r` [`requirements.txt`](../../requirements.txt).
- **Leakage of credentials or sensitive data**
  - Scan commits with [GitLeaks](https://github.com/gitleaks/gitleaks) or similar tools before merging.
  - Rotate credentials according to the organization's security policy.

