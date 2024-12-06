from collections import defaultdict

import sqlalchemy as sa
from pydantic_core import Url

from sqlalchemy_utils import view

from mitm_tooling.data_types import MITMDataType
from mitm_tooling.definition import ConceptName, MITM, get_mitm_def, ConceptKind, ConceptLevel, RelationName
from mitm_tooling.definition.definition_tools import map_col_groups, ColGroupMaps
from mitm_tooling.extraction.sql.db import create_sa_engine
from .intermediate_representation import Header
from mitm_tooling.utilities.sql_utils import qualify


def mk_concept_table_name(mitm: MITM, concept: ConceptName) -> str:
    return get_mitm_def(mitm).get_properties(concept).plural


def mk_type_table_name(mitm: MITM, concept: ConceptName, type_name: RelationName) -> str:
    return get_mitm_def(mitm).get_properties(concept).key + '_' + type_name.lower()


def mk_link_table_name(mitm: MITM, concept: ConceptName, type_name: RelationName, fk_name: RelationName) -> str:
    return mk_type_table_name(mitm, concept, type_name) + '_' + fk_name.lower()


def mk_db_schema(header: Header):
    mitm_def = get_mitm_def(header.mitm)
    meta = sa.MetaData()

    concept_level_view_members: dict[ConceptName, list[list[sa.Column]]] = defaultdict(list)
    tables: dict[ConceptName, list[sa.Table]] = {}
    views: dict[ConceptName, sa.Table] = {}

    for he in header.header_entries:
        he_concept = he.concept
        concept_properties = mitm_def.get_properties(he_concept)
        concept_relations = mitm_def.get_relations(he_concept)
        assert concept_properties is not None and concept_relations is not None

        table_name = mk_type_table_name(header.mitm, he_concept, he.type_name)

        columns, created_columns = map_col_groups(mitm_def, he_concept, {
            'kind': lambda: ('kind', sa.Column('kind', MITMDataType.Text.sa_sql_type, nullable=False)),
            'type': lambda: (concept_properties.typing_concept, sa.Column(concept_properties.typing_concept,
                                                                          MITMDataType.Text.sa_sql_type,
                                                                          nullable=False)),
            'identity': lambda: [(name, sa.Column(name, dt.sa_sql_type, nullable=False)) for
                                 name, dt in
                                 mitm_def.resolve_identity_type(he_concept).items()],
            'inline': lambda: [(name, sa.Column(name, dt.sa_sql_type)) for name, dt in
                               mitm_def.resolve_inlined_types(he_concept).items()],
            'foreign': lambda: [(name, sa.Column(name, dt.sa_sql_type)) for _, resolved_fk in
                                mitm_def.resolve_foreign_types(he_concept).items() for name, dt in
                                resolved_fk.items()],
            'attributes': lambda: [(name, sa.Column(name, dt.sa_sql_type)) for name, dt in
                                   zip(he.attributes, he.attribute_dtypes)],
        }, ensure_unique=True)

        constraints = []
        if concept_relations.identity:
            constraints.append(sa.PrimaryKeyConstraint(*(created_columns[c] for c in concept_relations.identity)))

        for fk_name, fk_info in concept_relations.foreign.items():
            cols, refcols = zip(*fk_info.fk_relations.items())
            fkc = sa.ForeignKeyConstraint(name=fk_name, columns=[created_columns[c] for c in cols], refcolumns=[
                sa.literal_column(qualify(table=mk_concept_table_name(header.mitm, fk_info.target_concept), column=c))
                for c in refcols])
            # constraints.append(fkc)

        t = sa.Table(table_name, meta, *columns, *constraints)

        if he_concept not in tables:
            tables[he_concept] = []
        tables[he_concept].append(t)

        if concept_relations.identity:
            outer_pk = []
            if not concept_properties.typing_concept in concept_relations.identity:
                outer_pk.append(created_columns[concept_properties.typing_concept])
            outer_pk.extend((created_columns[identity_col] for identity_col in concept_relations.identity))
            concept_level_view_members[he_concept].append(outer_pk)

    for concept, members in concept_level_view_members.items():
        view_selection = sa.union_all(*(sa.select(*pk_cols) for pk_cols in members))
        views[concept] = view.create_materialized_view(mk_concept_table_name(header.mitm, concept), view_selection,
                                                       meta)

    return meta, tables, views


def mk_sqlite(header: Header, file_path: str | None = ':memory:'):
    engine = create_sa_engine(Url(f'sqlite:///{file_path}'))
    meta, tables, views = mk_db_schema(header)
    print(meta.tables)
    print([f'{t.name}: {t.columns} {t.constraints}' for ts in tables.values() for t in ts])
    print([f'{t.name}: {t.columns} {t.constraints}' for t in views.values()])
    meta.create_all(engine)
