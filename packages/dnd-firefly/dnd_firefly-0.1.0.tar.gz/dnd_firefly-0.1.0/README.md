# Drag-n-Drop files to Firefly programmatically

## Reqs

Make an environment, install deps:

```bash
pip install dist wheel selenium
```

## Build the Package:
Run the following command to build the package.

```bash
python setup.py sdist bdist_wheel
```
## Install the Package:

Install the package on macOS or Windows.
```bash
pip install dist/your_package-0.1-py3-none-any.whl
```

## Run

Example:

```bash
python firefly_demo/dnd_firefly.py ~/Downloads/WISE-allwise_p3as_psd-Cone_100asec.tbl
```