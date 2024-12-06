# SPDX-FileCopyrightText: 2024-present Marceau <git@marceau-h.fr>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from pathlib import Path

import polars as pl

from base_converter import BaseConverter, PartsMapping

class Jsonl2Connlu(BaseConverter):
    parts_mapping = PartsMapping(
        FORM=0,
        LEMMA=2,
        UPOS=1,
        XPOS=3,
    )
    def __init__(self):
        super().__init__(
            file_glob="*.jsonl",
            output_suffix=".conllu",
        )

    def from_line_to_xpos(self, serie):
        if not any(serie[k] for k in ["asp", "per", "gen", "num", "stt", "cas", "vox", "mod"]):
            pass
            return serie['pos'].upper()
        pos, asp, per, gen, num, stt, cas, vox, mod = [e if e != "_" else '' for e in serie.values()]
        return f"{pos}.{asp}{per}{gen}{num}.{stt}{cas}{vox}{mod}".upper().strip(".")

    def converter(
            self,
            input_path: str | Path,
            output_path: str | Path,
            /,
            **kwargs,
    ) -> None:
        input_path, output_path = self.converter_input_validation(input_path, output_path)

        df = pl.read_ndjson(input_path).fill_nan("_").fill_null("_")

        df = df.with_columns(
            pl.col("vox").str.replace("u", "_", literal=True)
        )

        df = df.with_columns(
                 pl.struct(
                        [
                            "pos",
                            "asp",
                            "per",
                            "gen",
                            "num",
                            "stt",
                            "cas",
                            "vox",
                            "mod",
                        ]
                    ).map_elements(
                self.from_line_to_xpos,
                return_dtype=pl.Utf8,
            ).alias("xpos")
        )

        if "atbtok" not in df.columns:
            df = df.with_columns(pl.lit("_").alias("atbtok"))

        sents = self.toks_to_sents(df['word'], df['pos'], df['atbtok'], df['xpos'])

        self.write_connlu(output_path, sents, self.parts_mapping)


if __name__ == "__main__":
    j2c = Jsonl2Connlu()

    j2c.folder_converter("../../output/mled_msa", "../../output/mled_msa_conllu")
    j2c.folder_converter("../../output/mled_egy", "../../output/mled_egy_conllu")
    j2c.folder_converter("../../output/bert_msa", "../../output/bert_msa_conllu")
    j2c.folder_converter("../../output/bert_egy", "../../output/bert_egy_conllu")
    j2c.folder_converter("../../output/bert_glf", "../../output/bert_glf_conllu")
    j2c.folder_converter("../../output/bert_lev", "../../output/bert_lev_conllu")

    j2c.folder_converter("../../output_karamed/mled_msa_karamed", "../../output_karamed/mled_msa_karamed_conllu")
    j2c.folder_converter("../../output_karamed/mled_egy_karamed", "../../output_karamed/mled_egy_karamed_conllu")
    j2c.folder_converter("../../output_karamed/bert_msa_karamed", "../../output_karamed/bert_msa_karamed_conllu")
    j2c.folder_converter("../../output_karamed/bert_egy_karamed", "../../output_karamed/bert_egy_karamed_conllu")
    j2c.folder_converter("../../output_karamed/bert_glf_karamed", "../../output_karamed/bert_glf_karamed_conllu")
    j2c.folder_converter("../../output_karamed/bert_lev_karamed", "../../output_karamed/bert_lev_karamed_conllu")
