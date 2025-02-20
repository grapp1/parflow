# -----------------------------------------------------------------------------
# Map function Helper functions
# -----------------------------------------------------------------------------


def map_to_parent(pfdb_obj):
    """Helper function to extract the parent of a pfdb_obj"""
    return pfdb_obj._parent_

# -----------------------------------------------------------------------------


def map_to_self(pfdb_obj):
    """Helper function to extract self of self (noop)"""
    return pfdb_obj

# -----------------------------------------------------------------------------


def map_to_child(name):
    """Helper function that return a function for extracting a field name
    """
    return lambda pfdb_obj: getattr(pfdb_obj, name, None)

# -----------------------------------------------------------------------------


def map_to_children_of_type(class_name):
    """Helper function that return a function for extracting children
    of a given type (class_name).
    """
    return lambda pfdb_obj: pfdb_obj.get_children_of_type(class_name)

# -----------------------------------------------------------------------------
# Key dictionary helpers
# -----------------------------------------------------------------------------


def get_key_priority(key_name):
    """Return number that can be used to sort keys in term of priority
    """
    priority_value = 0
    path_token = key_name.split('.')
    if 'Name' in key_name:
        priority_value -= 100

    for token in path_token:
        if token[0].isupper():
            priority_value += 1
        else:
            priority_value += 10

    priority_value *= 100
    priority_value += len(key_name)

    return priority_value

# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Sort helpers
# -----------------------------------------------------------------------------


def sort_dict(d, key=None):
    """Create a key sorted dict
    """
    return {k: d[k] for k in sorted(d, key=key)}

# -----------------------------------------------------------------------------


def sort_dict_by_priority(d):
    """Create a key sorted dict
    """
    return sort_dict(d, key=get_key_priority)

# -----------------------------------------------------------------------------
# Dictionary helpers
# -----------------------------------------------------------------------------


def get_or_create_dict(root, key_path, overriden_keys):
    """Helper function to get/create a container dict for a given key path
    """
    current_container = root
    for i, key in enumerate(key_path):
        if key not in current_container:
            current_container[key] = {}
        elif not isinstance(current_container[key], dict):
            overriden_keys['.'.join(key_path[:i+1])] = current_container[key]
            current_container[key] = {}
        current_container = current_container[key]

    return current_container


# -----------------------------------------------------------------------------
# String helpers
# -----------------------------------------------------------------------------

def remove_prefix(s, prefix):
    if not s or not prefix or not s.startswith(prefix):
        return s

    return s[len(prefix):]
