from main_utils import normalize

def valid_start(prev_word: str, next_word: str) -> bool:
    prev = normalize(prev_word)
    nxt = normalize(next_word)
    if not prev or not nxt:
        return False
    return nxt[0] == prev[-1]
