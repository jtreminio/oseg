import json
import os
import openapi_pydantic as oa
import re
import yaml
from pathlib import Path


class FileLoader:
    def __init__(self, oas_file: str, example_data_dir: str | None = None):
        self._oas_file = oas_file
        self._base_dir = os.path.dirname(oas_file)
        self._example_data_file_list: dict[str, str] = {}

        self._read_example_data_dir(example_data_dir)

    @property
    def base_dir(self) -> str:
        return self._base_dir

    def oas(self):
        return self.get_file_contents(self._oas_file)

    def get_file_contents(self, filename: str) -> dict[str, any]:
        if not os.path.isfile(filename):
            return {}

        with open(filename, "r", encoding="utf-8") as f:
            if Path(filename).suffix == ".json":
                results = json.load(f)
            else:
                results = yaml.safe_load(f)

            return results if isinstance(results, dict) else {}

    def get_example_data(self, example_schema: oa.Example) -> dict[str, any] | None:
        """Read example data from external file.

        The filename comes from embedded $ref value in an Example schema.
        Filenames are prepended with the directory where the OAS file is
        located.
        """

        if not isinstance(example_schema.value, dict):
            return None

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
    ) -> dict[str, dict[str, any]]:
        """Read example data from external file.

        The filenames are not embedded in the OAS file like in
        ::get_example_data(). Instead, we search a given directory and match
        files using operation ID
        """

        if not self._example_data_file_list:
            return {}

        # example: "addPet__default_example.json"
        base_filename = f"{operation.operationId}__"
        r = re.compile(f".*/{base_filename}.*")
        results = {}

        for filename in list(filter(r.match, self._example_data_file_list)):
            data = self.get_file_contents(filename)

            if not data or not isinstance(data, dict):
                continue

            results[Path(filename).stem] = data

        return results

    def _read_example_data_dir(self, example_data_dir: str | dict | None) -> None:
        if (
            not example_data_dir
            or not isinstance(example_data_dir, str)
            or not os.path.isdir(example_data_dir)
        ):
            return

        self._example_data_file_list = [
            f"{example_data_dir}/{f}"
            for f in os.listdir(example_data_dir)
            if os.path.isfile(os.path.join(example_data_dir, f))
        ]
