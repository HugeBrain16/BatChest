def mention_to_id(mention: str):
    result = 0

    try:
        result = int(
            mention.replace("<", "").replace(">", "").replace("!", "").replace("@", "")
        )
    except Exception:
        result = 0

    return result
