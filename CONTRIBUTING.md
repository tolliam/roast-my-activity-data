# Contributing to Roast My Activity Data

First off, thank you for considering contributing to Roast My Activity Data! It's people like you that make this tool better for everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

## 🤝 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in all interactions.

### Our Standards

- ✅ Use welcoming and inclusive language
- ✅ Be respectful of differing viewpoints
- ✅ Accept constructive criticism gracefully
- ✅ Focus on what's best for the community
- ❌ No harassment, trolling, or insulting comments
- ❌ No personal or political attacks

## 🎯 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear descriptive title**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Environment details** (OS, Python version, etc.)
- **Sample data** if relevant (anonymized)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- **Clear description** of the feature
- **Use case** explaining why it's useful
- **Mockups or examples** if applicable
- **Implementation ideas** if you have them

### Your First Code Contribution

Unsure where to start? Look for issues labeled:
- `good first issue` - Simple issues for newcomers
- `help wanted` - Issues where we need community help
- `documentation` - Improvements to docs

## 🛠️ Development Setup

### 1. Fork and Clone

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/roast-my-activity-data.git
cd roast-my-activity-data
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

## 📝 Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with these specifics:

- **Line length**: Maximum 100 characters
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Double quotes for strings
- **Imports**: Grouped (standard lib, third-party, local)

### Documentation

All functions must have Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """Short description of function.
    
    Longer description if needed, explaining behavior, edge cases, etc.
    
    Args:
        param1: Description of param1.
        param2: Description of param2.
        
    Returns:
        Description of return value.
        
    Raises:
        ValueError: When param2 is negative.
        
    Examples:
        >>> example_function("test", 5)
        True
    """
    pass
```

### Type Hints

Use type hints for all function signatures:

```python
from typing import List, Dict, Optional

def process_data(df: pd.DataFrame, config: Dict[str, str]) -> Optional[List[str]]:
    pass
```

### Code Organization

- **config.py**: Constants and configuration only
- **data_loader.py**: Data loading and preprocessing
- **utils.py**: Helper functions and calculations
- **visualizations.py**: Chart creation functions
- **app.py**: Streamlit UI and orchestration

### Testing

When adding new features, include tests:

```python
# tests/test_new_feature.py
import pytest
from src.your_module import your_function

def test_your_function():
    """Test that your_function works correctly."""
    result = your_function(input_data)
    assert result == expected_output
```

## 📋 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```bash
feat(visualizations): add heat map for weekly activity patterns

Added create_weekly_heatmap function to show activity distribution
across days of the week. Uses plotly heatmap with custom color scale.

Closes #123
```

```bash
fix(data_loader): handle missing elevation data gracefully

Fixed crash when activities have null elevation values.
Now defaults to 0 and logs warning.

Fixes #456
```

## 🔄 Pull Request Process

### Before Submitting

1. ✅ Update documentation for any changed functionality
2. ✅ Add tests for new features
3. ✅ Ensure all tests pass
4. ✅ Update README.md if needed
5. ✅ Follow the coding standards
6. ✅ Rebase on latest main branch

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing done

## Screenshots
If applicable

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed my code
- [ ] Commented complex areas
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Added tests
- [ ] All tests pass
```

### Review Process

1. Automated checks must pass
2. At least one maintainer approval required
3. Address all review comments
4. Maintainer will merge when approved

## 🏗️ Project Structure Guidelines

### Adding New Modules

When adding new functionality:

1. **Consider existing modules first** - Can it fit in utils or visualizations?
2. **Create focused modules** - Single responsibility principle
3. **Update __init__.py** - Export public functions
4. **Add to documentation** - Update ARCHITECTURE.md

### Adding New Dependencies

1. **Justify necessity** - Explain why it's needed
2. **Check compatibility** - Ensure Python 3.8+ support
3. **Update requirements.txt** - Add with version constraints
4. **Update setup.py** - Include in install_requires

## 🎨 UI/UX Guidelines

### Streamlit Best Practices

- Use `st.cache_data` for expensive computations
- Provide loading indicators for long operations
- Use columns for responsive layouts
- Add helpful tooltips and help text
- Maintain consistent spacing and alignment

### Accessibility

- Use accessible color palettes (already using UK Gov standards)
- Provide text alternatives for visual info
- Ensure keyboard navigation works
- Use semantic HTML where possible

## 📚 Documentation

### What to Document

- **Functions**: Purpose, parameters, returns, examples
- **Classes**: Purpose, attributes, methods
- **Modules**: Overview and usage examples
- **Configuration**: Available options and defaults

### Where to Document

- **Code docstrings**: API documentation
- **README.md**: Project overview and quick start
- **docs/USAGE.md**: Detailed user guide
- **docs/ARCHITECTURE.md**: System design and structure
- **CONTRIBUTING.md**: This file!

## ❓ Questions?

Don't hesitate to ask! Open an issue with the `question` label or reach out to the maintainers.

## 🙏 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!

---

**Happy Coding! 🚀**
