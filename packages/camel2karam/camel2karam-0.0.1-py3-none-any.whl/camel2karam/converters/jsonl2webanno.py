# SPDX-FileCopyrightText: 2024-present Marceau <git@marceau-h.fr>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Caution: This script needs you to install the `webanno_tsv` package.
As it is not available on PyPI, we can't include it in the requirements.txt file.
You can install it by running `pip install git+https://github.com/neuged/webanno_tsv`.
"""
from dataclasses import replace
from pathlib import Path
from typing import Set, Iterable, Optional

import polars as pl
from webanno_tsv import Document, Annotation  # https://github.com/neuged/webanno_tsv

from base_converter import BaseConverter


class Jsonl2WebAnno(BaseConverter):
    points: Set[str] = {"!", "?", "."}

    def __init__(self):
        self.layer_defs: Optional[list[tuple[str, list[str]]]] = None
        self.layers: Optional[Set[str]] = None
        self.fields_to_keep: Optional[list[str]] = None

        self.init_fields()

        super().__init__(
            file_glob="*.jsonl",
            output_suffix=".csv",
        )

    def init_fields(self, fields_dict: dict[str, list[str]] | None = None) -> None:
        if fields_dict is not None:
            assert isinstance(fields_dict, dict), f"The kw argument `fields_dict` should be a dict (or None) !"

            self.layer_def = []
            for layer, fields in fields_dict.items():
                assert isinstance(layer, str)
                assert isinstance(fields, Iterable)
                fields = list(fields) if not isinstance(fields, list) else fields

                self.layer_defs.append((layer, fields))

            self.layers = set(fields_dict)
        else:
            self.layer_defs = [("webanno.custom.KARAMLayer", ["pos"]), ]
            self.layers = {"webanno.custom.KARAMLayer", }

        self.fields_to_keep = [
            f for _, fields in self.layer_defs for f in fields
        ]

    def converter(
            self,
            input_path: str | Path,
            output_path: str | Path,
            /,
            **kwargs,
    ) -> None:
        input_path, output_path = self.converter_input_validation(input_path, output_path)

        df = pl.read_ndjson(input_path)
        words = df['word']

        points_index = [i for i, w in enumerate(words) if w.casefold().strip() in self.points]

        sentences = [
            words[:points_index[i]] if i == 0
            else words[points_index[i - 1]:points_index[i]] if i != len(points_index)
            else words[points_index[i - 1]:]
            for i in range(len(points_index) + 1)
        ]

        doc = Document.from_token_lists(sentences)

        annotations = []

        df = df.select(self.fields_to_keep)

        for i, row in enumerate(df.iter_rows(named=True)):
            for attr_field, attr_value in row.items():
                for layer, fields in self.layer_defs:
                    if attr_field in fields:
                        break
                else:
                    print(f"Skipping {attr_field}={attr_value}")
                    continue
                annotations.append(
                    Annotation(
                        tokens=doc.tokens[i:i + 1],
                        layer=layer,
                        field=attr_field,
                        label=attr_value,
                    )
                )

        doc = replace(doc, annotations=annotations, layer_defs=self.layer_defs)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(doc.tsv())


if __name__ == "__main__":
    j2w = Jsonl2WebAnno()

    j2w.folder_converter("../../output/mled_msa", "../../output/mled_msa_webanno")
