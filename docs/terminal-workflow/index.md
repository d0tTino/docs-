---
title: "Terminal Workflow"
tags: [command-line, workflow]
project: terminal-workflow
updated: 2025-08-07
---

!!! note "Disclaimer"
    This document is provided for research purposes only and does not constitute legal advice. It also does not constitute financial advice.
# Getting started

This area collects notes on command-line tools and shell tips for daily
development. More workflow examples will be added over time. For a broader
overview of the docs repo, see [the main index](../index.md).

[[toc]]

## Setup
1. Install core tools
    ```sh
    brew install tmux zsh git
    ```
2. Clone a project
    ```sh
    git clone git@github.com:example/project.git
    ```

## Daily Usage
1. Start a tmux session
    ```sh
    tmux new -s dev
    ```
2. Sync latest changes
    ```sh
    git pull
    ```

!!! tip "Common pitfalls"
    - SSH keys not loaded? `ssh-add -l` shows active keys.
    - Tools missing from `PATH`? Check with `echo $PATH`.

## tmux

`tmux` is a terminal multiplexer that lets you run multiple sessions and panes in one terminal window.

**Typical use cases**

- Keep long-running tasks running after disconnection.
- Organize multiple shells in a single session.
- Share a terminal session with collaborators.

```sh
# Create a new session named "dev"
tmux new -s dev

# Split the window horizontally
tmux split-window -h

# Detach while leaving processes running
tmux detach
```

## zsh

`zsh` is a feature-rich shell offering advanced completions, prompts, and scripting capabilities.

**Typical use cases**

- Customize the shell environment with themes and plugins.
- Navigate directories with powerful tab completion.
- Write scripts using extended shell features.

```sh
# Add an alias for a detailed directory listing
echo "alias ll='ls -alF'" >> ~/.zshrc

# Apply the new configuration
source ~/.zshrc
```

## git

`git` is a distributed version control system for tracking changes in source code.

**Typical use cases**

- Manage project history and branching.
- Collaborate through pull requests and code reviews.
- Revert to previous versions when needed.

```sh
# Stage modified files
git add .

# Commit with a concise message
git commit -m "Update project files"

# Push to the main branch
git push origin main
```

## Example Session

![Screenshot of an example terminal session](../img/example-session.svg){data-glightbox}

