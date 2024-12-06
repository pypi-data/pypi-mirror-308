# SPDX-FileCopyrightText: 2024-present Marceau <git@marceau-h.fr>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from pathlib import Path

import polars as pl

from base_converter import BaseConverter


class TagsetConvert(BaseConverter):
    TAGSET = {
        "PART_DET": "PART",
        "CONJ": "PART",
        "PREP": "PART",
        "PART_NEG": "PART",
        "PART_FUT": "PART",
        "PART_PROG": "PART",
        "CONJ_SUB": "PART",
        "PRON_DEM": "NOUN",
        "PRON_INTERROG": "NOUN",
        "PART": "PART",
        "PART_CONNECT": "PART",
        "PART_EMPHATIC": "PART",
        "PART_RC": "PART",
        "PART_VOC": "PART",
        "PRON": "NOUN",
        "NOUN": "NOUN",
        "NOUN_NUM": "NOUN",
        "NOUN_PROP": "NOUN",
        "NOUN_QUANT": "NOUN",
        "ADJ": "NOUN",
        "ADJ_NUM": "NOUN",
        "ADJ_COMP": "NOUN",
        "ADV": "NOUN",
        "ADV_REL": "NOUN",
        "VERB": "VERB",
        "VERB_PSEUDO": "VERB",
        "VERB_NOUN": "NOUN",
        "PRON_EXCLAM": "NOUN",
        "PRON_REL": "NOUN",
        "PART_VERB": "PART",
        "PART_INTERROG": "PART",
        "PART_RESTRICT": "PART",
        "PART_FOCUS": "PART",
        "DIGIT": "DIGIT",
        "ABBREV": "PART",
        "INTERJ": "PART",
        "FOREIGN": "NOUN",
        "PUNC": "PUNC"
    }

    @classmethod
    def replace(cls, tag):
        return cls.TAGSET.get(tag.upper(), cls.TAGSET.get(tag, tag.upper()))

    def __init__(self):
        super().__init__(
            file_glob="*.jsonl",
            output_suffix=".jsonl",
        )

    def converter(
            self,
            input_path: str | Path,
            output_path: str | Path,
            /,
            **kwargs,
    ) -> None:
        input_path, output_path = self.converter_input_validation(input_path, output_path)

        (
            pl
            .read_ndjson(input_path)
            .with_columns(
                [pl.col("pos").map_elements(TagsetConvert.replace, return_dtype=pl.Utf8)]
            )
            .write_ndjson(output_path)
        )


if __name__ == "__main__":
    tc = TagsetConvert()

    tc.folder_converter("../../output/mled_msa", "../../output_karamed/mled_msa_karamed")
    tc.folder_converter("../../output/mled_egy", "../../output_karamed/mled_egy_karamed")
    tc.folder_converter("../../output/bert_msa", "../../output_karamed/bert_msa_karamed")
    tc.folder_converter("../../output/bert_egy", "../../output_karamed/bert_egy_karamed")
    tc.folder_converter("../../output/bert_glf", "../../output_karamed/bert_glf_karamed")
    tc.folder_converter("../../output/bert_lev", "../../output_karamed/bert_lev_karamed")
