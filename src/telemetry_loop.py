import os
import asyncio
import pandas as pd
from datetime import datetime, timezone

cache_dir = os.path.join(os.getcwd(), "cache", "ff1_cache")  
os.makedirs(cache_dir, exist_ok=True)

os.environ["REQUESTS_CACHE_BACKEND"] = "filesystem"
os.environ["FASTF1_CACHE"] = cache_dir

current_session_key = None

import fastf1 as ff1

ff1.Cache.enable_cache(cache_dir)

telemetry_cache = {
    "session": None,
    "drivers": {},
    "leaderboard": [],
    "weather": {},
    "flags": {}
}

def to_utc(ts):
    if pd.isna(ts):
        return None
    if ts.tzinfo is None:
        return ts.tz_localize("UTC")
    return ts.tz_convert("UTC")

#Gets the current or upcoming F1 event
def get_current_or_upcoming_event(year=2025):
    schedule = ff1.get_event_schedule(year)
    now = datetime.now(timezone.utc)

    for _, event in schedule.iterrows():
        race_time = to_utc(event["Session5"])

        if pd.notna(race_time) and race_time >= now:
            return event
        
    return None

# Gets the current session of the event
def get_current_session(event):
    now = datetime.now(timezone.utc)

    sessions = [
        ("FP1", event["Session1"]),
        ("FP2", event["Session2"]),
        ("FP3", event["Session3"]),
        ("Q",   event["Session4"]),
        ("R",   event["Session5"]),
    ]

    for name, start in sessions:
        if pd.notna(start):
            if start <= now <= start + pd.Timedelta(hours=2):
                return name

    return None

# Telemetry data fetching loop
async def telemetry_loop():
    await asyncio.sleep(5)

    while True:
        session_type = None
        try:

            event = get_current_or_upcoming_event()
            if event is None:   
                await asyncio.sleep(600)
                continue

            session_type = get_current_session(event)
            if session_type is None:
                print("No active session right now")
                await asyncio.sleep(300)
                continue

            session_key = f"{event['EventName']}-{session_type}"
            if session_key != current_session_key:
                session = ff1.get_session(
                    event["Year"],
                    event["EventName"],
                    session_type
                )
                session.load()
                current_session_key = session_key
            else:
                session = ff1.get_session(
                    event["Year"],
                    event["EventName"],
                    session_type
                )

            telemetry_cache["session"] = {
                "event": event,
                "session_type": session_type,
            }

            # Populate leaderboard data
            if not session.laps.empty and "LapTime" in session.laps:
                fastest = (
                    session.laps
                     .groupby("Driver", as_index=False)["LapTime"]
                    .min()
                    .sort_values("LapTime")
                    .reset_index(drop=True)
                )

                leaderboard = []

                leader_time = fastest.iloc[0]["LapTime"]

                for i, row in fastest.iterrows():
                    gap = row["LapTime"] - leader_time
                    leaderboard.append({
                        "position": i + 1,
                        "driver": row["Driver"],
                        "lap_time": str(row["LapTime"]),
                        "gap": "+0.000" if i == 0 else f"+{gap.total_seconds():.3f}s"
                    })

                telemetry_cache["leaderboard"] = leaderboard

            telemetry_cache["drivers"] = {}

            # Populate driver data
            for driver in session.drivers:
                driver_laps = session.laps.pick_driver(driver)
                telemetry_cache["drivers"][driver] = {
                    "laps": len(driver_laps),
                    "last_lap": (
                        str(driver_laps["LapTime"].iloc[-1])
                        if not driver_laps.empty else None
                    )
                }

        except Exception as e:
            print("Telemetry error: ", e)

        if session_type == "R":
            await asyncio.sleep(30)
        elif session_type == "Q":
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(300)