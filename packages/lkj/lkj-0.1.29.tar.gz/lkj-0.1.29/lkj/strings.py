"""Utils for strings"""


# Note: Vendored in i2.multi_objects and dol.util
def truncate_string_with_marker(
    s, *, left_limit=15, right_limit=15, middle_marker="..."
):
    """
    Return a string with a limited length.

    If the string is longer than the sum of the left_limit and right_limit,
    the string is truncated and the middle_marker is inserted in the middle.

    If the string is shorter than the sum of the left_limit and right_limit,
    the string is returned as is.

    >>> truncate_string_with_marker('1234567890')
    '1234567890'

    But if the string is longer than the sum of the limits, it is truncated:

    >>> truncate_string_with_marker('1234567890', left_limit=3, right_limit=3)
    '123...890'
    >>> truncate_string_with_marker('1234567890', left_limit=3, right_limit=0)
    '123...'
    >>> truncate_string_with_marker('1234567890', left_limit=0, right_limit=3)
    '...890'

    If you're using a specific parametrization of the function often, you can
    create a partial function with the desired parameters:

    >>> from functools import partial
    >>> truncate_string = partial(truncate_string_with_marker, left_limit=2, right_limit=2, middle_marker='---')
    >>> truncate_string('1234567890')
    '12---90'
    >>> truncate_string('supercalifragilisticexpialidocious')
    'su---us'

    """
    middle_marker_len = len(middle_marker)
    if len(s) <= left_limit + right_limit:
        return s
    elif right_limit == 0:
        return s[:left_limit] + middle_marker
    elif left_limit == 0:
        return middle_marker + s[-right_limit:]
    else:
        return s[:left_limit] + middle_marker + s[-right_limit:]


# TODO: Generalize so that it can be used with regex keys (not escaped)
def regex_based_substitution(replacements: dict, regex=None, s: str = None):
    """
    Construct a substitution function based on an iterable of replacement pairs.

    :param replacements: An iterable of (replace_this, with_that) pairs.
    :type replacements: iterable[tuple[str, str]]
    :return: A function that, when called with a string, will perform all substitutions.
    :rtype: Callable[[str], str]

    The function is meant to be used with ``replacements`` as its single input,
    returning a ``substitute`` function that will carry out the substitutions
    on an input string.

    >>> replacements = {'apple': 'orange', 'banana': 'grape'}
    >>> substitute = regex_based_substitution(replacements)
    >>> substitute("I like apple and bananas.")
    'I like orange and grapes.'

    You have access to the ``replacements`` and ``regex`` attributes of the
    ``substitute`` function:

    >>> substitute.replacements
    {'apple': 'orange', 'banana': 'grape'}

    """
    import re
    from functools import partial

    if regex is None and s is None:
        replacements = dict(replacements)

        if not replacements:  # if replacements iterable is empty.
            return lambda s: s  # return identity function

        regex = re.compile("|".join(re.escape(key) for key in replacements.keys()))

        substitute = partial(regex_based_substitution, replacements, regex)
        substitute.replacements = replacements
        substitute.regex = regex
        return substitute
    else:
        return regex.sub(lambda m: replacements[m.group(0)], s)


from typing import Callable, Iterable, Sequence


class TrieNode:
    def __init__(self):
        self.children = {}
        self.count = 0  # Number of times this node is visited during insertion
        self.is_end = False  # Indicates whether this node represents the end of an item


def identity(x):
    return x


def unique_affixes(
    items: Iterable[Sequence],
    suffix: bool = False,
    *,
    egress: Callable = None,
    ingress: Callable = identity,
) -> Iterable[Sequence]:
    """
    Returns a list of unique prefixes (or suffixes) for the given iterable of sequences.
    Raises a ValueError if duplicates are found.

    Parameters:
    - items: Iterable of sequences (e.g., list of strings).
    - suffix: If True, finds unique suffixes instead of prefixes.
    - ingress: Callable to preprocess each item. Default is identity function.
    - egress: Callable to postprocess each affix. Default is appropriate function based on item type.
      Usually, ingress and egress are inverses of each other.

    >>> unique_affixes(['apple', 'ape', 'apricot', 'banana', 'band', 'bandana'])
    ['app', 'ape', 'apr', 'bana', 'band', 'banda']

    >>> unique_affixes(['test', 'testing', 'tester'])
    ['test', 'testi', 'teste']

    >>> unique_affixes(['test', 'test'])
    Traceback (most recent call last):
    ...
    ValueError: Duplicate item detected: test

    >>> unique_affixes(['abc', 'abcd', 'abcde'])
    ['abc', 'abcd', 'abcde']

    >>> unique_affixes(['a', 'b', 'c'])
    ['a', 'b', 'c']

    >>> unique_affixes(['x', 'xy', 'xyz'])
    ['x', 'xy', 'xyz']

    >>> unique_affixes(['can', 'candy', 'candle'])
    ['can', 'candy', 'candl']

    >>> unique_affixes(['flow', 'flower', 'flight'])
    ['flow', 'flowe', 'fli']

    >>> unique_affixes(['ation', 'termination', 'examination'], suffix=True)
    ['ation', 'rmination', 'amination']

    >>> import functools
    >>> ingress = functools.partial(str.split, sep='.')
    >>> egress = '.'.join
    >>> items = ['here.and.there', 'here.or.there', 'here']
    >>> unique_affixes(items, ingress=ingress, egress=egress)
    ['here.and', 'here.or', 'here']

    """
    items = list(map(ingress, items))

    # Determine the default egress function based on item type
    if egress is None:
        if all(isinstance(item, str) for item in items):
            # Items are strings; affixes are lists of characters
            def egress(affix):
                return "".join(affix)

        else:
            # Items are sequences (e.g., lists); affixes are lists
            def egress(affix):
                return affix

    # If suffix is True, reverse the items
    if suffix:
        items = [item[::-1] for item in items]

    # Build the trie and detect duplicates
    root = TrieNode()
    for item in items:
        node = root
        for element in item:
            if element not in node.children:
                node.children[element] = TrieNode()
            node = node.children[element]
            node.count += 1
        # At the end of the item
        if node.is_end:
            # Duplicate detected
            if suffix:
                original_item = item[::-1]
            else:
                original_item = item
            original_item = egress(original_item)
            raise ValueError(f"Duplicate item detected: {original_item}")
        node.is_end = True

    # Find the minimal unique prefixes/suffixes
    affixes = []
    for item in items:
        node = root
        affix = []
        for element in item:
            node = node.children[element]
            affix.append(element)
            if node.count == 1:
                break
        if suffix:
            affix = affix[::-1]
        affixes.append(affix)

    # Postprocess affixes using egress
    affixes = list(map(egress, affixes))
    return affixes
