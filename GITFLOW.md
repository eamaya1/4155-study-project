# Gitflow Workflow

We follow Gitflow to structure our repository and manage our development process. The Gitflow model uses several types of branches with specific roles:
## Main Branch

**main**:
This branch always reflects a production-ready state. All stable releases are tagged on this branch.

## Develop Branch

**develop**:
The integration branch where completed features, bug fixes, and improvements are merged. This branch contains code that is ready for the next release cycle.

## Feature Branches

**Naming Convention:** 
feature/<short-description> (e.g., feature/user-authentication)

**Purpose:** 
These branches are created for developing new features. They branch off from develop and eventually merge back into develop after code review and testing.

**Usage:**
Start your new work with:
```git
git checkout -b feature/<short-description> develop
```

 Once the feature is complete, open a Pull Request (PR) to merge it back into develop.

## Release Branches

**Naming Convention:** 
release/<version> (e.g., release/1.2.0)

**Purpose:**
When the develop branch has enough features for a release, a release branch is created to prepare for a production release. Minimal bug fixes and release-specific changes are made on this branch.

**Usage:**
Create the branch:
```git 
git checkout -b release/<version> develop
```

After final testing and any necessary changes, this branch is merged into both master/main and back into develop.

## Hotfix Branches

Naming Convention: hotfix/<short-description> or include a version reference (e.g., hotfix/login-issue)
Purpose:
These branches are used for quickly patching production releases. They branch off from master/main and, once complete, are merged back into both master/main and develop.
Usage:
Create the branch:

```git
git checkout -b hotfix/<short-description> master
```

Once fixed, create a Pull Request (PR) to merge into both master/main and develop.

## Working on a Feature Branch with Multiple Developers

Communication:

Coordinate who works on which parts of a feature. Regularly update the team on progress to avoid overlapping work.

Keep Branch Up-to-Date:

Frequently pull changes from develop into your feature branch:

```git
git pull origin develop
```

or rebase your branch:

```git
git rebase develop
```

Internal Code Reviews:

If multiple developers are working on the same feature branch, consider using internal PRs or pair programming sessions as checkpoints before merging the finished feature back into develop.

## Using Pull Requests (PRs)

All merges from feature, release, or hotfix branches should be performed via Pull Requests to facilitate code reviews.
