# Camel 2 KARAM
[![PyPI - Version](https://img.shields.io/pypi/v/camel2karam.svg)](https://pypi.org/project/camel2karam)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/camel2karam.svg)](https://pypi.org/project/camel2karam)

Camel 2 KARAM

---

**Table des matières**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation
### PyPi
Camel 2 KARAM est disponible sur PyPi, vous pouvez l'installer avec pip à l'aide de la commande suivante:
```bash
pip install camel2karam
```
Vous pouvez ensuite vérifier que l'installation s'est bien passée en lançant la commande `camel2karam --version`

### Développement
Pour installer Europarser en mode développement, vous pouvez cloner le dépôt git et installer les dépendances avec pip:
```bash
git clone https://github.com/CERES-Sorbonne/C2K.git
cd C2K
pip install -e .
```

## Usages
#### Usage basique
```python
from pathlib import Path

from camel2karam.converters import PartsMapping, Csv2Connlu, CsvSent2CsvTok, CsvSent2OneLetterTag, CsvTok2CsvSent, Jsonl2Connlu, Jsonl2Csv, Jsonl2WebAnno, Jsonl2Xml, TagsetConvert # Liste de tous les convertisseurs disponibles (et PartsMapping)

input_folder = Path('/path/to/your/input')
output_folder = Path('/path/to/your/output')

converter = Jsonl2Connlu() # Changer le convertisseur ici
converter.folder_converter(input_folder, output_folder)
```

Certains convertisseurs nécessitent des paramètres supplémentaires, vous pouvez les passer en argument du constructeur du convertisseur.
Par exemple, les convertisseurs prenant des fichiers CSVs en entrée vous demanderont le mapping des colonnes : 
```python
from camel2karam.converters import Csv2Connlu
c2c = Csv2Connlu()

c2c.folder_converter(
    "path/to/your/input",
    "path/to/your/output",
    word_col="word",
    pos_col="pos",
    pos2_col=None
)
```


## License

`camel2karam` est distribué sous les termes de la licence [AGPLv3](https://www.gnu.org/licenses/agpl-3.0.html).
