# SPDX-FileCopyrightText: 2024-present Marceau <git@marceau-h.fr>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from pathlib import Path

import polars as pl

from base_converter import BaseConverter, PartsMapping


class Csv2Connlu(BaseConverter):
    parts_mapping = PartsMapping(
        FORM=0,
        UPOS=1,
        XPOS=2,
    )

    def __init__(self):
        super().__init__(
            file_glob="*.csv",
            output_suffix=".conllu",
        )

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

        df = pl.read_csv(input_path).fill_nan("_").fill_null("_")

        if pos2_col not in df.columns or pos2_col is None:
            pos2_col = pl.Series("pos2_col", ["_"] * df.shape[0])
        else:
            pos2_col = df[pos2_col]

        sents = self.toks_to_sents(df[word_col], df[pos_col], pos2_col)

        self.write_connlu(output_path, sents, self.parts_mapping)


if __name__ == "__main__":
    c2c = Csv2Connlu()

    c2c.folder_converter(
        "../../output/mled_msa_csv",
        "../../output/mled_msa_conllu_from_csv",
        word_col="word",
        pos_col="pos",
        pos2_col=None
    )
