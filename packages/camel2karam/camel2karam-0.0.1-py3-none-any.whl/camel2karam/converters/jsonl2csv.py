# SPDX-FileCopyrightText: 2024-present Marceau <git@marceau-h.fr>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from pathlib import Path

import polars as pl

from base_converter import BaseConverter

class Jsonl2Csv(BaseConverter):
    def __init__(self):
        self.fields_to_keep = ["id", "word", "pos"]

        super().__init__(
            file_glob="*.jsonl",
            output_suffix=".csv",
        )

    def converter(
            self,
            input_path: str | Path,
            output_path: str | Path,
            /,
            **kwargs,
    ) -> None:
        input_path, output_path = self.converter_input_validation(input_path, output_path)

        df = pl.read_ndjson(input_path)

        df = df.select(self.fields_to_keep)

        df.write_csv(output_path)


if __name__ == "__main__":
    j2c = Jsonl2Csv()

    j2c.folder_converter("../../output/mled_msa", "../../output/mled_msa_csv")
    j2c.folder_converter("../../output/mled_egy", "../../output/mled_egy_csv")
    j2c.folder_converter("../../output/bert_msa", "../../output/bert_msa_csv")
    j2c.folder_converter("../../output/bert_egy", "../../output/bert_egy_csv")
    j2c.folder_converter("../../output/bert_glf", "../../output/bert_glf_csv")
    j2c.folder_converter("../../output/bert_lev", "../../output/bert_lev_csv")

    j2c.folder_converter("../../output_karamed/mled_msa_karamed", "../../output_karamed/mled_msa_karamed_csv")
    j2c.folder_converter("../../output_karamed/mled_egy_karamed", "../../output_karamed/mled_egy_karamed_csv")
    j2c.folder_converter("../../output_karamed/bert_msa_karamed", "../../output_karamed/bert_msa_karamed_csv")
    j2c.folder_converter("../../output_karamed/bert_egy_karamed", "../../output_karamed/bert_egy_karamed_csv")
    j2c.folder_converter("../../output_karamed/bert_glf_karamed", "../../output_karamed/bert_glf_karamed_csv")
    j2c.folder_converter("../../output_karamed/bert_lev_karamed", "../../output_karamed/bert_lev_karamed_csv")
