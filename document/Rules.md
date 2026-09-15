# Team Development Guidelines

## 1. Development Workflow

Development should always be performed on a separate working branch rather than directly on main.

For a new feature, creating an Issue is not required. A developer may create a new branch, implement the feature, commit and push the changes, and then open a Pull Request. The Pull Request must be reviewed by another team member before it is merged into main. After the merge is complete, the working branch should be deleted.

For bug fixes, improvements, or changes to existing features, an Issue should generally be created before development begins. The Issue should clearly describe the problem, requested improvement, or required change. Development should then proceed on a separate branch, and the resulting changes should be submitted through a Pull Request. Once the Pull Request has been reviewed and merged, the related Issue should be closed and the working branch should be deleted.

An Issue should also be created when a change affects multiple team members or requires discussion before implementation.

Direct pushes to the main branch are not allowed. All changes to main must go through a Pull Request and Code Review.

## 2. Branch Rules

All development work must be performed on a separate branch. Direct development on the `main` branch is not allowed.

Branch names should clearly describe the purpose of the work and follow a consistent naming convention.

Recommended formats include:

```text
feature/<feature-name>
fix/<fix-name>
docs/<document-name>
refactor/<target-name>
```

Examples:

```text
feature/login-page
feature/user-profile
fix/login-button
fix/navbar-layout
docs/update-readme
refactor/authentication
```

A branch should be created for one main purpose. Unrelated changes should not be included in the same branch.

Team members should avoid working on the same branch at the same time unless collaboration on that branch is necessary and has been agreed on in advance.

Before creating a new branch, the local `main` branch should be updated so that development starts from the latest version of the project.

After the related Pull Request has been merged, the branch should be deleted if it is no longer needed.

## 3. Issue Rules

Issues are used to track bugs, improvements, changes to existing features, and work that requires discussion before implementation.

An Issue should generally be created in the following situations:

- A bug has been found
- An existing feature needs to be improved
- A specification or behavior needs to be changed
- A large refactoring is required
- The change may affect multiple team members
- The implementation requires discussion before development begins

Creating an Issue is not required when implementing a completely new feature from scratch, unless the feature requires prior discussion or coordination.

Each Issue should clearly describe the problem or requested change. When necessary, it should also include the expected behavior, relevant context, screenshots, error messages, or other information that may help with implementation.

Each Issue should focus on one main problem or objective. If an Issue contains multiple unrelated tasks, it should be divided into separate Issues.

When a team member starts working on an Issue, the Issue should be assigned to that person so that the team can clearly see who is responsible for the work.

The related Issue should be referenced in the Pull Request and closed after the corresponding changes have been successfully merged.

## 4. Commit Rules

Commits should be small, focused, and easy to understand. Each commit should represent one meaningful change.

Unrelated changes should not be combined into the same commit. This makes the history easier to review and helps identify the cause of problems when debugging.

Commit messages should briefly explain what was changed. Use clear and specific wording rather than vague messages.

Recommended prefixes include:

```text
feat:     new feature
fix:      bug fix
docs:     documentation update
style:    formatting or UI style change
refactor: code restructuring without changing behavior
test:     test-related changes
chore:    configuration or maintenance work
```

Examples:

```text
feat: add login form
fix: correct login button behavior
docs: update setup instructions
refactor: simplify authentication logic
```

Avoid unclear commit messages such as:

```text
update
change
fix
test
final
aaa
```

Before committing, review the changed files and make sure that only the intended changes are included.

## 5. Pull Request Rules

All changes to the `main` branch must be submitted through a Pull Request.

The Pull Request description must follow the existing Pull Request Template provided in the repository.

The Pull Request title should clearly and concisely describe the main change. It should contain the minimum information necessary to understand what the Pull Request does.

Good examples:

```text
Add login page
Fix login button
Improve navbar layout
Update README
```

Avoid vague titles such as:

```text
Update
Fix
Changes
PR
Test
```

Each Pull Request should focus on one main purpose. Unrelated changes should not be included in the same Pull Request.

If a Pull Request is related to an Issue, the Issue should be referenced in the Pull Request.

Before requesting review, the author should make sure that the implementation is complete, the code works as expected, and no unnecessary files or changes are included.

## 6. Code Review and Merge Rules

Every Pull Request must be reviewed by at least one team member other than the author before it is merged into `main`.

The reviewer should check whether the implementation matches its intended purpose, follows the project’s coding conventions, and does not introduce unnecessary or unrelated changes. Reviewers should also look for potential bugs, security concerns, maintainability issues, and possible effects on existing functionality.

If changes are requested during review, the author should address them before the Pull Request is merged. When necessary, the author and reviewer should discuss the implementation directly in the Pull Request.

A Pull Request may be merged only when:

- The required review has been completed
- Requested changes have been addressed
- There are no unresolved merge conflicts
- Required tests pass
- No unintended files or changes are included

The author should not merge their own Pull Request without review.

Use `Squash and merge` as the default merge method unless there is a specific reason to use another method. After the merge is complete, the working branch should be deleted if it is no longer needed.
