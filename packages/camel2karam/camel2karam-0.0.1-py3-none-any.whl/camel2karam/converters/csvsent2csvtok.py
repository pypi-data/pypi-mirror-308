# SPDX-FileCopyrightText: 2024-present Marceau <git@marceau-h.fr>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from pathlib import Path
from typing import Optional

import polars as pl

from base_converter import BaseConverter


class CsvSent2CsvTok(BaseConverter):
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
        self.converter_input_validation(input_path, output_path)

        if output_path.exists() and output_path.is_dir():
            output_path = output_path / input_path.with_suffix(".conllu").name

        df = pl.read_csv(input_path).fill_nan("").fill_null("")

        if pos2_col is None or pos_col not in df.schema:
            pos2_col = "pos2"
            words, poss, pos2s = [], [], None

            df = df.with_columns(
                pl.lit("").alias("pos2")
            )
        else:
            words, poss, pos2s = [], [], []

        df = df.select([word_col, pos_col, pos2_col])


        for row in df.iter_rows():
            word, pos, pos2 = row
            word, pos, pos2 = word.split(" | "), pos.split(" | "), pos2.split(" | ")

            assert len(word) == len(pos)

            words.extend(word)
            poss.extend(pos)

            if pos2s is not None:
                pos2s.extend(pos2)

        if pos2s is None:
            new_df = pl.DataFrame({
                word_col: words,
                pos_col: poss
            })
        else:
            new_df = pl.DataFrame({
                word_col: words,
                pos_col: poss,
                pos2_col: pos2s
            })


        new_df.write_csv(output_path)

if __name__ == "__main__":
    cs2ct = CsvSent2CsvTok()

    cs2ct.folder_converter(
        "../../output/mled_msa_csv_sent",
        "../../output/mled_msa_csv_sent_tok",
        word_col="word",
        pos_col="pos",
        pos2_col=None
    )

