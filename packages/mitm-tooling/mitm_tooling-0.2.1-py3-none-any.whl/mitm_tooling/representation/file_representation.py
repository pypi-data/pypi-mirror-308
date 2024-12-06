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

    return pd.Index(columns)
