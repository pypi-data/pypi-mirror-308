# SPDX-FileCopyrightText: 2024-present Marceau <git@marceau-h.fr>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
import json
from enum import StrEnum
from pathlib import Path
from typing import Optional

import polars as pl
from tqdm.auto import tqdm
from camel_tools.disambig.bert.unfactored import BERTUnfactoredDisambiguator
from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tokenizers.word import simple_word_tokenize
# from camel_tools.tagger.default import DefaultTagger

class Disambiguator(StrEnum):
    MLED_MSA = "mled_msa"
    MLED_EGY = "mled_egy"
    BERT_MSA = "bert_msa"
    BERT_EGY = "bert_egy"
    BERT_GLF = "bert_glf"
    BERT_LEV = "bert_lev"


def mled_init(disambiguator: Optional[Disambiguator] = None):
    """apply camel-tools POS tagging according to tags listed in tags_list.json"""

    if disambiguator is None:
        disambiguator = Disambiguator.MLED_MSA

    disambiguators = {
        "mled_msa": [MLEDisambiguator.pretrained, {"model_name": "calima-msa-r13"}],
        "mled_egy": [MLEDisambiguator.pretrained, {"model_name": "calima-egy-r13"}],

        "bert_msa": [BERTUnfactoredDisambiguator.pretrained, {"model_name": "msa"}],
        "bert_egy": [BERTUnfactoredDisambiguator.pretrained, {"model_name": "egy"}],
        "bert_glf": [BERTUnfactoredDisambiguator.pretrained, {"model_name": "glf"}],
        "bert_lev": [BERTUnfactoredDisambiguator.pretrained, {"model_name": "lev"}],
    }

    try:
        mled = disambiguators[disambiguator]
        mled = mled[0](**mled[1])
    except KeyError:
        raise ValueError(f"disambiguator must be one of {list(disambiguators.keys())}")

    return mled


def tagger(
        input_path: str | Path,
        output_path: str | Path,
        mled: MLEDisambiguator,
        tags_list: list[str],
        debug=False
) -> None:
    if isinstance(input_path, str):
        input_path = Path(input_path)
    elif isinstance(input_path, Path):
        pass
    else:
        raise ValueError(f"input_path must be a string or a Path object, not {type(input_path)}")

    if isinstance(output_path, str):
        output_path = Path(output_path)
    elif isinstance(output_path, Path):
        pass
    else:
        raise ValueError(f"output_path must be a string or a Path object, not {type(output_path)}")

    assert input_path.exists(), f"Input file {input_path} does not exist"

    if output_path.exists() and output_path.is_dir():
        output_path = output_path / input_path.with_suffix(".jsonl").name

    assert output_path.parent.exists(), f"Output folder {output_path.parent} does not exist"

    with input_path.open('r', encoding='utf-8') as f:
        file = f.read()

    if debug:
        len_file = len(file)
        len_file_words = len(file.split())

    tokens = simple_word_tokenize(file)  # split_digits

    if debug:
        len_tokens = len(tokens)

    if isinstance(mled, BERTUnfactoredDisambiguator):
        batch_size = 10_000
        tokens_batches = [tokens[i:i + batch_size] for i in range(0, len(tokens), batch_size)]
        disambig = []
        for tokens_batch in tokens_batches:
            disambig.extend(mled.disambiguate(tokens_batch))


    else:
        disambig = mled.disambiguate(tokens)

    liste = [
        {
            "id": i,
            "word": tok,
            **{
                k: d.analyses[0].analysis[k]
                for k in tags_list
                if d.analyses
                and k in d.analyses[0].analysis
            }
        }
        for i, (tok, d) in enumerate(zip(tokens, disambig))
    ]

    if debug:
        len_liste = len(liste)

    liste = [
        {
            k: v
            if v not in {"", "na"}
            else v
            if k!="vox" and v!="u"
            else None
            for k, v in d.items()
        }
        for d in liste
    ]

    if debug:
        len_liste_na = len(liste)

    df = pl.DataFrame(liste)

    if debug:
        len_df = len(df)

        print(
            f"File: {input_path}\n"
            f"File length: {len_file}\n"
            f"File words: {len_file_words}\n"
            f"Tokens: {len_tokens}\n"
            f"Liste: {len_liste}\n"
            f"Liste na: {len_liste_na}\n"
            f"DataFrame: {len_df}\n"
        )

    df.write_ndjson(output_path)
    df.write_json(output_path.with_suffix(".json"))


def folder_tagger(
        input_folder: str | Path,
        output_folder: str | Path,
        mled: MLEDisambiguator,
        tags_list: list[str]
) -> None:
    if isinstance(input_folder, str):
        input_folder = Path(input_folder)
    elif isinstance(input_folder, Path):
        pass
    else:
        raise ValueError(f"input_folder must be a string or a Path object, not {type(input_folder)}")

    if isinstance(output_folder, str):
        output_folder = Path(output_folder)
    elif isinstance(output_folder, Path):
        pass
    else:
        raise ValueError(f"output_folder must be a string or a Path object, not {type(output_folder)}")

    assert input_folder.exists(), f"Input folder {input_folder} does not exist"

    output_folder.mkdir(parents=True, exist_ok=True)

    pbar = tqdm(sorted(input_folder.glob("*.txt"), key=lambda x: int(x.stem.strip().split()[-1])))
    for path in pbar:
        new_path = output_folder
        pbar.set_description(f"Processing {path}")

        tagger(path, new_path, mled, tags_list)


def main(
        input_folder: str | Path,
        output_folder: str | Path,
        disambiguator: Optional[Disambiguator] = None
):
    mled = mled_init(disambiguator)

    with open("../tags_list.json", "r") as f:
        tags_list = json.load(f)

    folder_tagger(input_folder, output_folder, mled, tags_list)


if __name__ == "__main__":
    for disamb in Disambiguator:
        print(disamb)
        main("../txts", "../output/" + disamb, disamb)

