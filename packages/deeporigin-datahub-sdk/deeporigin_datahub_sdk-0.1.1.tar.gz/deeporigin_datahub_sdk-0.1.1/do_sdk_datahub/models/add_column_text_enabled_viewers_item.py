from enum import Enum


class AddColumnTextEnabledViewersItem(str, Enum):
    CODE = "code"
    HTML = "html"
    IMAGE = "image"
    MOLECULE = "molecule"
    NOTEBOOK = "notebook"
    SEQUENCE = "sequence"
    SMILES = "smiles"
    SPREADSHEET = "spreadsheet"

    def __str__(self) -> str:
        return str(self.value)
