"""Načítanie a validácia znalostnej databázy (KB) z YAML.

Validácia je tvrdá: ak ktorýkoľvek záznam nezodpovedá schéme (chýba povinné pole,
nekonzistentný reviewed stav, neznáma spoločnosť/modul...), vyhodí sa výnimka.
Tým pádom pytest aj prípadná CI zlyhajú skôr, než sa nekompletný obsah dostane do appky.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import yaml
from pydantic import ValidationError

from .schema import Entity, Recommendation

KB_DIR = Path(__file__).resolve().parent.parent / "kb"

_KB_FILES = {
    Entity.HL: "hl.yaml",
    Entity.DLBCL: "dlbcl.yaml",
    Entity.FL: "fl.yaml",
    Entity.MCL: "mcl.yaml",
    Entity.MZL: "mzl.yaml",
    Entity.PTCL: "ptcl.yaml",
}


class KBError(Exception):
    """Chyba pri načítaní/validácii znalostnej databázy."""


def _load_file(path: Path) -> List[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if data is None:
        return []
    if not isinstance(data, list):
        raise KBError(f"{path.name}: očakával sa zoznam záznamov, nájdené {type(data).__name__}.")
    return data


def load_kb(kb_dir: Path | None = None) -> List[Recommendation]:
    """Načíta a zvaliduje všetky záznamy KB. Vyhodí KBError pri akejkoľvek chybe."""
    kb_dir = kb_dir or KB_DIR
    records: List[Recommendation] = []
    seen_ids: Dict[str, str] = {}

    for entity, filename in _KB_FILES.items():
        path = kb_dir / filename
        raw_records = _load_file(path)
        for idx, raw in enumerate(raw_records):
            if not isinstance(raw, dict):
                raise KBError(f"{filename}[{idx}]: záznam musí byť mapa (dict).")
            try:
                rec = Recommendation(**raw)
            except ValidationError as exc:
                rec_id = raw.get("id", f"#{idx}")
                raise KBError(f"{filename}: neplatný záznam '{rec_id}':\n{exc}") from exc

            if rec.entity != entity:
                raise KBError(
                    f"{filename}: záznam '{rec.id}' má entity='{rec.entity.value}', "
                    f"očakávalo sa '{entity.value}'."
                )
            if rec.id in seen_ids:
                raise KBError(
                    f"Duplicitné id '{rec.id}' v {filename} aj {seen_ids[rec.id]}."
                )
            seen_ids[rec.id] = filename
            records.append(rec)

    return records


def kb_by_entity(records: List[Recommendation] | None = None) -> Dict[Entity, List[Recommendation]]:
    records = records if records is not None else load_kb()
    out: Dict[Entity, List[Recommendation]] = {e: [] for e in Entity}
    for rec in records:
        out[rec.entity].append(rec)
    return out
