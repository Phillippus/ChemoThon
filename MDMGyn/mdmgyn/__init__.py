"""MDM Gyn — deterministický nástroj klinickej podpory pre gynekologickú onkológiu.

Balík obsahuje:
- schema.py   : pydantic schéma jedného záznamu znalostnej databázy (KB)
- entities.py : definícia entít a polí wizardu (čisto formulárová konfigurácia, žiadny klinický obsah)
- kb_loader.py: načítanie a validácia YAML KB
- matching.py : deterministický matching engine nad KB

KRITICKÉ: V tomto balíku NIE JE žiadny klinický obsah ani LLM. Všetky odporúčania
a kritériá žijú v ./kb/*.yaml a sú validované pydanticom. Engine len deterministicky
páruje vstupy používateľa so záznamami KB.
"""

__all__ = ["schema", "entities", "kb_loader", "matching"]
