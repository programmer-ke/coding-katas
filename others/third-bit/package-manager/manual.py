import json
import itertools
import sys


def main():
    manifest = json.load(sys.stdin)
    possible = make_possibilities(manifest)
    print(f"{len(possible)} possibilities")
    allowed = [p for p in possible if compatible(manifest, p)]
    print(f"{len(allowed)} allowed")
    for a in allowed:
        print(a)


def make_possibilities(manifest):
    available = []
    for package, versions in manifest.items():
        available.append([(package, v) for v in versions])

    accum = []
    _make_possible(available, [], accum)
    return accum


def _make_possible(remaining, current, accum):
    if not remaining:
        accum.append(current)
    else:
        head, tail = remaining[0], remaining[1:]
        for h in head:
            _make_possible(tail, current + [h], accum)


def compatible(manifest, combination):
    for package, version in combination:
        lookup = manifest[package][version]
        for package_i, version_i in combination:
            if package_i == package:
                continue
            if package_i not in lookup:
                continue
            if version_i not in lookup[package_i]:
                return False
    return True


if __name__ == "__main__":
    main()
