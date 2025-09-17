# Contributing to Waybar Hardware Info Module

First off, thank you for considering contributing to the Waybar Hardware Info Module! It's people like you that make this tool useful and robust for everyone.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [info@fredonbytes.cloud].

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

Before creating bug reports, please check the [existing issues](https://github.com/patrik-fredon/waybar-hardware-info/issues) as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title** for the issue to identify the problem.
- **Describe the exact steps which reproduce the problem** in as many details as possible.
- **Provide specific examples to demonstrate the steps**. Include links to files or GitHub projects, or copy/pasteable snippets, which you use in those examples.
- **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
- **Explain which behavior you expected to see instead and why.**
- **Include details about your configuration and environment:**
  - Python version
  - Waybar version
  - Wayland compositor and version
  - GPU type and drivers

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion, including completely new features and minor improvements to existing functionality.

- **Use a clear and descriptive title** for the issue to identify the suggestion.
- **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
- **Provide specific examples to demonstrate the steps**.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
- **Include screenshots and animated GIFs** which help you demonstrate the steps or point out the part of the project which the suggestion is related to.
- **Explain why this enhancement would be useful** to most users.

### Pull Requests

The process described here has several goals:

- Maintain the project's quality
- Fix problems that are important to users
- Engage the community in working toward the best possible solution
- Enable a sustainable system for the project's maintainers to review contributions

Please follow these steps to have your contribution considered by the maintainers:

1. Follow all instructions in [the template](.github/PULL_REQUEST_TEMPLATE.md)
2. Follow the [styleguides](#styleguides)
3. After you submit your pull request, verify that all [status checks](https://help.github.com/articles/about-status-checks/) are passing

While the prerequisites above must be satisfied prior to having your pull request reviewed, the reviewer(s) may ask you to complete additional design work, tests, or other changes before your pull request can be ultimately accepted.

## Styleguides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- When only changing documentation, include `[ci skip]` in the commit title

### Python Styleguide

All Python code must adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/).

- Use 4 spaces for indentation, not tabs
- Limit all lines to a maximum of 88 characters (following Black's default)
- Use descriptive variable and function names
- Write docstrings for all public modules, functions, classes, and methods
- Use type hints where possible

### Documentation Styleguide

- Use [Markdown](https://daringfireball.net/projects/markdown/) for documentation
- Reference methods and classes in markdown with the custom `{}` notation:
  - Reference classes with `{ClassName}`
  - Reference instance methods with `{ClassName.method_name}`
  - Reference class methods with `{ClassName.method_name}`

## Additional Notes

### Issue and Pull Request Labels

This section lists the labels we use to help us track and manage issues and pull requests.

#### Type of Issue and Issue State

- `bug` - Issues that are bugs
- `enhancement` - Issues that are feature requests
- `documentation` - Issues related to documentation
- `question` - Issues that are questions
- `help wanted` - Issues that need assistance
- `good first issue` - Good for newcomers

#### Pull Request Labels

- `work in progress` - Pull requests which are still being worked on
- `needs review` - Pull requests which need code review
- `under review` - Pull requests that are currently being reviewed
- `requires changes` - Pull requests which need to be updated by the author
- `needs testing` - Pull requests which need manual testing
