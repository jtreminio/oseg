import json
import os
from oseg import Generator
import argparse

"""Example:
python run.py examples/petstore/openapi.yaml \
    examples/petstore/config-php.yaml \
    examples/petstore/generated/php \
    --example_data_file=examples/petstore/example_data.json
"""

__DIR = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description="OpenApi SDK Example Generator")
parser.add_argument("oas_file", type=str, help="Path to OpenAPI file")
parser.add_argument(
    "sdk_config",
    type=str,
    help="Config file for the target SDK to generate examples for. One of csharp, java, php, python, ruby, typescript-node",
)
parser.add_argument("output_dir", type=str, help="Where to output example files to")
parser.add_argument("--example_data_file", type=str, help="Path to example data file")
parser.add_argument(
    "--operation_id",
    type=str,
    help="If passed, will only generate examples for this Operation ID",
)

args = parser.parse_args()

oas_file: str = args.oas_file
sdk_config: str = args.sdk_config
output_dir: str = args.output_dir
example_data_file: str | None = args.example_data_file
operation_id: str | None = args.operation_id

example_data = None

if example_data_file and os.path.isfile(example_data_file):
    with open(example_data_file, "r", encoding="utf-8") as f:
        example_data = json.load(f)

generator = Generator(
    oas_file=oas_file,
    operation_id=operation_id,
    example_data=example_data,
)


generator.generate(
    config_file=sdk_config,
    output_dir=output_dir,
)
