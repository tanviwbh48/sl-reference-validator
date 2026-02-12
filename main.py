import json
import sys
from validator import validate


def cli_mode():
    if len(sys.argv) != 2:
        print("Usage: python main.py <input.json>")
        return

    file_path = sys.argv[1]

    with open(file_path, "r") as f:
        sentence = json.load(f)

    result = validate(sentence)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    cli_mode()
