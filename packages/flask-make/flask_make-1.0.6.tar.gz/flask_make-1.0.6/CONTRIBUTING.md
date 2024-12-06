# Contributing to create-flask-app

We welcome contributions to **create-flask-app**! Whether you’re fixing bugs, proposing new features, or improving documentation, your input is valuable. Follow the guide below to get started.

## Getting Started

1. **Fork the Repository**
   - Fork this repository to create your own copy.
   - Clone the forked repository to your local machine:
     ```bash
     git clone https://github.com/your-username/create-flask-app.git
     cd create-flask-app
     ```

2. **Set Up a Virtual Environment**
   - It's recommended to work in a virtual environment for isolated dependencies.
   ```bash
   python3 -m venv env
   source env/bin/activate  # On macOS/Linux
   env\Scripts\activate     # On Windows
   ```

## Code Structure

The project follows a structured directory layout:

- **`flask_make`**: Contains the main script (`__init__.py`) responsible for the app creation logic.

## Making Changes

1. **Create a Feature Branch**
   - Make sure you’re on the `main` branch, and create a new branch for your feature or fix:
     ```bash
     git checkout main
     git pull origin main
     git checkout -b feature/your-feature-name
     ```

2. **Make Your Edits**
   - Add or modify code, documentation, or tests as needed.

3. **Lint and Format**
   - Run linters and formatters to keep the codebase consistent:
     ```bash
     flake8 .  # Linting
     black .   # Formatting
     ```

4. **Commit Your Changes**
   - Commit your changes with a meaningful message:
     ```bash
     git add .
     git commit -m "Add a concise message describing your changes"
     ```

5. **Push to Your Fork and Submit a PR**
   - Push your branch to your fork and open a pull request to the `main` branch of this repository:
     ```bash
     git push origin feature/your-feature-name
     ```
   - Open a pull request (PR) and fill out the template, explaining the changes and why they’re needed.

## Guidelines

- **Write Clear Commit Messages**: Follow conventional commits, e.g., `fix:`, `feat:`, or `docs:`.
- **Document Your Code**: Write comments for complex or crucial parts of the code.
- **Test Your Changes**: Ensure existing and new tests pass before submitting.
- **Follow Code Style**: Run `black` and `flake8` to ensure consistent formatting.

## Setting Up for Local Testing

To test the CLI tool locally without publishing, you can use `pip install -e .` in the project’s root directory. This will install the package in “editable” mode, allowing you to test changes directly:

```bash
pip install -e .
```

Or you can simply run the python command in the terminal

```bash
cd flask_make
python __init__.py app-name
```

## Licensing

By contributing to **flask-make**, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make **flask-make** better for everyone!