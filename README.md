# smoosh: Software Module Outline & Organization Summary Helper

smoosh is a Python tool that helps developers understand and work with Python packages by generating LLM-optimized summaries of package structure, dependencies, and patterns. It creates compressed yet meaningful representations that can be effectively used in LLM prompts for package understanding and troubleshooting.

## Features

- **Intelligent Package Analysis**: Parse and analyze Python packages using AST to understand structure, relationships, and patterns
- **Smart Compression**: Generate compact package representations while preserving essential information
- **LLM-Optimized Output**: Create summaries specifically formatted for effective use with Language Models
- **Flexible Output Formats**: Export summaries in JSON, YAML, Markdown, or custom LLM formats
- **Command Line Interface**: Easy-to-use CLI for quick package analysis

## Installation

```bash
pip install smoosh
```

## Quick Start

Analyze a Python package and generate a summary:

```bash
smoosh /path/to/package
```

Generate a focused API summary:

```bash
smoosh /path/to/package --focus api
```

Export to specific format:

```bash
smoosh /path/to/package --format json --output summary.json
```

## Configuration

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

## Key Components

### Code Analyzer
- AST-based Python file parsing
- Function and class relationship mapping
- Dependency analysis
- Pattern detection

### Compression Engine
- Intelligent type abbreviation
- Pattern reference system
- Call chain compression
- Reference deduplication

### Summary Generator
- Multiple output format support
- Customizable summary types
- LLM-optimized formatting

## CLI Options

```bash
Options:
  --focus TEXT          Analysis focus (api, structure, patterns)
  --format TEXT         Output format (json, yaml, markdown, llm)
  --output FILE        Output file path
  --compression-level  Compression level (low, medium, high)
  --to-clipboard       Copy output to clipboard
  --help              Show this message and exit
```

## Example Output

```yaml
package:
  name: "example_pkg"
  structure:
    modules: ["core", "utils", "api"]
    patterns:
      p1: "DataFrame processor"
      p2: "Data validation"

  api:
    core:
      - "process_data(df: DataFrame) -> DataFrame"
      - "validate_input(D[s, Any]) -> bool"
    utils:
      - "load_config(path: s) -> Config"
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

## Acknowledgments

- Built with Python's ast module for code analysis
- Inspired by the need for better LLM-based code understanding tools

## Roadmap

Future developments may include:
- Snakemake pipeline analysis
- Error pattern detection
- IDE integration
- Documentation generation
- Learning path creation

## Support

For questions and support, please open an issue in the GitHub repository.
