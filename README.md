# CADCAST Estimation Plugin for Cura — Technical Documentation

Sphinx-based technical documentation for the CADCAST Cura Cost Estimator plugin, built with [MyST-Parser](https://myst-parser.readthedocs.io/) for Markdown support and served as static HTML.

---

## Requirements

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/)
- [`anaconda-project`](https://anaconda-project.readthedocs.io/) installed in your base conda environment
- Python 3.14 (managed automatically by `anaconda-project`)

### Installing `anaconda-project`

If you haven't already, install it into your base conda environment:

```bash
conda install -c conda-forge anaconda-project
```

---

## Setup

Clone the repository and navigate to the project root (the directory containing `anaconda-project.yaml`), then run:

```bash
anaconda-project prepare
```

This will automatically create and configure a conda environment with all required dependencies:

- Python 3.14
- Sphinx 9.1.0
- MyST-Parser
- setuptools

You do not need to run `conda create` or `pip install` manually — `anaconda-project` manages the environment for you.

---

## Usage

### Build the Documentation

Compiles the Sphinx source files in `./source` into static HTML output in `./build`:

```bash
anaconda-project run build
```

> This clears any previous build output before rebuilding.

### Serve the Documentation Locally

Starts a local HTTP server to preview the built documentation in your browser:

```bash
anaconda-project run runserver
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

> You must run `build` before `runserver` — the server serves the `./build` directory, which won't exist until after a successful build.

---

## Project Structure

```
.
├── anaconda-project.yaml   # Environment and command definitions
├── source/                 # Sphinx source files (.md / .rst)
│   ├── conf.py             # Sphinx configuration
│   ├── index.rst           # Documentation root / table of contents
│   └── ...
└── build/                  # Generated HTML output (not committed to version control)
```

---

## Development Notes

- Documentation source files are written in Markdown (`.md`) via MyST-Parser. Refer to the [MyST-Parser docs](https://myst-parser.readthedocs.io/) for syntax guidance.
- Sphinx configuration lives in `source/conf.py`. Extensions, theme, and other settings are managed there.
- The `build/` directory is generated output and should be listed in `.gitignore`.
- If your conda environment becomes broken or out of sync, remove it and re-prepare:

```bash
conda env remove -n cadcast-estimation-plugin-for-cura
anaconda-project prepare
```

> The environment name is derived from the `name` field in `anaconda-project.yaml`.
