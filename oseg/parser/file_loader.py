from pathlib import Path
import json
import yaml


class FileLoader:
    @staticmethod
    def get_file_contents(filename: str) -> any:
        file = open(filename, "r")

        if Path(filename).suffix == ".json":
            data = json.load(file)
        else:
            data = yaml.safe_load(file)

        file.close()

        return data
