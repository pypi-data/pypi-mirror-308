# SPDX-FileCopyrightText: 2024-present Marceau <git@marceau-h.fr>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from pathlib import Path

import polars as pl

from base_converter import BaseConverter


class CsvTok2CsvSent(BaseConverter):
    def __init__(self):
        super().__init__(
            file_glob="*.csv",
            output_suffix=".csv",
        )

    def toks_to_sents_zipped_unzipped(self, words, pos, pos2=None):
        res = self.toks_to_sents(words, pos) if pos2 is None else self.toks_to_sents(words, pos, pos2)
        return zip(*((" | ".join(e) for e in zip(*s)) for s in res))

    def converter(
            self,
            input_path: str | Path,
            output_path: str | Path,
            /,
            word_col: str = "word",
            pos_col: str = "pos",
            pos2_col: str = "xpos",
            **kwargs,
    ) -> None:
        input_path, output_path = self.converter_input_validation(input_path, output_path)

        df = pl.read_csv(input_path).fill_nan("").fill_null("")

        if pos2_col is None:
            w_col, p_col = self.toks_to_sents_zipped_unzipped(df[word_col], df[pos_col])
            new_df = pl.DataFrame({word_col: w_col, pos_col: p_col})

        else:
            w_col, p_col, p2_col = self.toks_to_sents_zipped_unzipped(df[word_col], df[pos_col], df[pos2_col])
            new_df = pl.DataFrame({word_col: w_col, pos_col: p_col, pos2_col: p2_col})

        new_df.write_csv(output_path)


if __name__ == "__main__":
    ct2cs = CsvTok2CsvSent()

    ct2cs.folder_converter(
        "../../output/mled_msa_csv",
        "../../output/mled_msa_csv_sent",
        word_col="word",
        pos_col="pos",
        pos2_col=None
    )
