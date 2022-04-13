import yaml

with open('config.yaml') as f:
    _data = yaml.load(f, Loader=yaml.FullLoader)

    MEXC = _data['MEXC']
