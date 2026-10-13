# Cryptalis research laboratory

Private checkpoint repository authorized by the owner. The original debrato2005/cryptalis repository and original 15-commit mailbox remain unchanged.

## S5 recovery

The full S5 archive is stored in binary parts under checkpoints/s5. With Python 3.12+, run `python checkpoints/s5/restore.py /path/to/new-empty-location`. This verifies every part, the complete archive SHA256, and all 3579 extracted manifest entries. The archive contains the integrated candidate, historical candidates, packaged artifacts, original mailbox, research records, evidence and master inputs.

The root build checklist is newer than the archive's frozen copy. Production qualification remains UNKNOWN. Runtime replays and clean-machine/database qualification are separate from byte recovery. Seven historical lifecycle test failures remain open. Do not use live/customer databases. No credentials, SSH private keys or live runtime homes belong here.

This checkpoint does not yet include the separately inventoried older workspace history bundle or all older evidence. These remain pending preservation; do not interpret this as a complete backup of every accessible workspace file.
