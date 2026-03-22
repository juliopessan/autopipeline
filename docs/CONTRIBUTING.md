# Contributing to Azure Autonomous Data Platform

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Respect different viewpoints and experiences

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Git
- Docker (optional)

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/fcamara/autopipeline.git
cd autopipeline

# Backend setup
python -m venv venv
source venv/bin/activate
pip install -r backend/backend_requirements.txt

# Frontend setup
cd frontend
npm install
```

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/my-feature
# or
git checkout -b fix/my-fix
```

### 2. Make Changes

- Follow the code style (Python: PEP 8, JavaScript/TypeScript: Prettier)
- Add tests for new features
- Update documentation as needed

### 3. Test Changes

```bash
# Backend tests
pytest backend/

# Frontend build
cd frontend && npm run build

# Local test
docker-compose up
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: Add new feature" 
# or
git commit -m "fix: Fix bug in dashboard"
```

Use conventional commits:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `style:` for code style changes
- `refactor:` for refactoring
- `test:` for tests
- `chore:` for maintenance

### 5. Push and Create Pull Request

```bash
git push origin feature/my-feature
```

Visit GitHub and create a Pull Request.

## Pull Request Guidelines

- Provide clear description of changes
- Reference related issues
- Include tests for new features
- Update documentation
- Ensure CI/CD checks pass
- Request review from maintainers

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Max line length: 100
- Format with Black

```bash
pip install black
black backend/
```

### TypeScript/JavaScript
- Use Prettier
- Use ESLint
- Max line length: 100

```bash
cd frontend
npm run lint
npm run format
```

## Testing

### Backend Tests

```bash
pip install pytest pytest-cov
pytest backend/ -v --cov=backend/
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Documentation

- Update README.md for user-facing changes
- Update SETUP-DEPLOYMENT-GUIDE.md for deployment changes
- Add code comments for complex logic
- Update API documentation in docstrings

## Reporting Issues

### Bug Reports
Include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment info (OS, Python/Node version)
- Screenshots if applicable

### Feature Requests
Include:
- Clear description of feature
- Why it's needed
- Possible implementation approach
- Examples

## Commit Conventions

```
<type>(<scope>): <subject>

<body>

<footer>
```

Example:
```
feat(dashboard): Add metric trend chart

Add a new chart to visualize metric improvements over time
using Recharts. Includes time-range selector and zoom controls.

Closes #123
```

## Release Process

1. Update version in `setup.py` or `package.json`
2. Update CHANGELOG.md
3. Create release branch
4. Run full test suite
5. Create GitHub release
6. Deploy to production

## Questions?

- Open an issue for questions
- Check existing documentation
- Ask in GitHub Discussions
- Contact maintainers

---

Thank you for contributing! 🎉
