def qualify(*, table: str, schema: str | None = None, column: str | None = None):
    res = table
    if schema is not None:
        res = schema + '.' + res
    if column is not None:
        res += '.' + column
    return res


def unqualify(n: str) -> list[str]:
    return n.split('.')


