#!/usr/bin/env python3
"""Generate ML_Out.sds.yml from MODEL_LABELS in model_config.h."""

import argparse
import ast
import re
import sys
from pathlib import Path

import yaml


NUM_CLASSES_PATTERN = re.compile(
    r"^\s*#\s*define\s+MODEL_NUM_CLASSES\s+\(?\s*(\d+)\s*\)?",
    re.MULTILINE,
)
LABEL_ARRAY_PATTERN = re.compile(
    r"static\s+const\s+char\s*\*\s*const\s+MODEL_LABELS\s*"
    r"\[\s*MODEL_NUM_CLASSES\s*\]\s*=\s*\{(?P<body>.*?)\}\s*;",
    re.DOTALL,
)
C_STRING_PATTERN = re.compile(r'"(?:\\.|[^"\\])*"')


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Read MODEL_NUM_CLASSES and MODEL_LABELS from model_config.h, "
            "then generate ML_Out.sds.yml."
        )
    )
    parser.add_argument(
        "model_config",
        type=Path,
        help="Path to model_config.h",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("ML_Out.sds.yml"),
        help="Output YAML path (default: ./ML_Out.sds.yml)",
    )
    parser.add_argument(
        "-f",
        "--frequency",
        type=float,
        default=8.33,
        help="SDS output frequency (default: 8.33)",
    )
    return parser.parse_args()


def remove_c_comments(text: str) -> str:
    """Remove C/C++ comments while preserving string literals."""
    return re.sub(
        r'("(?:\\.|[^"\\])*")|(/\*.*?\*/|//[^\r\n]*)',
        lambda match: match.group(1) or "",
        text,
        flags=re.DOTALL,
    )


def decode_c_string(token: str) -> str:
    """Decode a standard C string literal using Python-compatible escapes."""
    try:
        value = ast.literal_eval(token)
    except (SyntaxError, ValueError) as exc:
        raise ValueError(f"Unable to parse label string: {token}") from exc

    if not isinstance(value, str):
        raise ValueError(f"Label is not a string: {token}")
    return value


def load_model_labels(header_path: Path) -> tuple[int, list[str]]:
    if not header_path.is_file():
        raise FileNotFoundError(f"Header file not found: {header_path}")

    source = header_path.read_text(encoding="utf-8")
    source_without_comments = remove_c_comments(source)

    num_classes_match = NUM_CLASSES_PATTERN.search(source_without_comments)
    if not num_classes_match:
        raise ValueError("Could not find numeric MODEL_NUM_CLASSES definition")
    num_classes = int(num_classes_match.group(1))

    labels_match = LABEL_ARRAY_PATTERN.search(source_without_comments)
    if not labels_match:
        raise ValueError(
            "Could not find 'static const char * const "
            "MODEL_LABELS[MODEL_NUM_CLASSES]' initializer"
        )

    array_body = labels_match.group("body")
    labels = [decode_c_string(token) for token in C_STRING_PATTERN.findall(array_body)]

    if not labels:
        raise ValueError("MODEL_LABELS does not contain any labels")

    if any(not label.strip() for label in labels):
        raise ValueError("MODEL_LABELS contains an empty label")

    if len(labels) != num_classes:
        raise ValueError(
            f"MODEL_NUM_CLASSES is {num_classes}, but MODEL_LABELS contains "
            f"{len(labels)} labels"
        )

    return num_classes, labels


def generate_sds_yaml(labels: list[str], output_path: Path, frequency: float) -> None:
    document = {
        "sds": {
            "name": "ML output",
            "description": "ML classification results",
            "frequency": frequency,
            "content": [
                {"value": label.upper(), "type": "float"}
                for label in labels
            ],
        }
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as output_file:
        yaml.safe_dump(
            document,
            output_file,
            sort_keys=False,
            default_flow_style=False,
            allow_unicode=True,
            width=4096,
        )


def validate_generated_yaml(output_path: Path, expected_count: int) -> None:
    with output_path.open("r", encoding="utf-8") as output_file:
        generated = yaml.safe_load(output_file)

    try:
        content = generated["sds"]["content"]
    except (TypeError, KeyError) as exc:
        raise ValueError("Generated YAML does not contain sds.content") from exc

    if not isinstance(content, list):
        raise ValueError("Generated YAML sds.content is not a list")

    if len(content) != expected_count:
        raise ValueError(
            f"Generated YAML contains {len(content)} labels, expected "
            f"{expected_count}"
        )


def main() -> int:
    args = parse_arguments()

    try:
        if args.frequency <= 0:
            raise ValueError("Frequency must be greater than 0")

        num_classes, labels = load_model_labels(args.model_config)
        generate_sds_yaml(labels, args.output, args.frequency)
        validate_generated_yaml(args.output, num_classes)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(
        f"Generated {args.output} with {len(labels)} labels at "
        f"frequency={args.frequency}; count matches "
        f"MODEL_NUM_CLASSES={num_classes}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
