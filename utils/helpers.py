def pretty_name(m):
    return m.from_user.first_name if m.from_user else "Unknown"
