import re

def normalize(text: str) -> str:
    return re.sub(r"[^a-zA-Z\u0900-\u097F]", "", text).lower()
