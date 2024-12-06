# LLM Multiple Choice

[![Python Versions](https://img.shields.io/pypi/pyversions/llm-multiple-choice.svg)](https://pypi.org/project/llm-multiple-choice/)
[![PyPI version](https://badge.fury.io/py/llm-multiple-choice.svg)](https://badge.fury.io/py/llm-multiple-choice)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python library for having an LLM fill out a multiple-choice questionnaire about the current state of a chat.

## Features

- Composible with any LLM provider -- this library generates LLM prompts and validates responses,
  but leaves the actual LLM calls to you.
- Flexible questionnaire structure.
- Simple API for using the questionnaire results in code.

## Installation

Requires Python 3.12 or later.

You can install the library using pip:

```bash
pip install llm-multiple-choice
```

If you're using Poetry:

```bash
poetry add llm-multiple-choice
```

## Usage

This library helps you create multiple-choice questionnaires for LLMs to fill out.

### Creating a Questionnaire

```python
from llm_multiple_choice import ChoiceManager, DisplayFormat

# Create a questionnaire
manager = ChoiceManager()

# Add a section with choices
section = manager.add_section("Assess the sentiment of the message.")
positive_sentiment = section.add_choice("The message expresses positive sentiment.")
neutral_sentiment = section.add_choice("The message is neutral in sentiment.")
negative_sentiment = section.add_choice("The message expresses negative sentiment.")

# Get the prompt to send to your LLM
prompt = manager.prompt_for_choices(DisplayFormat.MARKDOWN)
```

### Processing LLM Responses

The library enforces these rules for LLM responses:
- Must contain only numbers corresponding to valid choices
- Numbers must be separated by commas
- Each number can only appear once
- Cannot be empty

Process the response:
```python
try:
    choices = manager.validate_choices_response(llm_response)
    # Check which choices were selected
    if choices.has(positive_sentiment):
        print("Choice 1 was selected")
except InvalidChoicesResponseError as e:
    print(f"Invalid response: {e}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Setting Up for Development

1. **Ensure you have Python 3.12 or later**:
   ```bash
   # On macOS with Homebrew
   brew install python@3.13  # or python@3.12
   ```

2. **Install Poetry**:
   ```bash
   # On macOS with Homebrew
   brew install poetry

   # Verify installation
   poetry --version
   ```

3. **Clone the repository**:
   ```bash
   git clone https://github.com/deansher/llm-multiple-choice.git
   cd llm-multiple-choice
   ```

4. **Create a virtual environment and install dependencies**:
   ```bash
   # Ensure poetry uses the correct Python version
   poetry env use python3.13  # or python3.12

   # Create venv and install all dependencies
   poetry install
   ```

5. **Verify your setup**:
   ```bash
   # Check Python version
   poetry run python --version  # Should show 3.13.x

   # Run tests to ensure everything works
   poetry run pytest
   ```

You can either activate the virtual environment in your shell by running `poetry shell`, or run commands directly using `poetry run <command>`.

### Setting Up Pre-commit Hooks

After installing dependencies, set up pre-commit hooks:
```bash
poetry shell
pre-commit install
```

This ensures code quality checks run automatically before each commit.

### Setting Up VS Code

To ensure VS Code works correctly with this project:

1. Open the Command Palette (Cmd+Shift+P on Mac, Ctrl+Shift+P on Windows/Linux)
2. Select "Python: Select Interpreter"
3. Get your Poetry environment's Python path:
   ```bash
   poetry run which python
   ```
4. Click "Enter interpreter path..." (option with folder icon)
5. In the text field that appears labeled "Enter path to a Python interpreter", paste your Poetry environment's Python path
6. Press Enter to confirm

If VS Code doesn't recognize your virtual environment after setting it up, try closing and reopening VS Code.

### Running Tests

Run the test suite using pytest:
```bash
poetry run pytest
```

### Adding Dependencies

To add a new dependency to the project:

- For regular dependencies:
   ```bash
   poetry add <package_name>
   ```

- For development dependencies (e.g., testing tools):
   ```bash
   poetry add --group dev <package_name>
   ```

This updates the `pyproject.toml` and `poetry.lock` files accordingly.

### Troubleshooting

If you encounter issues:

1. **Wrong Python version**:
   ```bash
   # Verify Python version
   python --version

   # If needed, explicitly use Python 3.13
   poetry env use python3.13
   ```

2. **Poetry environment issues**:
   ```bash
   # Remove existing environment
   poetry env remove python

   # Create fresh environment
   poetry env use python3.13
   poetry install
   ```

## Release Process

This project uses GitHub Actions for automated testing and publishing to PyPI.

### Making a Release

1. Update version in `pyproject.toml`
2. Create and push a new tag:
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```
3. Create a new Release on GitHub:
   - Go to the repository's Releases page
   - Click "Create a new release"
   - Choose "Choose a tag" and select the tag you just created
   - Add release notes describing the changes
   - Click "Publish release"
4. GitHub Actions will automatically:
   - Run all tests and type checking
   - Build the package
   - Publish to PyPI if all checks pass

### Manual Publishing

If needed, you can publish manually using the build script:

```bash
# Publish to TestPyPI
./scripts/build_and_publish.sh

# Publish to production PyPI
./scripts/build_and_publish.sh --production
```

### Local Development Integration

When developing applications that use this library, you may want to test changes to the library without publishing them to PyPI. You can achieve this using either Poetry or pip's editable install feature.

#### Using Poetry

Poetry's path dependency feature makes local development straightforward:

1. Clone this repository alongside your project:
   ```bash
   git clone https://github.com/deansher/llm-multiple-choice-py.git
   ```

2. In your project's `pyproject.toml`, replace the PyPI dependency with a path dependency:
   ```toml
   [tool.poetry.dependencies]
   llm-multiple-choice = { path = "../llm-multiple-choice-py", develop = true }
   ```

   Or use the Poetry CLI:
   ```bash
   poetry remove llm-multiple-choice
   poetry add --editable ../llm-multiple-choice-py
   ```

The `develop = true` flag creates a symlink to the library's source, allowing you to modify the library code and immediately see the effects in your project without reinstalling.

#### Using pip

If you're using pip, you can use its editable install feature:

1. Clone this repository alongside your project:
   ```bash
   git clone https://github.com/deansher/llm-multiple-choice-py.git
   ```

2. Install the package in editable mode:
   ```bash
   pip install -e ../llm-multiple-choice-py
   ```

The `-e` flag tells pip to install the package in "editable" mode, creating a link to the source code instead of copying it. This allows you to modify the library code and see changes immediately without reinstalling.


## License

This project is licensed under the MIT License - see the LICENSE file for details.
