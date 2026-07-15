RANKS = [
    ("F",   10,  5,   "blue"),
    ("E",   20,  10,  "blue"),
    ("D",   30,  15,  "blue"),
    ("C",   40,  20,  "blue"),
    ("B",   50,  25,  "green"),
    ("A",   60,  30,  "green"),
    ("A+",  70,  40,  "green"),
    ("AA",  80,  50,  "red"),
    ("S",   90,  60,  "red"),
    ("SS",  100, 70,  "red"),
    ("SSS", 110, 80,  "red"),
    ("LEGEND", 999, 100, "gold")
]

def get_rank(score):
    if score >= 300:
        return RANKS[-1]
    idx = min(score // 25, len(RANKS) - 2)
    return RANKS[idx]
