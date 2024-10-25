import json
import sys


class BuildBase:
    def build(self, config_file):
        config = self._configure(config_file)
        ordered = self._topo_sort(config)
        for node in ordered:
            self._refresh(config, node)

    def _refresh(self, config, node):
        assert node in config
        print(config[node]['rule'])

    def _configure(self, config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        known = set(config.keys())
        return {
            n: self._check(n, d, known)
            for n, d in config.items()
        }

    def _check(self, name, details, known):
        assert all(['rule' in details, 'depends' in details])
        depends = set(details['depends'])
        assert depends.issubset(known)
        return {
            'rule': details['rule'],
            'depends': depends
        }
    
    def _topo_sort(self, config):
        graph = {n: config[n]['depends'] for n in config}
        results = []
        while graph:
            available = {n for n in graph if not graph[n]}
            assert available, f"Circular graph {graph}"
            results.extend(available)
            graph = {
                n: graph[n] - available
                for n in graph
                if n not in available
            }
        return results


if __name__ == '__main__':
    config = sys.argv[1]
    b = BuildBase()
    b.build(config)
