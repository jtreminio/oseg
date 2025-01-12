import glob
import json
import os
import openapi_pydantic as oa
import yaml
from pathlib import Path
from typing import Optional
from oseg import model


class FileLoader:
    def __init__(self, oas_file: str, example_data_dir: str | None = None):
        self._base_dir = os.path.dirname(oas_file)
        self._example_data_dir = example_data_dir

    @property
    def base_dir(self) -> str:
        return self._base_dir

    def get_file_contents(self, filename: str) -> dict[str, any]:
        if not os.path.isfile(filename):
            return {}

        with open(filename, "r", encoding="utf-8") as f:
            if Path(filename).suffix == ".json":
                return json.load(f)

            return yaml.safe_load(f)

    def get_example_data(self, example_schema: oa.Example) -> dict[str, any] | None:
        """Read example data from external file.

        The filename comes from embedded $ref value in an Example schema.
        Filenames are prepended with the directory where the OAS file is
        located.
        """

        filename = example_schema.value.get("$ref")

        if not filename:
            return None

        filename = f"{self.base_dir}/{filename}"

        try:
            return self.get_file_contents(filename)
        except Exception as e:
            print(f"Error reading example file {filename}")
            print(e)

    def get_example_data_from_custom_file(
        self,
        operation: oa.Operation,
    ) -> Optional["model.CustomExampleData"]:
        """Read example data from external file.

        The filenames are not embedded in the OAS file like in
        ::get_example_data(). Instead, we search a given directory and match
        files using operation ID
        """

        if not self._example_data_dir or not os.path.isdir(self._example_data_dir):
            return None

        base_filename = f"{operation.operationId}__"
        http_key_name = "__http__"

        body = {}
        http: dict[str, any] = {}

        path = os.path.join(self._example_data_dir, f"{base_filename}*")
        for filepath in glob.glob(path):
            data = self.get_file_contents(filepath)

            if not data or not isinstance(data, dict):
                continue

            # Only read http data from first file that has data,
            # for any given operation
            if http_key_name in data:
                if not http:
                    http = data[http_key_name]

                del data[http_key_name]

            example_name = Path(filepath).stem.replace(base_filename, "")

            if example_name == "":
                example_name = "default_example"

            body[example_name] = data

        return model.CustomExampleData(http, body)
