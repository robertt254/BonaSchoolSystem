CBC_TERMLY_FEES = {
    "Play Group": 12000.00,
    "PP1": 15000.00,
    "PP2": 15000.00,
    "Grade 1": 18000.00,
    "Grade 2": 18000.00,
    "Grade 3": 18000.00,
    "Grade 4": 20000.00,
    "Grade 5": 20000.00,
    "Grade 6": 20000.00,
}

CBC_GRADES = [
    "Play Group", "PP1", "PP2",
    "Grade 1", "Grade 2", "Grade 3",
    "Grade 4", "Grade 5", "Grade 6",
]

TERM_ORDER = {"Term 1": 1, "Term 2": 2, "Term 3": 3}
TERM_BY_NUM = {1: "Term 1", 2: "Term 2", 3: "Term 3"}


# ── Academic calendar ─────────────────────────────────────────────────────────
# Standard Kenyan school-term pattern, used as the fallback when no term dates
# have been configured for a year. (month, day) tuples for (start, end).
DEFAULT_TERM_PATTERN = {
    "Term 1": ((1, 2),  (4, 11)),
    "Term 2": ((4, 28), (8, 8)),
    "Term 3": ((9, 1),  (11, 7)),
}


def default_term_dates(year: int):
    """Return {term: (start_date, end_date)} for a given year using the standard
    Kenyan calendar pattern."""
    from datetime import date
    return {
        term: (date(year, sm, sd), date(year, em, ed))
        for term, ((sm, sd), (em, ed)) in DEFAULT_TERM_PATTERN.items()
    }
