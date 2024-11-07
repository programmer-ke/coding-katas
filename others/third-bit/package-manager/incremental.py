import json
import itertools
import sys


def main():
    manifest = json.load(sys.stdin)
    packages = list(manifest.keys())
    if len(sys.argv) > 1:
        packages.reverse()

    accum = []
    count = find(manifest, packages, accum, [], 0)
    print(f"Count: {count}")
    for a in accum:
        print(a)


def find(manifest, remaining, accum, current, count):
    count += 1
    if not remaining:
        accum.append(current)
    else:
        first, rest = remaining[0], remaining[1:]
        for version in manifest[first]:
            candidate = current + [(first, version)]
            if compatible(manifest, candidate):
                count = find(manifest, rest, accum, candidate, count)
    return count


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


if __name__ == '__main__':
    main()
