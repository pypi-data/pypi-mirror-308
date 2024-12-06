from importlib.resources import files
import json
import yaml

class StatsProcessor:
    @classmethod
    def load_txt(cls, filename, json_load = True):
        txt_path = files('neurostats_API.tools').joinpath(filename)
        with open(txt_path, 'r', encoding='utf-8') as f:
            data = json.load(f) if (json_load) else f.read() 
        return data
    @classmethod
    def load_yaml(cls, filename):
        yaml_path = files('neurostats_API.tools').joinpath(filename)
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        return data