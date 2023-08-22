"Plugin management."

import importlib
import importlib.metadata
import itertools
import pkgutil
import types
import typing as t

P_co = t.TypeVar("P_co", covariant=True)  #: Protocol implementation

MF: t.TypeAlias = types.FunctionType | types.ModuleType  #: Module or function

PluginMap: t.TypeAlias = dict[str, P_co | None]  #: Map of plugins to implementations


class Adapter(t.Protocol, t.Generic[P_co]):
    """
    Functions satisfying this protocol adapt or cast a module or function to a protocol.

    The argument to the adapter MUST be named ``plugin``, else MyPy will warn you:

    > Incompatible types in assignment
    """

    def __call__(self, plugin: types.ModuleType | types.FunctionType) -> P_co | None:
        "Adapt or cast a module or function to a protocol."
        ...


def find_plugins(
    namespace: str,
    group: str,
    adapter: Adapter[P_co],
) -> PluginMap[P_co]:
    """
    Find plugins by their package namespace or entry point.

    The values in the returned dict MAY be None, indicating a plugin which is in the namespace
    or which has declared the entry point, but which doesn't satisfy the adapter.
    """
    return {
        n: adapter(m)
        for n, m in itertools.chain(_find_entry_points(group), _find_modules(namespace))
    }


def _find_entry_points(group: str) -> t.Iterable[tuple[str, MF]]:
    for ep in importlib.metadata.entry_points(group=group):
        yield ep.name, ep.load()


def _find_modules(namespace: str) -> t.Iterable[tuple[str, MF]]:
    ns = importlib.import_module(namespace)
    for _, name, _ in pkgutil.iter_modules(ns.__path__, ns.__name__ + "."):
        yield name, importlib.import_module(name)
