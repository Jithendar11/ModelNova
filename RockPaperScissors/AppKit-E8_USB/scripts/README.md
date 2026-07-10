# ML Out SDS Generator

`generate_ml_out_sds_from_header.py` reads model class information from a C header file and generates an ML OUT SDS YAML file.

## Requirements

- Python 3.9 or later
- PyYAML

Install the dependency with:

```bash
python3 -m pip install PyYAML
```

## Input file

The input is a C header file, typically named `model_config.h` in RockPaperScissors\AppKit-E8_USB\algorithm\ML Directory.

## Usage

Example using all defaults:

```bash
python3 generate_ml_out_sds_from_header.py model_config.h
```

Example with a custom frequency:

```bash
python3 generate_ml_out_sds_from_header.py model_config.h --frequency 10.0
```

Example with a custom output path:

```bash
python3 generate_ml_out_sds_from_header.py model_config.h --output generated/ML_Out.sds.yml
```

Example using short option names:

```bash
python3 generate_ml_out_sds_from_header.py model_config.h -f 10.0 -o generated/ML_Out.sds.yml
```

## Command-line arguments

| Argument | Required | Default | Description |
|---|---:|---:|---|
| `model_config` | Yes | None | Path to the input `model_config.h` file. |
| `-o`, `--output` | No | `./ML_Out.sds.yml` | Path of the generated YAML file. Parent directories are created automatically. |
| `-f`, `--frequency` | No | `8.33` | Frequency written to `sds.frequency`. The value must be greater than zero. |
| `-h`, `--help` | No | N/A | Displays command-line help. |

To display help:

```bash
python3 generate_ml_out_sds_from_header.py --help
```

## Output file

By default, the script generates:

```text
ML_Out.sds.yml
```

For the example input above, the generated file will look like:

```yaml
sds:
  name: ML output
  description: ML classification results
  frequency: 8.33
  content:
  - value: CAT
    type: float
  - value: DOG
    type: float
  - value: BIRD
    type: float
```
**Note:** All labels are automatically converted to uppercase in the generated `ML_Out.sds.yml` file.
