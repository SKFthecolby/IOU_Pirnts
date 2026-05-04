# file_organizer

Safe Windows-friendly file inventory and organization CLI/TUI.

## Install
```bash
cd file_organizer
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
- Scan all drives: `python findex.py scan --all-drives`
- Scan one drive: `python findex.py scan --drive D:`
- Scan one root: `python findex.py scan --root "D:/Downloads"`
- Search: `python findex.py search "turbo"`
- Edit `rules.yaml` for destinations, protection markers, and conflict behavior.
- Build plan: `python findex.py plan`
- Dry run move: `python findex.py move --dry-run`
- Execute move with explicit typed string: `python findex.py move --yes-confirmation-string "MOVE BATCH <batch_id>"`
- Rollback list: `python findex.py rollback --list`
- Rollback batch dry-run by default: `python findex.py rollback --batch <batch_id>`
- Rollback execute: `python findex.py rollback --batch <batch_id> --execute`

## Safety
- Protected project internals are never included in move plans.
- Actual move requires exact typed confirmation string.
- Scan is read-only by default.
- Every batch writes rollback manifests.
