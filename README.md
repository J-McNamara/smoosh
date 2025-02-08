# smoosh: Software Module Outline & Organization Summary Helper

**Snapshot an entire repo or directory as plaintext on the clipboard and paste to your favorite AI tool!**

smoosh is a Python tool that helps developers understand and work with code repositories by generating LLM-optimized summaries of software modules, structure, dependencies, and patterns. It creates compressed yet meaningful representations that can be effectively used in LLM prompts for package understanding and troubleshooting.

## Features

- **Repo Snapshot**: Copy code repositories to clipboard as plaintext and paste to your favorite AI tools!
- **Smart Exclusion**: Exclude files in .gitignore, non-text, caches, large data files
- **Flexible Output Formats**: Export summaries in text, JSON, or YAML
- **Command Line Interface**: Easy-to-use CLI for quick analysis

## Installation

```bash
pip install smoosh
```

## Quick Start

Analyze a Python package and generate a summary:

```bash
smoosh /path/to/package
```

Export to specific format:

```bash
smoosh /path/to/package --format json --output summary.json
```

## Configuration (optional)

Create a `smoosh.yaml` in your project root:

```yaml
analysis:
  exclude_patterns: ['tests/*', '**/__pycache__/*']
  max_depth: 3
  focus: ['api', 'structure', 'patterns']

compression:
  level: medium  # low, medium, high
  custom_patterns:
    df_ops: "standard pandas operations"
    api_call: "external service request/response"

output:
  format: json
  include_schema: true
  max_tokens: 1000
```

## Example Output

```
╭───────────────────────────────────────────────────────────────╮
│ 🐍 smoosh v0.1.2 - Making Python packages digestible!         │
╰───────────────────────────────────────────────────────────────╯
⠋ Analyzing repository...INFO: Processing directory at code/smoosh
⠋ Analyzing repository...
⠋ Generating summary...
✨ Output copied to clipboard!
        Analysis Results
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Metric              ┃ Value  ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ Repository Size     │ 0.06MB │
│ Total Files         │ 36     │
│ Python Files        │ 17     │
│ Original Lines      │ 2436   │
│ Composed Lines      │ 2520   │
│ Original Characters │ 62187  │
│ Composed Characters │ 63366  │
│ Lines Ratio         │ 1.03x  │
│ Characters Ratio    │ 1.02x  │
└─────────────────────┴────────┘
⠹ Analyzing repository...
⠹ Generating summary...
```
**Clipboard output**
```
Repository: smoosh
Mode: cat
Files: 36 (17 Python)
Total Size: 0.06MB

Repository Structure:
smoosh/
    ├── .github/
    │   └── workflows/
    │       ├── ci.yml
    │       ├── publish.yml
    │       └── release-candidate.yml
    ├── src/
    │   └── smoosh/
    │       ├── analyzer/
    │       │   ├── __init__.py
    │       │   ├── repository.py
    │       │   └── tree.py
    │       ├── composer/
    │       │   ├── __init__.py
    │       │   ├── concatenator.py
    │       │   └── formatter.py
    │       ├── utils/
    │       │   ├── __init__.py
    │       │   ├── config.py
    │       │   ├── file_utils.py
    │       │   ├── logger.py
    │       │   └── path_resolver.py
    │       ├── __init__.py
    │       ├── custom_types.py
    │       └── version.py
    ├── tests/
    │   ├── utils/
    │   │   └── generate_sample.py
    │   ├── __init__.py
    │   └── test_cli.py
    ├── .flake8
    ├── .gitignore
    ├── .pre-commit-config.yaml
    ├── DEVELOPMENT.md
    ├── LICENSE
    ├── pyproject.toml
    └── README.md



### File: .flake8 ###
[flake8]
max-line-length = 100
exclude =
    .git,
    __pycache__,
    build,
    dist
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/smoosh.git
cd smoosh
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Run tests:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap

Future developments may include:
- Smart Compression: Generate compact package representations while preserving essential information
- LLM-Optimized Output: Create summaries specifically formatted for effective use with Language Models
- Error pattern detection
- IDE integration
- Documentation generation
- Intelligent type abbreviation
- Pattern reference system
- Call chain compression
- Reference deduplication

## Support

For questions and support, please open an issue in the GitHub repository.
