# ELF Reader

A simple tool to list the executable sections from ELF files.
The tool was tested with the [hello_world](https://github.com/espressif/esp-idf/tree/67552c31da/examples/get-started/hello_world) example project from Espressif.

## Installation

Before running any installation, make sure you prepare a local Python environment:

```bash
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements/dev.txt
```

### Self-contained tool

```bash
pyinstaller -F --console --name elfreader src/elfreader/__main__.py
```

The resulting binary can be found in the `dist` folder.

### Python package

The Python package can be built using the following commands:

```bash
python3 -m build
```

This should build the package and place the archives in the `dist` folder.
To install these packages locally, use the following command:

```bash
pip3 install dist/ELFReader-1.0.0.tar.gz
```

## Usage

The resulting CLI application is very simple.
Printing the help can be done with the `-h/--help` argument.

### Self-contained tool

```ps
./elfreader <your_file> -v
```

### Python package

```bash
python3 -m elfreader <your_file> -v
```

## Development

Pre-commit hooks are used for static code checks.
These can be installed in the following way:

```bash
pip3 install pre-commit
pre-commit install
```

They can be run in the following way:

```bash
pre-commit run --all
```
