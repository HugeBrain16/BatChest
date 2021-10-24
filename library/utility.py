"""utility library for the bot"""

def mention_to_id(mention: str) -> int:
    """extract user id from discord mention"""
    result = 0

    try:
        result = int(
            mention.replace("<", "").replace(">", "").replace("!", "").replace("@", "")
        )
    except (AttributeError, ValueError):
        pass

    return result
