"""non classifiable tools"""

import numpy as np


def safe_isnan(value, extend_to_None=True):
    """
    Make np.isnan working on any type.

    >>> test = {False: False, "": False, None: True, 1: False, np.nan:True}
    >>> for test, exp in test.items():
    ...     assert safe_isnan(test) == exp

    None can be checked as `np.NaN` depending on `extend_to_None`:

    >>> safe_isnan(None, extend_to_None=False)
    False
    >>> safe_isnan(None, extend_to_None=True)  # default
    True
    >>> safe_isnan(""), safe_isnan(0)
    (False, False)
    """
    try:
        return np.isnan(value)
    except TypeError:
        if value is None and extend_to_None:
            return True
        return False


def replace_nan(value, default=None):
    """
    >>> replace_nan(5)
    5
    >>> replace_nan(np.nan)
    >>> replace_nan(np.nan, 0)
    0
    """
    if safe_isnan(value, extend_to_None=False):
        return default
    return value


def calc_repetition(span=None, nb=None, pitch=None, raise_on_error=True):
    """
    >>> calc_repetition(span=4, pitch=2)
    (4, 2, 2)
    >>> calc_repetition(span=4, nb=3)
    (4, 3, 1.333...)
    >>> calc_repetition(pitch=2, nb=3)
    (6, 3, 2)
    >>> calc_repetition(span=5)
    Traceback (most recent call last):
        ...
    ValueError: Two of `span=5`, `pitch=None`, `nb=None` must be provided
    >>> calc_repetition(nb=0)
    (0, 0, 0)
    >>> calc_repetition(pitch=1.5, nb=5)
    (7.5, 5, 1.5)
    """
    # convert np.NaN to None in order to use pd.DataFrameApply conveniently:
    span, nb, pitch = map(replace_nan, (span, nb, pitch))
    if nb is not None and nb == 0:
        # if nb == 0 occurs in two cases:
        #  * no repetition at all, in which case span and pitch are null
        #  * span and pitch are provided, nb needs to be calculated
        if set([span, pitch]) == {None}:
            return (0, 0, 0)
        else:
            nb = None
    if span and pitch and nb:
        raise ValueError('"span", "pitch" and "nb" are all defined')
    if nb is not None and not isinstance(nb, int):
        try:
            nb = int(nb)
        except ValueError:
            raise TypeError("`nb` must be an integer or a float")
    if len(set((span, pitch, nb)) - {None}) != 2:
        if raise_on_error:
            raise ValueError(f"Two of `{span=}`, `{pitch=}`, `{nb=}` must be provided")
        else:
            return span, nb, pitch
    if span and nb:
        pitch = span / nb
    elif span and pitch:
        nb = int(span / pitch)
    elif nb and pitch:
        span = pitch * nb
    if nb is not None:
        nb = int(nb)
    return span, nb, pitch


def repeat(start, discard=(), span=None, nb=None, pitch=None, rnd=4):
    """
    Repeat a value starting from
    >>> repeat(start=1, pitch=2, nb=3)
    (1.0, 3.0, 5.0, 7.0)

    """
    span, nb, pitch = calc_repetition(span, nb, pitch)
    if set((span, nb, pitch)) == {None}:
        return (float(start),)
    else:
        instances = np.linspace(
            start=start, stop=(start + span), num=nb + 1, endpoint=True
        )
    if discard:
        instances = np.delete(instances, discard)
    return tuple(instances.round(rnd))


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
