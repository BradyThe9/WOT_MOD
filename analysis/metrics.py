import argparse
import json

def compute_metrics(data: dict) -> dict:
    perf   = data["battle_performance"][0]
    common = data["common"][0]

    # Dauer in Minuten
    duration_min = common["duration"] / 60.0

    # Basis-Metriken
    damage   = perf.get("damage_dealt", 0)
    kills    = perf.get("kills", 0)
    died     = perf.get("death_count", 0) > 0
    won      = (perf.get("team") == common.get("winner_team"))

    # Erweiterte Metriken
    spots            = perf.get("spotted_enemies", 0)
    damage_received  = perf.get("damage_received", 0)
    assisted_radio   = perf.get("damage_assisted_radio", 0)
    assisted_track   = perf.get("damage_assisted_track", 0)
    shots            = perf.get("shots", 0)
    hits             = perf.get("hits", 0)
    capture_points   = perf.get("capture_points", 0)

    return {
        # Basis
        "damage_per_minute":        round(damage / duration_min, 2) if duration_min > 0 else 0,
        "kills_per_minute":         round(kills / duration_min, 3) if duration_min > 0 else 0,
        "survived":                 int(not died),
        "won_match":                int(won),

        # Erweiterung
        "spots_per_minute":         round(spots / duration_min, 3) if duration_min > 0 else 0,
        "damage_received_per_minute": round(damage_received / duration_min, 2) if duration_min > 0 else 0,
        "assist_damage_per_minute": round((assisted_radio + assisted_track) / duration_min, 2) if duration_min > 0 else 0,
        "hit_ratio_percent":        round((hits / shots * 100), 1) if shots > 0 else 0,
        "capture_points_per_minute": round(capture_points / duration_min, 2) if duration_min > 0 else 0
    }

def main():
    parser = argparse.ArgumentParser(
        description="Berechne erweiterte Kennzahlen aus last_battle.json"
    )
    parser.add_argument(
        "-i", "--input", required=True, help="Pfad zur JSON-Datei (reports/last_battle.json)"
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    metrics = compute_metrics(data)

    # Ausgeben
    for key, value in metrics.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
