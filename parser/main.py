#!/usr/bin/env python3
import argparse
import json
import datetime
from wotreplay import ReplayData

def to_dict(obj):
    """
    Konvertiert NamedTuples, Listen, Datetimes und Dictionaries rekursiv
    in reine Python-Dicts/Listen/Strings.
    """
    # datetime → ISO-String
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    # NamedTuple (hat _asdict)
    if hasattr(obj, "_asdict"):
        return obj._asdict()
    # NamedTuple ohne _asdict (hat _fields)
    if hasattr(obj, "_fields"):
        return {field: to_dict(getattr(obj, field)) for field in obj._fields}
    # dict
    if isinstance(obj, dict):
        return {key: to_dict(val) for key, val in obj.items()}
    # list oder tuple
    if isinstance(obj, (list, tuple)):
        return [to_dict(item) for item in obj]
    # alles andere (int, float, str, bool, None)
    return obj

def parse_replay(input_path: str) -> dict:
    """
    Liest die .wotreplay-Datei ein und gibt ein Dictionary mit allen wichtigen Sektionen zurück.
    """
    replay = ReplayData(file_path=input_path, db_path='', db_name='', load=False)
    return {
        "battle_metadata":     to_dict(replay.battle_metadata),
        "battle_performance":  to_dict(replay.battle_performance),
        "common":              to_dict(replay.common),
        "battle_frags":        to_dict(replay.battle_frags),
        "battle_economy":      to_dict(replay.battle_economy),
        "battle_xp":           to_dict(replay.battle_xp),
    }

def main():
    parser = argparse.ArgumentParser(description="WOT-Replay → JSON Converter")
    parser.add_argument("-i", "--input",  required=True, help="Pfad zur .wotreplay-Datei")
    parser.add_argument("-o", "--output", required=True, help="Pfad zur Ausgabedatei (JSON)")
    args = parser.parse_args()

    data = parse_replay(args.input)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[✓] JSON geschrieben: {args.output}")

if __name__ == "__main__":
    main()
