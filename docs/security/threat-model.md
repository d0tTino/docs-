---
title: "Threat Model"
tags: [security, docs]
project: docs-hub
updated: 2025-07-28
---

# Documentation and Scripts Threat Model

## Assets

- Public documentation site
- Build and deployment scripts
- Source repository and configuration

## Potential Threats

- Unauthorized modification or defacement of docs
- Malicious code injection in scripts
- Leakage of credentials or sensitive data

## Mitigations

- Use version control with code review to gate changes
- Restrict script permissions and validate dependencies
- Scan commits for secrets and rotate credentials regularly

## Security Tools

- [git-secrets](https://github.com/awslabs/git-secrets) – blocks committed secrets by scanning for credential patterns.
- [Semgrep](https://semgrep.dev) – SAST scanner that detects code vulnerabilities during CI.
