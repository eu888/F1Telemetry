import fastf1
import asyncio

telemetry_cache = {
    "session": None,
    "drivers": {},
    "leaderboard": [],
    "weather": {},
    "flags": {}
}

async def telemetry_loop():
    await asyncio.sleep(5)

    while True:
        try:
            session = fastf1.get_session(2025, 'Monaco', 'R')
            session.load(laps=False, telemetry=False)

            telemetry_cache["session"] = session.session_info
            telemetry_cache["leaderboard"] = (
                session.laps
                .groupby("Driver")["LapTime"]
                .min()
                .sort_values()
                .index
                .tolist()
            )

            for driver in session.drivers:
                telemetry_cache["drivers"][driver] = {
                    "laps": len(session.laps.pick_driver(driver)),
                    "last_lap": session.laps.pick_driver(driver).iloc[-1]["LapTime"]
                }

        except Exception as e:
            print("Telemetry error: ", e)

        await asyncio.sleep(10)