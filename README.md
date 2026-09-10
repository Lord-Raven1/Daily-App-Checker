# Daily App Execution Auditor

A lightweight Windows utility designed to answer a single question without the bloat:

> **"Did I launch these apps today?"**

Instead of running a resident background daemon that polls active processes 24/7, this script performs **on-demand forensic checks** against the Windows Prefetch cache (`C:\Windows\Prefetch`).

---

## Why Not Just Run a Background Script?

Traditional monitoring tools sit in memory and constantly iterate through `psutil` or poll the Windows process table.

This script has **zero runtime footprint**:

- **Zero CPU/RAM overhead** — Runs only when invoked, evaluates in milliseconds, and immediately exits.
- **Native OS telemetry** — Reads Windows `.pf` file metadata created automatically by the OS cache manager.
- **Deterministic history** — Checks past activity even if the application was opened and closed hours ago while the script wasn't running.

---

## How It Works

The auditor follows three simple steps:

1. **Target Disambiguation**  
   Checks configured targets against known executable names and engine fallback signatures, such as Unreal Engine shipping binaries versus custom wrappers.

2. **Prefetch Query**  
   Locates matching `.pf` artifacts in `%SystemRoot%\Prefetch`.

3. **Temporal Diff**  
   Compares the latest artifact timestamp against `datetime.date.today()` to determine whether the application was launched today.

### Example Output

```text
┌───────────────────────┬───────────────┬──────────┐
│ Target                │ Opened Today? │ Time     │
├───────────────────────┼───────────────┼──────────┤
│ Honkai: Star Rail     │ Yes           │ 08:14:22 │
│ Genshin Impact        │ No            │ Last: ...│
└───────────────────────┴───────────────┴──────────┘
```

---

## Setup & Configuration

### 1. Install Dependencies

Install the required Python package using `pip`:

```bash
pip install tabulate
```

### 2. Define Monitored Binaries

Configure the applications you want to monitor in **`checker.py`**:

```python
GAMES = {
    "App Title": ("MainExecutable", "AlternativeFallback"),
}
```

For example:

```python
GAMES = {
    "Honkai: Star Rail": ("StarRail.exe", "StarRailBase.exe"),
    "Genshin Impact": ("GenshinImpact.exe", "YuanShen.exe"),
}
```

### 3. Run with Administrator Privileges

Because `C:\Windows\Prefetch` is a protected Windows directory, the script may require **Administrator privileges** to access the required files.

A clean way to handle this is to run the script through a batch file and configure a shortcut to use:

> **Run as administrator**

---

## Requirements

- Windows
- Python 3.x
- `tabulate`
- Administrator privileges

---

## Project Structure

```text
Daily-App-Execution-Auditor/
│
├── checker.py
├── run.bat
└── README.md
```

---

## Notes

This utility relies on the Windows Prefetch system and is therefore intended specifically for **Windows environments**.

Prefetch data is maintained by Windows and is not intended to be a complete application usage history. Results should therefore be interpreted as an indicator of application execution rather than a guaranteed audit log.