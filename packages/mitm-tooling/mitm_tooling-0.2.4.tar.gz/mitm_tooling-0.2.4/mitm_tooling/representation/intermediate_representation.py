import itertools
from typing import TYPE_CHECKING

import pandas as pd
import pydantic

from mitm_tooling.data_types.data_types import MITMDataType
from mitm_tooling.definition.definition_representation import ConceptName, MITM
from mitm_tooling.extraction.sql.data_models.table_identifiers import ColumnName


class HeaderEntry(pydantic.BaseModel):
    concept: ConceptName
    kind: ConceptName
    type_name: str
    attributes: list[ColumnName]
    attribute_dtypes: list[MITMDataType]

    def get_k(self) -> int:
        return len(self.attributes)

    def to_row(self) -> list[str | None]:
        return [self.kind, self.type_name] + list(
            itertools.chain(*zip(self.attributes, map(str, self.attribute_dtypes))))

class Header(pydantic.BaseModel):
    mitm: MITM
    header_entries: list[HeaderEntry]

    @classmethod
    def generate_header_columns(cls, k: int) -> list[str]:
        return ['kind', 'type'] + list(
            itertools.chain(*((f'a_{i}', f'a_dt_{i}') for i in range(1, k + 1))))

    def generate_header_df(self) -> pd.DataFrame:
        k = max(map(lambda he: he.get_k(), self.header_entries), default=0)
        deduplicated = {}
        for he in self.header_entries:
            deduplicated[(he.kind, he.type_name)] = he
        lol = [he.to_row() for he in deduplicated.values()]
        return pd.DataFrame(data=lol, columns=Header.generate_header_columns(k))