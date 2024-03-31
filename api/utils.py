def has_duplicate_dicts(lst):
    seen = set()
    for d in lst:
        if tuple(d.items()) in seen:
            return True
        seen.add(tuple(d.items()))
    return False
