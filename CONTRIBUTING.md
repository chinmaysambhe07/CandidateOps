# Contributing to CandidateOps

Thank you for considering contributing to CandidateOps! We welcome contributions from the community.

## 📋 How to Contribute

### Reporting Issues

If you find a bug or have a feature request, please open an issue on GitHub. When reporting issues, please include:

- A clear and descriptive title
- Steps to reproduce the issue (if applicable)
- Expected behavior vs. actual behavior
- Screenshots or logs if relevant
- Your environment (Python version, OS, etc.)

### Pull Requests

We welcome pull requests! To ensure your contribution is accepted smoothly:

1. **Fork the repository** on GitHub
2. **Create a topic branch** from where you want to base your work
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes** following the coding standards below
4. **Add tests** for new functionality
5. **Ensure all tests pass** before submitting
6. **Commit your changes** with a clear, descriptive message
7. **Push to your branch** and open a pull request

### Coding Standards

#### Python Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) for code style
- Use [Black](https://github.com/psf/black) for code formatting
- Use [isort](https://pycqa/isort.readthedocs.io/) for import sorting
- Use [Flake8](https://flake8.pycqa.org/) for linting
- Use [mypy](https://mypy-lang.org/) for type checking

#### Documentation

- Use [Google-style docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
- Keep README and other documentation up to date
- Add comments for complex logic

#### Testing

- Write unit tests for new functionality
- Aim for high test coverage
- Test both positive and negative cases
- Mock external dependencies appropriately

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, missing semi-colons, etc.
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Adding or correcting tests
- `chore`: Changes to build process or auxiliary tools

Example:
```
feat(sap): implement real Selenium-based SAP client
```

### Development Workflow

1. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Run with coverage:
   ```bash
   pytest --cov=./ --cov-report=term-missing
   ```

4. Format code:
   ```bash
   black .
   isort .
   ```

5. Check types:
   ```bash
   mypy .
   ```

## 📄 License

By contributing to CandidateOps, you agree that your contributions will be licensed under the MIT License.

## 💡 Getting Help

If you need help with your contribution, please:
- Check the existing documentation
- Look at similar existing code in the repository
- Ask questions in the issue tracker
- Review the CONTRIBUTING guidelines again

Thank you for contributing to CandidateOps!