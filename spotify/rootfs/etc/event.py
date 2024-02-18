#!/usr/bin/python3

import os

import requests


def update_state(state: int | str):
    home_assistant_token = os.environ["SUPERVISOR_TOKEN"]

    req = requests.post(
        f"http://supervisor/core/api/states/sensor.spotify_connect",
        headers={
            "Authorization": f"Bearer {home_assistant_token}",
            "Content-Type": "application/json",
        },
        json={
            "state": state,
            "attributes": {
                "friendly_name": "Spotify Connect",
                "icon": "mdi:spotify",
            },
        },
    )

    req.raise_for_status()


match os.environ["PLAYER_EVENT"]:
    case "changed":
        old_track_id = os.environ["OLD_TRACK_ID"]
        new_track_id = os.environ["TRACK_ID"]
        update_state("playing" if new_track_id else "paused")

    case "started":
        track_id = os.environ["TRACK_ID"]
        update_state("playing")

    case "stopped":
        track_id = os.environ["TRACK_ID"]
        update_state("idle")

    case "playing":
        track_id = os.environ["TRACK_ID"]
        track_duration_ms = os.environ["DURATION_MS"]
        track_position_ms = os.environ["POSITION_MS"]
        update_state("playing")

    case "paused":
        track_id = os.environ["TRACK_ID"]
        track_duration_ms = os.environ["DURATION_MS"]
        track_position_ms = os.environ["POSITION_MS"]
        update_state("paused")

    case "preloading":
        track_id = os.environ["TRACK_ID"]
        update_state("buffering")

    case "volume_set":
        volume = os.environ["VOLUME"]

    case "sink":
        status = os.environ["SINK_STATUS"]
        match status:
            case "running":
                pass
            case "temporarily_closed":
                pass
            case "closed":
                pass
