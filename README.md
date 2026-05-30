# File_Organizer Walkthrough

This repository contains a **safe file organization tool** located in `file_organizer/`.

The guide below is written to be used directly when you open the repository. It includes **copy/paste command blocks for each step** so you can run the process end-to-end with minimal guesswork.

---

## What this tool does

`file_organizer` provides a Windows-friendly workflow to:

- scan files into an inventory database,
- search and report on what was found,
- generate a move plan,
- run a dry-run before any real move,
- execute guarded moves with a typed confirmation string,
- rollback a batch if needed.

---

## Step 0) Open the tool folder

### Copy this
```bash
cd file_organizer
```

---

## Step 1) Install dependencies

> The activation command below matches the project README (Windows venv activation).

### Copy this
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Step 2) Review configuration before scanning

You should review both files before first run:

- `config.yaml` (database/report/rollback paths)
- `rules.yaml` (destination root, category mappings, extension rules, protections)

### Copy this (PowerShell)
```powershell
notepad .\config.yaml
notepad .\rules.yaml
```

### Copy this (quick terminal view)
```bash
type config.yaml
type rules.yaml
```

---

## Step 3) (Optional) List available drives

### Copy this
```bash
python findex.py drives
```

---

## Step 4) Scan files into inventory

Use **one** of the following patterns.

### Copy this (all drives)
```bash
python findex.py scan --all-drives
```

### Copy this (single drive)
```bash
python findex.py scan --drive D:
```

### Copy this (specific root folder)
```bash
python findex.py scan --root "D:/Downloads"
```

---

## Step 5) Explore what was indexed

### Copy this (text search)
```bash
python findex.py search "turbo"
```

### Copy this (by extension)
```bash
python findex.py ext .pdf
```

### Copy this (by category)
```bash
python findex.py category CAD
```

### Copy this (detected projects)
```bash
python findex.py projects
```

### Copy this (duplicate candidates)
```bash
python findex.py duplicates
```

### Copy this (generate reports)
```bash
python findex.py report
```

---

## Step 6) Build the move plan

This creates planning artifacts such as `move_plan.csv`, `conflicts.csv`, and `protected_skipped.csv` in the reports directory.

### Copy this
```bash
python findex.py plan
```

> Save the printed **batch id**. You need it for execution confirmation.

---

## Step 7) Review plan files before moving

### Copy this (PowerShell)
```powershell
notepad .\_file_index_reports\move_plan.csv
notepad .\_file_index_reports\conflicts.csv
notepad .\_file_index_reports\protected_skipped.csv
```

---

## Step 8) Dry-run the move (recommended every time)

### Copy this
```bash
python findex.py move --dry-run
```

---

## Step 9) Execute the approved move plan

You must pass the exact confirmation string:

`MOVE BATCH <batch_id>`

### Copy this
```bash
python findex.py move --yes-confirmation-string "MOVE BATCH <batch_id>"
```

Example:

### Copy this (example)
```bash
python findex.py move --yes-confirmation-string "MOVE BATCH 20260504_143512"
```

---

## Step 10) Rollback if needed

### Copy this (list rollback manifests)
```bash
python findex.py rollback --list
```

### Copy this (dry-run rollback for a batch)
```bash
python findex.py rollback --batch <batch_id>
```

### Copy this (execute rollback)
```bash
python findex.py rollback --batch <batch_id> --execute
```

---

## Optional: Open the TUI menu

### Copy this
```bash
python findex.py tui
```

---

## Recommended first production run

If this is your first time using the tool on a real machine:

1. Edit `rules.yaml` destination and drive exclusions.
2. Scan a limited folder first (`--root`).
3. Run `report` and `plan`.
4. Review conflicts and protected skips.
5. Run `move --dry-run`.
6. Execute with exact confirmation string.
7. Keep rollback manifest files.

---

## Safety reminders

- Avoid scanning system-sensitive locations unless intentional.
- Always run `plan` and review conflicts before real moves.
- Use `--dry-run` before every execute step.
- Keep rollback manifests for every batch.
