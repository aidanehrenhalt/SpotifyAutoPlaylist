from __future__ import annotations

from dataclasses import dataclass


GENRE_ALIASES: dict[str, set[str]] = {
    "shoegaze": {"dream pop", "noise pop", "ethereal"},
    "deep house": {"house", "electronic", "late night"},
    "jazz": {"modal jazz", "hard bop", "cool jazz"},
}


@dataclass(slots=True)
class GenreProfile:
    target_genre: str
    related_genres: list[str]
    lexical_aliases: list[str]

    @property
    def search_terms(self) -> list[str]:
        seen: dict[str, None] = {}
        for value in [self.target_genre, *self.related_genres, *self.lexical_aliases]:
            seen.setdefault(value, None)
        return list(seen.keys())


def build_genre_profile(genre: str) -> GenreProfile:
    normalized = genre.strip().lower()
    aliases = sorted(GENRE_ALIASES.get(normalized, set()))
    return GenreProfile(
        target_genre=normalized,
        related_genres=aliases,
        lexical_aliases=[normalized.replace("-", " ")],
    )
