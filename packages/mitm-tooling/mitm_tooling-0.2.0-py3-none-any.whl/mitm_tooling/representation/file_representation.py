from collections.abc import Iterable

import pandas as pd

from mitm_tooling.definition.definition_tools import map_col_groups
from mitm_tooling.definition import ConceptLevel, MITMDefinition, ConceptName, ConceptKind
from mitm_tooling.utilities.python_utils import elem_wise_eq, normalize_into_dict


def mk_concept_file_header(mitm_def: MITMDefinition, concept: ConceptName, k: int) -> pd.Index:
    concept_properties = mitm_def.concept_properties[concept]
    concept_relations = mitm_def.concept_relations[concept]

    columns, _ = map_col_groups(mitm_def, concept, {
        'kind': lambda: 'kind',
        'type': lambda: concept_properties.typing_concept,
        'identity': lambda: concept_relations.identity.keys(),
        'inline': lambda: concept_relations.inline.keys(),
        'foreign': lambda: [
            (name for fk_info in concept_relations.foreign.values() for name in fk_info.fk_relations)],
        'attributes': lambda: [f'a_{i}' for i in range(1, k + 1)],
    })

    columns = []

    def add_cols(cols: Iterable[str]):
        columns.extend((c for c in cols if c not in columns))

    for column_group in concept_properties.column_group_ordering:
        match column_group:
            case 'kind' if any(elem_wise_eq(concept_properties.nature, (ConceptLevel.Sub, ConceptKind.Abstract))):
                # concept_properties.nature[0] is ConceptLevel.Sub or concept_properties.nature[1] is ConceptKind.Abstract
                add_cols(['kind'])
            case 'type':
                add_cols([concept_properties.typing_concept])
            case 'identity-relations':
                # not really deterministic due to unspecified key ordering (on mitm file definition level; within this python program, it should be consistent due to guaranteed set ordering)
                add_cols(concept_relations.identity.keys())
            case 'inline-relations':
                add_cols(concept_relations.inline.keys())
            case 'foreign-relations':
                add_cols(concept_relations.foreign.keys())
            case 'attributes' if concept_properties.permit_attributes:
                add_cols((f'a_{i}' for i in range(1, k + 1)))
    return pd.Index(columns)
