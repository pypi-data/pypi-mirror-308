from enum import Enum


class SeqDataType(str, Enum):
    AA = "aa"
    DNA = "dna"
    RNA = "rna"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
