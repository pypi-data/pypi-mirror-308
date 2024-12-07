import inspect
import pytest

__all__ = ['class_fixture']

def class_fixture (*args, **kwargs):
    caller_locals = inspect.stack()[1].frame.f_locals

    def class_fixturer (cls):
        @pytest.fixture(**kwargs)
        def construct():
            return cls()

        cls._pytestfixturefunction = construct._pytestfixturefunction

        # Support BDD: a method decorated with `@given`, `@when` or
        # `@then` works pretty much like an ordinary function
        # decorated in the same way, provided we twist the arm of the
        # fixtures framework into injecting `constructor()` as the
        # first (i.e. `self`) parameter. As it turns out, all it takes
        # is to rewrite the name of the first parameter in the
        # signature.
        fixture_name = kwargs.get('name', cls.__name__)
        for (step_method_name, step_method) in inspect.getmembers(cls):
            if hasattr(step_method, '_pytest_bdd_step_context'):
                bdd_context = step_method._pytest_bdd_step_context
                bdd_context.step_func = _step_func_of_method(
                    bdd_context.step_func,
                    name_for_self=fixture_name)

                # Trick the fixtures manager into picking up the
                # doctored step method, by stuffing it into the
                # caller_locals. Maybe there is a better way?
                caller_locals[f"🎁{step_method_name}"] = step_method

        return cls

    if args and inspect.isclass(args[0]):
        return class_fixturer(args[0])
    else:
        return class_fixturer

def _step_func_of_method (method, name_for_self):
    """Returns: `method`, except that the first parameter
       (typically `self`) is renamed to `name_for_self`."""

    orig_signature = inspect.signature(method)
    rewritten_signature = orig_signature.replace(
        parameters = [
            p if n > 0
            else inspect.Parameter(
                    name_for_self, p.kind, default=p.default)
            for n, p in enumerate(orig_signature.parameters.values())])

    def wrapped_method (*args, **kwargs):
        if name_for_self in kwargs:
            args = (kwargs.pop(name_for_self), *args)

        return method(*args, **kwargs)

    wrapped_method.__signature__ = rewritten_signature

    return wrapped_method
