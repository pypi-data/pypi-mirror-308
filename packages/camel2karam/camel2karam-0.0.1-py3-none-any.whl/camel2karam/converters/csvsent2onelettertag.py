# SPDX-FileCopyrightText: 2024-present Marceau <git@marceau-h.fr>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from pathlib import Path
from typing import Optional

import polars as pl

from base_converter import BaseConverter


class CsvSent2OneLetterTag(BaseConverter):
    corresp = {
        "PART": "P",
        "NOUN": "N",
        "PUNC": "Z",
        "VERB": "V",
        "DIGIT": "D",
        "NOUN_OR_PART": "N",
    }

    @classmethod
    def transform(cls, liste):
        return " | ".join([cls.corresp.get(tag.upper(), "X") for tag in liste.split(" | ")])

    def __init__(self):
        super().__init__(
            file_glob="*.csv",
            output_suffix=".csv",
        )

    def converter(
            self,
            input_path: str | Path,
            output_path: str | Path,
            /,
            word_col: str = "word",
            pos_col: str = "pos",
            pos2_col: Optional[str] = "xpos",
            **kwargs,
    ) -> None:
        input_path, output_path = self.converter_input_validation(input_path, output_path)

        df = pl.read_csv(input_path).fill_nan("").fill_null("")

        if pos2_col is None or pos_col not in df.schema:
            pos2_col = "empty_col"
            df = df.with_columns(
                pl.lit("").alias("empty_col")
            )

        df = df.select([word_col, pos_col, pos2_col])
        df = df.with_columns(
            pl.col(pos_col).map_elements(self.transform, return_dtype=pl.String).alias(pos_col),
            pl.col(pos2_col).map_elements(self.transform, return_dtype=pl.String).alias(pos2_col),
        )

        if pos2_col == "empty_col":
            df = df.select([word_col, pos_col])

        df.write_csv(output_path)

if __name__ == "__main__":
    cs2olt = CsvSent2OneLetterTag()

    cs2olt.folder_converter(
        "../../output/mled_msa_csv_sent",
        "../../output/mled_msa_csv_sent_olt",
        word_col="word",
        pos_col="pos",
        pos2_col=None
    )

