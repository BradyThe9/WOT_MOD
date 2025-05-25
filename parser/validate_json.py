#!/usr/bin/env python3
import argparse
import json
import sys
from jsonschema import validate
from jsonschema.exceptions import ValidationError

def main():
    parser = argparse.ArgumentParser(
        description="Validiert ein WoT-Replay-JSON gegen unser Schema"
    )
    parser.add_argument(
        "-i", "--input", required=True, help="Pfad zu reports/last_battle.json"
    )
    parser.add_argument(
        "-s", "--schema", required=True, help="Pfad zu parser/schema.json"
    )
    args = parser.parse_args()

    with open(args.schema, "r", encoding="utf-8") as f:
        schema = json.load(f)
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    try:
        validate(instance=data, schema=schema)
        print("[✓] JSON ist schema-konform.")
    except ValidationError as e:
        print("[✗] Schema-Fehler:", e.message)
        sys.exit(1)

if __name__ == "__main__":
    main()
