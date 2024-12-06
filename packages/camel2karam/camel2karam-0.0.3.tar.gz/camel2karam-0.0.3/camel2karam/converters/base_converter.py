# SPDX-FileCopyrightText: 2024-present Marceau <git@marceau-h.fr>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple

from tqdm import tqdm


@dataclass
class PartsMapping:
    FORM: int = -1
    LEMMA: int = -1
    UPOS: int = -1
    XPOS: int = -1
    FEATS: int = -1
    HEAD: int = -1
    DEPREL: int = -1
    DEPS: int = -1
    MISC: int = -1


class BaseConverter(ABC):
    @abstractmethod
    def __init__(self, /, file_glob: str = "*.jsonl", output_suffix: str = ".xml") -> None:
        self.file_glob = file_glob
        self.output_suffix = output_suffix

    @staticmethod
    def replace_rafter(text: str) -> str:
        return text.replace("=\">", "=\"&gt;").replace("=\"<", "=\"&lt;")

    @staticmethod
    def toks_to_sents(*cols: Iterable[str]) -> List[List[Tuple[str, ...]]]:
        sents = []
        sent = []
        prev = None
        for i, row in enumerate(zip(*cols)):
            tok = row[0].strip()
            if len(sent) > 1 and tok not in "!؟.!?" and prev in "!؟.!?":
                sents.append(sent)
                sent = []
            sent.append(tuple(map(str.strip, row)))
            prev = tok

            # sent.append(tuple(map(str.strip, row)))
            # if tok in "!؟.!?" and sent and (len(sent) < 2 or sent[-2] not in "!؟.!?"):
            #     sents.append(sent)
            #     sent = []

        if sent:
            sents.append(sent)

        return sents

    @staticmethod
    def write_connlu(
            output_path: str | Path,
            sents: List[List[Tuple[str, ...]]],
            parts_mapping: PartsMapping,
    ) -> None:
        pm_values = list(parts_mapping.__dict__.values())
        with output_path.open("w", encoding="utf-8") as f:
            f.write("# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC\n\n")
            for i, sent in enumerate(sents, 1):
                f.write(f"""# sent_id = {i}\n# text = {' '.join(w[parts_mapping.FORM] for w in sent)}\n""")
                for j, parts in enumerate(sent, 1):
                    to_fill = [j] + [parts[i] if i != -1 else "_" for i in pm_values]
                    f.write("\t".join(map(str, to_fill)) + "\n")
                f.write("\n")

    def converter_input_validation(
            self,
            input_path: str | Path,
            output_path: str | Path,
    ) -> tuple[Path, Path]:
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
            output_path = output_path / input_path.with_suffix(self.output_suffix).name

        assert output_path.parent.exists(), f"Output folder {output_path.parent} does not exist"

        return input_path, output_path

    @abstractmethod
    def converter(
            self,
            input_path: str | Path,
            output_path: str | Path,
            /,
            **kwargs,
    ) -> None:
        raise NotImplementedError

    def folder_converter(
            self,
            input_folder: str | Path,
            output_folder: str | Path,
            **kwargs,
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

        if not output_folder.exists():
            output_folder.mkdir(parents=True)

        pbar = tqdm(list(input_folder.glob(self.file_glob)))
        pbar.set_description(f"Converting {input_folder} to {output_folder}")
        for input_path in pbar:
            output_path = output_folder / input_path.with_suffix(self.output_suffix).name
            pbar.set_postfix(
                input_path_name=input_path.name,
                # output_path_name=output_path.name,
            )
            self.converter(input_path, output_path, **kwargs)
