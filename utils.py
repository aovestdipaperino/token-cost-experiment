def slugify(text):
    out = text.strip().lower()
    for ch in " _":
        out = out.replace(ch, "-")
    while "--" in out:
        out = out.replace("--", "-")
    return out


def chunk(items, size):
    return [items[i:i + size] for i in range(0, len(items), size)]


def moving_average(values, window):
    if window <= 0:
        raise ValueError("window must be positive")
    result = []
    for i in range(len(values) - window + 1):
        result.append(sum(values[i:i + window]) / window)
    return result


def retry(fn, attempts):
    last = None
    for _ in range(attempts):
        try:
            return fn()
        except Exception as exc:
            last = exc
    raise last
