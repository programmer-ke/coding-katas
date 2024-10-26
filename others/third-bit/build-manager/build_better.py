
class Builder:
    def build(self, config_file):
        config = self._configure(config_file)
        ordered = self._topo_sort(config)
        actions = []
        for node in ordered:
            self._refresh(config, node, actions)
        return actions

    def _refresh(self, config, node, actions):
        self._must(node in config, "Unknown node")
        actions.append(config[node]['rule'])
    
    def _must(self, condition, message):
        if not condition:
            raise ValueError("Message")

    def _configure(self, config):
        known = set(config.keys())
        return {
            n: self._check(n, d, known)
            for n, d in config.items()
        }

    def _check(self, name, details, known):
        self._check_keys(name, details)
        depends = set(details['depends'])
        self._must(depends.issubset(known), "Unknown dependencies")
        result = details.copy()
        result['depends'] = depends
        return result

    def _check_keys(self, name, details):
        self._must("rule" in details, f"Missing rule for {name}")
        self._must(
            "depends" in details, f"Missing depends for {name}"
        )        

    def _topo_sort(self, config):
        graph = {n: config[n]['depends'] for n in config}
        results = []
        while graph:
            available = {n for n in graph if not graph[n]}
            self._must(available, f"Circular graph {graph}")
            results.extend(sorted(available))
            graph = {
                n: graph[n] - available
                for n in graph
                if n not in available
            }
        return results


class BuildTime(Builder):
    def _check_keys(self, name, details):
        super()._check_keys(name, details)
        self._must("time" in details, f"No time for {name}")

    def _refresh(self, config, node, actions):
        assert node in config, f"Unknown node {node}"
        if self._needs_update(config, node):
            actions.append(config[node]["rule"])

    def _needs_update(self, config, node):
        return any(
            config[node]["time"] < config[d]["time"]
            for d in config[node]["depends"]
        )



def test_circular():
    action_A = "build A"
    action_B = "build B"
    config = {
        "A": {"depends": ["B"], "rule": action_A},
        "B": {"depends": ["A"], "rule": action_B},
    }
    try:
        Builder().build(config)
        assert False, "should have had exception"
    except ValueError:
        pass


def test_no_dep():
    action_A = "build A"
    action_B = "build B"
    config = {
        "A": {"depends": [], "rule": action_A},
        "B": {"depends": [], "rule": action_B},
    }
    assert Builder().build(config) == [action_A, action_B]


def test_diamond_dep():
    action_A = "build A"
    action_B = "build B"
    action_C = "build C"
    action_D = "build D"
    config = {
        "A": {"depends": ["B", "C"], "rule": action_A, "time": 0},
        "B": {"depends": ["D"], "rule": action_B, "time": 0},
        "C": {"depends": ["D"], "rule": action_C, "time": 1},
        "D": {"depends": [], "rule": action_D, "time": 1},
    }
    assert BuildTime().build(config) == [action_B, action_A]
