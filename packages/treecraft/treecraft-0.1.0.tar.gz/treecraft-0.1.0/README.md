# 🌳 Treecraft

Treecraft is a Python tool that generates directory structures from text-based tree representations. It provides an intuitive way to create project scaffolding from a visual directory tree structure.

## ✨ Features

- 📁 Generate directory structures from text-based tree representations
- 🐍 Automatic Python file initialization with docstrings
- 🔍 Dry run mode to preview changes
- ⚡ Simple and intuitive CLI interface
- 🛡️ Safe path handling and validation

## 🚀 Installation

You can install Treecraft using pip:

```bash
pip install treecraft
```

For development installation:

```bash
git clone https://github.com/ashwin271/treecraft.git
cd treecraft
pip install -e .
```

## 📖 Usage

### Command Line Interface

Create a text file with your desired directory structure:

```
src/
├── agents/
│   ├── __init__.py
│   └── agent.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
└── main.py
```

Then run Treecraft:

```bash
treecraft input.txt -o output_directory
```

### Python API

```python
from treecraft import TreeParser, Generator

# Initialize components
parser = TreeParser()
generator = Generator()

# Parse tree structure
with open('input.txt', 'r') as f:
    tree_content = f.read()
    
structure = parser.parse(tree_content)

# Generate directory structure
generator.generate(structure, 'output_directory')
```

## 🔧 Development

### Setup Development Environment

1. Clone the repository:
```bash
git clone https://github.com/ashwin271/treecraft.git
cd treecraft
```

2. Install development dependencies:
```bash
pip install -r requirements.txt
```

### Running Tests

```bash
pytest tests/
```

## 📝 Examples

### Basic Structure

```
project/
├── README.md
├── requirements.txt
└── src/
    └── main.py
```

### Complex Structure

```
project/
├── docs/
│   └── index.md
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   └── main.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   └── test_core.py
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

Ashwin Murali - [@Ashwin_271](https://twitter.com/Ashwin_271)

Project Link: [https://github.com/ashwin271/treecraft](https://github.com/ashwin271/treecraft)
