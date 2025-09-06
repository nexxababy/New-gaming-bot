def pretty_name(user):
    """Convert user object or string into a pretty display name"""
    if isinstance(user, str):
        return user.title()
    elif hasattr(user, "first_name"):
        return f"{user.first_name} {user.last_name or ''}".strip()
    elif hasattr(user, "username"):
        return f"@{user.username}"
    return str(user)
