# CR Checker

`cr_checker.py` is a tool designed to check if files contain a specified copyright header. It provides configurable logging, color-coded console output, and can handle large file sets efficiently. The script supports reading configuration files for custom copyright templates and can utilize memory-mapped file reading for better performance with large files.

## Features

- Checks files for specified copyright headers based on file extensions.
- Configurable logging, including color-coded output for easy visibility of log levels.
- Supports parameter files for flexible input handling.
- Can use memory mapping for large file handling.
- Customizable file encoding and offset adjustments for header text positioning.

## Requirements

- Python 3.6+
- `argparse`, `logging`, `os`, `sys`, `mmap`, and `configparser` (standard library modules)

## Installation

To use `cr_checker.py`, simply clone this repository or copy the script into your project.

```bash
git clone <your_repo_url>
```

## Usage

The script can be run from the command line with various options to customize its behavior:

```bash
python cr_checker.py -t <template_file> [options] <inputs>
```

### Arguments

- -t, --template-file: (Required) Path to the template file that defines the copyright text for each file extension.
- -v, --verbose: Enable debug-level logging.
- -l, --log-file: Path to a log file where logs will be saved. If not provided, logs will print to the console.
- -e, --extensions: List of file extensions to filter, e.g., -e .py .cpp.
- --use_memory_map: Use memory-mapped file reading for large files.
- --encoding: File encoding (default is utf-8).
- --offset: Additional offset for the header length to account for lines like a shebang.
- inputs: Directories or files to parse, or a parameter file prefixed with @ that lists files or directories.

### Examples

```sh
python cr_checker.py -t templates.ini -v -l logs.txt -e .py .cpp @files_to_check.txt

python cr_checker.py -t templates.ini -e .py .cpp --offset 24 --use_memory_map @files_to_check.txt
```

### Template File Format

The template file should be in INI format, with each section representing a file extension and a template key specifying the copyright text.

Example templates.ini:

```ini
[py,sh]
template = # Copyright (c) 2024 Nikola Radakovic

[cpp,c,h]
template = // Copyright (c) 2024 Nikola Radakovic
```

## Exit Codes

- 0: All files contain the required copyright text.
- 1: Some files are missing the required copyright text.
- Other: Error encountered during file processing.

### Logging and Color-Coded Output

By default, logs are printed to the console in color-coded format to indicate log levels. You can redirect logs to a file using the -l option.

#### Log Colors

- DEBUG: Blue
- INFO: Green
- WARNING: Yellow
- ERROR: Red

## License

MIT License
