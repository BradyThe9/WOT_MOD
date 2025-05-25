#!/usr/bin/env python3
import argparse
import json

def compute_metrics(data: dict) -> dict:
    perf   = data["battle_performance"][0]
    common = data["common"][0]

    duration_min = common["duration"] / 60.0  # Sekunden → Minuten
    damage       = perf["damage_dealt"]
    kills        = perf["kills"]
    died         = perf["death_count"] > 0
    won          = (perf["team"] == common["winner_team"])

    return {
        "damage_per_minute": round(damage / duration_min, 2),
        "kills_per_minute":  round(kills / duration_min, 3),
        "survived":          int(not died),
        "won_match":         int(won)
    }

def main():
    parser = argparse.ArgumentParser(description="Berechne Basis-Kennzahlen aus last_battle.json")
    parser.add_argument("-i", "--input", required=True, help="Pfad zur JSON-Datei")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    metrics = compute_metrics(data)
    for k, v in metrics.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
