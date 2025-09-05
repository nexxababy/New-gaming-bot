import time

def now_ts():
    return time.time()

def pretty_name(m):
    user = m.from_user
    if not user:
        return "Unknown"
    return f"@{user.username}" if user.username else user.first_name
