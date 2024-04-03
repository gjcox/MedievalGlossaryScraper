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

    def __init__(self, plaintext: str) -> None:
        self.plaintext = plaintext.strip().lower()
        self.meanings = []

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.plaintext} - {"; ".join(map(lambda m: m.substitution, self.meanings))}"

    def add_meaning(self, meaning: Meaning) -> None:
        self.meanings.append(meaning)