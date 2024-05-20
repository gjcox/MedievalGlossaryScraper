from typing import List

class Meaning:
    substitution: str
    note: str

    def __init__(self, sub: str, note : str | None = None) -> None:
        self.substitution = sub.strip(" .")
        if note:
            self.note = note.strip(" .")

class GlossaryEntry:
    plaintext: str
    meanings: List[Meaning]
    synonymOf: str # I know that Python uses snakecase, but this is for use in JS

    def __init__(self, plaintext: str) -> None:
        self.plaintext = plaintext.strip().lower()
        self.meanings = []

    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.synonymOf: 
            return f"{self.plaintext} - synonym of {self.synonymOf}"
        elif self.meanings:
            return f"{self.plaintext} - {"; ".join(map(lambda m: m.substitution, self.meanings))}"
        else:
            return self.plaintext

    def add_meaning(self, meaning: Meaning) -> None:
        self.meanings.append(meaning)

    def set_synonym_of(self, synonym_of: str) -> None:
        self.synonymOf = synonym_of