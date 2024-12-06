import dataclasses
import io
import logging
import os
import zipfile
from abc import ABC, abstractmethod
from typing import BinaryIO, Iterator

import pandas as pd

from mitm_tooling.definition import MITM, ConceptName, get_mitm_def
from mitm_tooling.representation.intermediate_representation import HeaderEntry, Header

logger = logging.getLogger('api')


@dataclasses.dataclass
class FileExport(ABC):
    mitm: MITM
    filename: str

    @abstractmethod
    def into(self, into: os.PathLike | BinaryIO):
        pass

    def to_buffer(self) -> io.BytesIO:
        buffer = io.BytesIO()
        self.into(buffer)
        buffer.seek(0)
        return buffer

    def into_file(self, path: os.PathLike):
        self.into(path)


@dataclasses.dataclass
class InMemoryExport(FileExport):
    header: Header
    data: dict[ConceptName, pd.DataFrame]

    def into(self, into: os.PathLike | BinaryIO):
        mitm_def = get_mitm_def(self.mitm)

        with zipfile.ZipFile(into, mode='w', compression=zipfile.ZIP_DEFLATED) as f:
            with f.open('header.csv', 'w') as hf:
                self.header.generate_header_df().to_csv(hf, header=True, index=False, sep=';')
            for c, df in self.data.items():
                table_name = mitm_def.get_properties(c).plural
                with f.open(f'{table_name}.csv', 'w') as cf:
                    df.to_csv(cf, header=True, index=False, sep=';', date_format='%Y-%m-%dT%H:%M:%S.%f%z')
                    logger.debug(f'Wrote {len(df)} rows to {table_name}.csv (in-memory export).')


@dataclasses.dataclass
class StreamingExport(FileExport):
    data_sources: dict[ConceptName, tuple[pd.DataFrame, list[Iterator[tuple[pd.DataFrame, list[HeaderEntry]]]]]]

    def into(self, into: os.PathLike | BinaryIO):
        mitm_def = get_mitm_def(self.mitm)
        collected_header_entries = []

        with zipfile.ZipFile(into, mode='w', compression=zipfile.ZIP_DEFLATED) as f:
            for c, (structure_df, chunk_iterators) in self.data_sources.items():
                table_name = mitm_def.get_properties(c).plural
                with f.open(f'{table_name}.csv', 'w') as cf:
                    structure_df.to_csv(cf, header=True, index=False, sep=';', date_format='%Y-%m-%dT%H:%M:%S.%f%z')
                    for df_chunks in chunk_iterators:
                        for df_chunk, header_entries in df_chunks:
                            collected_header_entries.extend(header_entries)
                            df_chunk.to_csv(cf, header=False, index=False, sep=';',
                                            date_format='%Y-%m-%dT%H:%M:%S.%f%z')
                            logger.debug(f'Wrote {len(df_chunk)} rows to {table_name}.csv (streaming export).')

            with f.open('header.csv', 'w') as hf:
                header_df = Header(mitm=self.mitm, header_entries=header_entries).generate_header_df()
                header_df.to_csv(hf, header=True, index=False, sep=';')
