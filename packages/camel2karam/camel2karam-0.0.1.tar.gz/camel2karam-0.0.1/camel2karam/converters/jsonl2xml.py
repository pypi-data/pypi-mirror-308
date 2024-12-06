# SPDX-FileCopyrightText: 2024-present Marceau <git@marceau-h.fr>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

import polars as pl

from base_converter import BaseConverter

class Jsonl2Xml(BaseConverter):
    @staticmethod
    def better_quoteattr(s):
        if isinstance(s, int):
            return f'"{s}"'
        if s is None:
            return f'"{None}"'
        return quoteattr(s)

    def __init__(self):
        super().__init__(
            file_glob="*.jsonl",
            output_suffix=".xml",
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

        with output_path.open('w', encoding='utf-8') as f:
            f.write("""<?xml version="1.0" encoding="utf-8"?>\n<root>""")

            for i, row in enumerate(df.iter_rows(named=True)):
                f.write("<w ")
                f.write(" ".join(
                    f'{k}={self.better_quoteattr(v)}'
                    # if v is not None else f'{k}="{None}"'
                    for k, v in row.items()
                    if k != "word"
                ))
                f.write(f"> {escape(self.replace_rafter(row['word']))} </w>\n")

            f.write("</root>")



if __name__ == "__main__":
    j2x = Jsonl2Xml()

    j2x.folder_converter("../../output/mled_msa", "../../output/mled_msa_xml")
    j2x.folder_converter("../../output/mled_egy", "../../output/mled_egy_xml")
    j2x.folder_converter("../../output/bert_msa", "../../output/bert_msa_xml")
    j2x.folder_converter("../../output/bert_egy", "../../output/bert_egy_xml")
    j2x.folder_converter("../../output/bert_glf", "../../output/bert_glf_xml")
    j2x.folder_converter("../../output/bert_lev", "../../output/bert_lev_xml")

    j2x.folder_converter("../../output_karamed/mled_msa_karamed", "../../output_karamed/mled_msa_karamed_xml")
    j2x.folder_converter("../../output_karamed/mled_egy_karamed", "../../output_karamed/mled_egy_karamed_xml")
    j2x.folder_converter("../../output_karamed/bert_msa_karamed", "../../output_karamed/bert_msa_karamed_xml")
    j2x.folder_converter("../../output_karamed/bert_egy_karamed", "../../output_karamed/bert_egy_karamed_xml")
    j2x.folder_converter("../../output_karamed/bert_glf_karamed", "../../output_karamed/bert_glf_karamed_xml")
    j2x.folder_converter("../../output_karamed/bert_lev_karamed", "../../output_karamed/bert_lev_karamed_xml")

