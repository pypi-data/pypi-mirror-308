import contextlib
import sys
from io import StringIO

import pytest
from pydantic_settings import BaseSettings

from monkay import Monkay, load, load_any


@pytest.fixture(autouse=True, scope="function")
def cleanup():
    for name in [
        "module_full_preloaded1_fn",
        "module_full_preloaded1",
        "module_preloaded1",
        "module_full",
        "fn_module",
    ]:
        sys.modules.pop(f"tests.targets.{name}", None)
    yield


def test_preloaded():
    assert "tests.targets.module_full" not in sys.modules
    import tests.targets.module_full as mod

    assert "tests.targets.fn_module" not in sys.modules

    assert "tests.targets.module_full" in sys.modules
    assert "tests.targets.module_full_preloaded1" in sys.modules
    assert "tests.targets.module_full_preloaded1_fn" in sys.modules
    assert "tests.targets.module_preloaded1" in sys.modules
    assert "tests.targets.extension" in sys.modules

    with contextlib.redirect_stdout(StringIO()):
        mod.bar  # noqa

    assert "tests.targets.fn_module" in sys.modules


def test_attrs():
    import tests.targets.module_full as mod

    assert isinstance(mod.monkay, Monkay)

    # in extras
    assert mod.foo() == "foo"
    assert mod.bar() == "bar"
    assert mod.bar2() == "bar2"
    with pytest.raises(KeyError):
        mod.monkay.add_lazy_import("bar", "tests.targets.fn_module:bar")
    with pytest.raises(KeyError):
        mod.monkay.add_deprecated_lazy_import(
            "bar",
            {
                "path": "tests.targets.fn_module:deprecated",
                "reason": "old",
                "new_attribute": "super_new",
            },
        )

    assert isinstance(mod.settings, BaseSettings)
    with pytest.warns(DeprecationWarning) as record:
        assert mod.deprecated() == "deprecated"
    assert record[0].message.args[0] == 'Attribute: "deprecated" is deprecated.\nReason: old.\nUse "super_new" instead.'


def test_load():
    assert load("tests.targets.fn_module.bar") is not None
    assert load("tests.targets.fn_module:bar") is not None
    with pytest.raises(ValueError):
        assert load("tests.targets.fn_module.bar", allow_splits=":") is not None
    with pytest.raises(AttributeError):
        assert load("tests.targets.fn_module:bar", allow_splits=".") is not None


def test_load_any():
    assert load_any("tests.targets.fn_module", ["not_existing", "bar"]) is not None
    with pytest.warns(DeprecationWarning) as records:
        assert (
            load_any(
                "tests.targets.fn_module",
                ["not_existing", "bar"],
                non_first_deprecated=True,
            )
            is not None
        )
    assert (
        load_any(
            "tests.targets.fn_module",
            ["bar", "not_existing"],
            non_first_deprecated=True,
        )
        is not None
    )
    assert str(records[0].message) == '"bar" is deprecated, use "not_existing" instead.'
    with pytest.raises(ImportError):
        assert load_any("tests.targets.fn_module", ["not-existing"]) is None
    with pytest.raises(ImportError):
        assert load_any("tests.targets.fn_module", []) is None
    with pytest.raises(ImportError):
        load_any("tests.targets.not_existing", ["bar"])


def test_extensions(capsys):
    import tests.targets.module_full as mod
    from tests.targets.extension import Extension, NonExtension

    captured = capsys.readouterr()
    assert captured.out == captured.err == ""

    app = mod.FakeApp()
    mod.monkay.set_instance(app)
    captured_out = capsys.readouterr().out
    assert captured_out == "settings_extension1 called\nsettings_extension2 called\n"
    with pytest.raises(ValueError):
        mod.monkay.add_extension(NonExtension(name="foo"))  # type: ignore
    with pytest.raises(KeyError):
        mod.monkay.add_extension(Extension(name="settings_extension1"))
    assert capsys.readouterr().out == ""

    # order

    class ExtensionA:
        name: str = "A"

        def apply(self, monkay: Monkay) -> None:
            monkay.ensure_extension("B")
            with pytest.raises(RuntimeError):
                monkay.ensure_extension("D")
            print("A")

    class ExtensionB:
        name: str = "B"

        def apply(self, monkay: Monkay) -> None:
            monkay.ensure_extension("A")
            monkay.ensure_extension(ExtensionC())
            print("B")

    class ExtensionC:
        name: str = "C"

        def apply(self, monkay: Monkay) -> None:
            monkay.ensure_extension(ExtensionA())
            print("C")

    with mod.monkay.with_extensions({"B": ExtensionB(), "A": ExtensionA()}):
        mod.monkay.apply_extensions()

    assert capsys.readouterr().out == "A\nC\nB\n"
    with mod.monkay.with_extensions(
        {
            "C": ExtensionC(),
            "B": ExtensionB(),
        }
    ):
        mod.monkay.apply_extensions()

    assert capsys.readouterr().out == "B\nA\nC\n"


def test_app(capsys):
    import tests.targets.module_full as mod

    app = mod.FakeApp()
    mod.monkay.set_instance(app)
    assert mod.monkay.instance is app
    captured_out = capsys.readouterr().out
    assert captured_out == "settings_extension1 called\nsettings_extension2 called\n"
    app2 = mod.FakeApp()
    with mod.monkay.with_instance(app2):
        assert mod.monkay.instance is app2
        assert capsys.readouterr().out == ""
    assert capsys.readouterr().out == ""


def test_caches():
    import tests.targets.module_full as mod

    assert not mod.monkay._cached_imports

    assert mod.bar() == "bar"
    assert "bar" in mod.monkay._cached_imports
    assert isinstance(mod.settings, BaseSettings)
    assert "settings" not in mod.monkay._cached_imports
    # settings cache
    assert "_settings" in mod.monkay.__dict__
    mod.monkay.clear_caches()

    assert not mod.monkay._cached_imports
    assert "_settings" not in mod.monkay.__dict__


def test_find_missing():
    import tests.targets.module_full as mod

    # __all__ is autogenerated
    assert not mod.monkay.find_missing(all_var=mod.__all__, search_pathes=["tests.targets.fn_module"])
    assert mod.monkay.find_missing(
        all_var=mod.__all__,
        search_pathes=["tests.targets.not_existing", "tests.targets.module_preloaded1"],
    ) == {
        "tests.targets.not_existing": {"search_path_import"},
        "tests.targets.module_preloaded1.not_included_export": {"search_path_extra"},
    }
    assert mod.monkay.find_missing(all_var={}, search_pathes=["tests.targets.module_full_preloaded1"]) == {
        "bar": {"all_var"},
        "bar2": {
            "all_var",
        },
        "dynamic": {"all_var"},
        "settings": {"all_var"},
        "deprecated": {"all_var"},
        "tests.targets.module_full_preloaded1": {
            "search_path_all_var",
        },
    }
