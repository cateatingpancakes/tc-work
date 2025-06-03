from typing import Any, TypeVar, get_origin, get_args
from collections.abc import Mapping, Iterable

DFA_TYPES = [("states", list[str]), ("accepting", list[str]), ("initial", str), ("symbols", list[str]), ("ruleset", dict[str, dict[str, str]])]
NFA_TYPES = [("states", list[str]), ("accepting", list[str]), ("initial", str), ("symbols", list[str]), ("ruleset", dict[str, dict[str, list[str]]])]
TM_TYPES = [("states", list[str]), ("accepting", list[str]), ("symbols", list[str]), ("blank", str), ("initial", str), ("increment", str), ("decrement", str), ("ruleset", list[dict[str, str]])]

# Asserts that an object is of type T
def assert_type(object: Any, T: TypeVar) -> None:
    origin, args = get_origin(T), get_args(T)

    # If the origin is None, the object has a real type
    # In this case we can check it against T directly
    if origin is None:
        if not isinstance(object, T):
            raise TypeError(f"Expected object to be {T} but got {type(object)}")
        
    # Otherwise, the object is a generic and we check
    # its components first
    else:
        # Check the origin (wrapping) type
        if not isinstance(object, origin):
            raise TypeError(f"Expected generic object to have origin {origin}")

        # Check the argument (wrapped) types, if any exist
        if args is not None:       
            # For list-like objects (iterables)
            if isinstance(object, Iterable): 
                V = args[0]
                for value in object:
                    assert_type(value, V)
    
            # For dictionary-like objects (mappings)
            elif isinstance(object, Mapping):
                K, V = args[0], args[1]
                for key, value in object.items():
                    assert_type(key, K), assert_type(value, V)

            else:
                # Arguments exist, but we can't typecheck properly
                # Valid automata pass the typecheck, so anything that gets here already implies an invalid automaton
                # JSON files also cannot contain anything that isn't already handled by the rest of the typechecker
                raise TypeError(f"Could not check unsupported type {type(object)}")


# Asserts types for the members of a dictionary
# match_list is a list in [(member, expected_type)] form
def assert_dictionary_types(data: dict, match_list: list) -> None:
    for key, type in match_list:
        assert_type(data[key], type)
