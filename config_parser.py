import json

def parse_config(file: str) -> None:
    try:
        with open(file, 'r') as f:
            data = json.load(f)
            print(data)

    except FileNotFoundError:
        print(f'{file} file dosent exist')

parse_config('config.json')
