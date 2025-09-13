# Copilot Cleanup Workflow

This directory contains tools to help clean up after GitHub Copilot agent work and properly manage branch workflows.

## The Problem

When GitHub Copilot agents create draft PRs on temporary branches, your local repository may still be carrying some of those changes, and you might not be on the main branch. This can lead to:

- Confusion about which branch you're on
- Uncommitted changes piling up
- Difficulty starting fresh Copilot sessions
- Commits landing in temporary branches instead of proper feature branches

## The Solution

A 3-step workflow that ensures you have a clean main branch to restart from:

### Step 1: Clean up your workspace
```bash
./dev/workspace-status
# or
make workspace-status
```

**What it does:**
- Checks git status for uncommitted changes  
- Offers to commit any pending work with a standard message
- Shows available branches and draft PRs
- Provides guidance on next steps

### Step 2: Merge the Copilot PR (if you want the changes)
```bash
./dev/pr-management  
# or
make pr-management
```

**What it does:**
- Opens GitHub PR page for review
- Lists local Copilot branches for cleanup
- Provides options to delete specific or all Copilot branches
- Guides you through PR merge/discard decisions

**Manual steps on GitHub:**
- Go to your GitHub repository
- Open the Pull Request created by Copilot (draft PRs)
- Review the changes
- If you're happy, click "Merge pull request" into main
- If not, close/delete the PR

### Step 3: Re-run your Copilot agent prompt
```bash
./dev/switch-to-main
# or  
make switch-to-main
```

**What it does:**
- Switches to main branch (creates if needed)
- Pulls latest changes from origin
- Ensures clean starting point
- Confirms you're ready for new Copilot work

```bash
./dev/copilot-restart
```

**What it does:**
- Verifies environment is ready
- Shows current git status and recent commits
- Provides tips for next Copilot session
- Confirms normal branch/PR workflow will work

## Complete Workflow

Run the entire process with one command:

```bash
./dev/copilot-cleanup
# or
make copilot-cleanup
```

This interactive script guides you through all steps with explanations and confirmations.

## Usage Examples

### After Copilot agent work:
```bash
# Check what state you're in
./dev/workspace-status

# Handle any draft PRs on GitHub, then:
./dev/pr-management

# Switch to clean main branch
./dev/switch-to-main

# Prepare for next session
./dev/copilot-restart
```

### Quick complete cleanup:
```bash
make copilot-cleanup
```

### Just switch to main:
```bash
make switch-to-main
```

## What This Enables

After running this workflow:

✅ **You're on main branch** - Status bar shows `main` at bottom left  
✅ **Working tree is clean** - No uncommitted changes  
✅ **Latest changes pulled** - Up to date with origin  
✅ **Normal workflow ready** - Commits will land in proper feature branches  

Now you can safely re-issue your Copilot agent role prompt, and any commits will land in a normal branch/PR workflow instead of piling up in a temporary detached branch.

## Files

- `copilot-cleanup` - Master interactive workflow script
- `workspace-status` - Step 1: Check and clean workspace  
- `pr-management` - Step 2: Manage Copilot PRs
- `switch-to-main` - Step 3: Switch to main branch
- `copilot-restart` - Step 4: Prepare for restart

All scripts are also available as Makefile targets with `make` prefix.