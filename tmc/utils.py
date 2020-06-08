import importlib
import sys


def load_module(pkg, lang='en'):
    module_not_found = 'File {0} does not exist!'.format(pkg)
    other_exception = 'Running exercise {0} failed. Please make sure that you can run your code.'.format(pkg)
    if lang == 'fi':
        module_not_found = 'Tiedostoa {0} ei löytynyt.'.format(pkg)
        other_exception = 'Tehtävän {0} suorittaminen epäonnistui. \
            Varmista, että saat ohjelman suoritettua loppuun.'.format(pkg)
    try:
        return importlib.import_module(pkg)
    except ModuleNotFoundError:
        return AssertionError(module_not_found)
    except Exception:
        return AssertionError(other_exception)


def reload_module(module):
    if isinstance(module, AssertionError):
        raise module
    importlib.reload(module)


def load(pkg, method, lang='en', err=None):
    module_not_found = 'Function {1} was not found in file {0}.'.format(pkg, method)
    if lang == 'fi':
        module_not_found = 'Tiedostosta {0} ei löytynyt funktiota {1}.'.format(pkg, method)

    if not err:
        err = module_not_found

    def fail(*args, **kwargs):
        raise AssertionError(err)

    try:
        return getattr(importlib.import_module(pkg), method)
    except Exception:
        return fail


def get_stdout():
    return sys.stdout.getvalue().strip()


def get_stderr():
    return sys.stderr.getvalue().strip()


def any_contains(needle, haystacks):
    any(map(lambda haystack: needle in haystack, haystacks))
