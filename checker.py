import glob
import os
from datetime import date, datetime
from tabulate import tabulate

# ---------------------------------------------------------------------------
# Target Configuration
#
# Maps a friendly display name to a tuple of potential executable base names.
# Windows Prefetch files follow the convention: <EXE_NAME>-<HASH>.pf
# Multiple aliases cover cases like Unreal Engine packaged binaries
# (e.g., 'Client-Win64-Shipping') vs. launcher wrappers.
# ---------------------------------------------------------------------------
GAMES = {
    "Honkai: Star Rail": ("StarRail",),
    "Genshin Impact": ("GenshinImpact",),
    "Zenless Zone Zero": ("ZenlessZoneZero",),
    "Wuthering Waves": ("Client-Win64-Shipping", "WutheringWaves"),
    "Neverness to Everness": ("NTE", "NevernessToEverness"),
    "Arknights: Endfield": ("Endfield", "ArknightsEndfield"),
}

# Protected system directory where Windows stores application launch metadata
PREFETCH_DIR = r"C:\Windows\Prefetch"


def get_last_run_time(exe_names):
    """Searches the Windows Prefetch directory for artifacts matching the target

    executable names and returns the latest launch timestamp.
    """
    if isinstance(exe_names, str):
        exe_names = (exe_names,)

    all_matches = []
    # Collect all matching .pf files for each alias
    for exe in exe_names:
        # Case-insensitive wildcard match against the executable prefix
        pattern = os.path.join(PREFETCH_DIR, f"{exe.upper()}*.pf")
        all_matches.extend(glob.glob(pattern))

    # If no .pf files exist, the app has never run (or prefetch was purged)
    if not all_matches:
        return None

    # Determine the most recently updated prefetch artifact
    latest_file = max(all_matches, key=os.path.getmtime)
    mtime = os.path.getmtime(latest_file)

    # Windows updates the file modification time upon every process launch
    return datetime.fromtimestamp(mtime)


def check_games_today():
    """Iterates through all configured targets, compares execution timestamps

    against the current calendar date, and prints a formatted status table.
    """
    today = date.today()
    table_data = []

    for game_name, exe_prefixes in GAMES.items():
        last_run = get_last_run_time(exe_prefixes)

        if last_run and last_run.date() == today:
            status = "Yes"
            timestamp = last_run.strftime("%H:%M:%S")
        elif last_run:
            status = "No"
            timestamp = f"Last: {last_run.strftime('%Y-%m-%d %H:%M')}"
        else:
            status = "No"
            timestamp = "No record found"

        table_data.append([game_name, status, timestamp])

    # Display operational status in an aligned terminal table
    print(f"\n--- Daily Login Status ({today.strftime('%A, %d %b %Y')}) ---")
    print(
        tabulate(
            table_data,
            headers=["Game", "Opened Today?", "Time"],
            tablefmt="rounded_outline",
        )
    )


if __name__ == "__main__":
    # Validate directory presence and access permissions
    if not os.path.exists(PREFETCH_DIR):
        print(
            f"Error: Unable to locate {PREFETCH_DIR}. Ensure Prefetch is enabled on this system."
        )
    else:
        try:
            check_games_today()
        except PermissionError:
            # Access to C:\Windows\Prefetch requires elevated NTFS read rights
            print(
                "Permission Error: Please execute via an elevated terminal or Administrator shortcut."
            )