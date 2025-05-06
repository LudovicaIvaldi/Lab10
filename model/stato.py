from dataclasses import dataclass


@dataclass
class Stato:
    StateAbb: str
    CCode: int
    StateNme: str

    def __hash__(self):
        return hash((self.StateAbb, self.CCode))

    def __eq__(self, other):
        return self.StateAbb==other.StateAbb and self.CCode==other.CCode

    def __str__(self):
        return self.StateNme