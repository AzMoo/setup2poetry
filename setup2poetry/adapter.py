import pkg_resources

import toml


class PoetryAdapter:
    _deps = None

    def __init__(self, package):
        self._package = pkg_resources.require(package)[0]
        meta = dict(
            self._package._pkg_info.items()  # pylint: disable=protected-access
        )

        self._toml_dict = {
            'tool.poetry': {
                'name': meta['Name'],
                'version': meta['Version'],
                'description': meta['Summary'],
                'authors': [meta['Author']],
                'license': meta['License']
            },
            'tool.poetry.dependencies': {
                x: y for x, y in self._iter_deps(self._dependencies)
            },
            'tool.poetry.dev-dependencies': {
                x: y for x, y in self._iter_deps(self._get_extras())
            },
            'build-system': {
                'requires': ["poetry>=0.12"],
                'build-backend': "poetry.masonry.api"
            }
        }

    def _iter_deps(self, deps):
        for dep in deps:
            try:
                yield (dep.name, "={}".format(dep.specs[0][1]))
            except IndexError:
                yield (dep.name, "*")

    def _get_extras(self):
        extra_deps = self._package.requires(self._package.extras)
        return [i for i in extra_deps if i not in self._dependencies]

    @property
    def _dependencies(self):
        if self._deps is not None:
            return self._deps

        return self._package.requires()

    def writepath(self, filepath):
        with open(filepath, "w") as f:
            self.write(f)

    def write(self, f):
        toml.dump(self._toml_dict, f)

    def print(self):
        print(toml.dumps(self._toml_dict))
