import math
import random
import numpy as np

def sin(t, f):
    """Return a sine sample computed at time t and frequency f

    Parameters
    ----------
    t : float
        The time
    f : float
        The frequency

    Returns
    -------
    float
        The sine at time t and frequency f
    """

    return math.sin(2*math.pi*f*t)

def cos(t, f):
    """Return a cosine sample computed at time t and frequency f

    Parameters
    ----------
    t : float
        The time
    f : float
        The frequency

    Returns
    -------
    float
        The cosine at time t and frequency f
    """

    return math.cos(2*math.pi*f*t)

def sanitize(x):
    """Clamps x between -1 and +1. Also NaN gets converted to 0

    Parameters
    ----------
    x : float
        The value to clamp

    Returns
    -------
    float
        A number between -1 and +1
    """

    if x > 1:
        return +1
    if x < 1:
        return -1
    if math.isnan(x):
        return 0
    return x

def safe_division(num, den):
    """Division without ZeroDivisionError
    num/0 with positive num will return +infinity
    num/0 with negative num will return -infinity
    0/0 will return NaN

    Parameters
    ----------
    num : float
        The numerator
    den : float
        The denominator

    Returns
    -------
    float
        The division result
    """

    if den == 0:
        if num > 0:
            return float("inf")
        elif num < 0:
            return float("-inf")
        else:
            return float("nan")
    return num/den

def tan(t, f1, f2=None):
    """Computes sin(t, f1)/cos(t, f2)

    Parameters
    ----------
    t : float
        The time
    f1 : float
        The frequency of the sine
    f2 : float, optional
        The frequency of the cosine (defaults to f1)
    """

    if f2 is None:
        f2 = f1
    return safe_division(sin(t, f1), cos(t, f2))

def square(t, f):
    """Return a square wave sample computed at time t and frequency f

    Parameters
    ----------
    t : float
        The time
    f : float
        The frequency

    Returns
    -------
    float
        The square wave sample at time t and frequency f
    """
    x = sin(t, f)
    if x >= 0:
        return +1
    return -1

def sawtooth(t, f):
    """Return a sawtooth wave sample computed at time t and frequency f

    Parameters
    ----------
    t : float
        The time
    f : float
        The frequency

    Returns
    -------
    float
        The sawtooth wave sample at time t and frequency f
    """
    return (2*f*t) % 2 - 1

def mod(a, b):
    """Computes the modulus of a by b. It also handles edge cases

    Parameters
    ----------
    a : complex
        The numerator
    b : complex
        The denominator

    Returns
    -------
    float
        The remainder of the division of the aboslute values of a by b.
        If b == 0 then 0 is returned
    """

    if isinstance(a, complex):
        a = abs(a)
    if isinstance(b, complex):
        b = abs(b)
    if b == 0:
        return 0
    return a % b

def get_freq_from_interval(base_note, note_interval):
    """Returns the note away note_interval semitones from base_note

    Parameters
    ----------
    base_note : float
        The frequency of the base note
    note_interval : float
        The numbers of semitones away from base_note. Can also be negative or
        a decimal number

    Returns
    -------
    float
        The frequency of the note away note_interval semitones from
        base_note
    """

    return base_note * 2**(note_interval/12)

def get_freq_from_scale_degree(i, base_note, scale):
    """Returns the i-th scale degree in key of base_note

    Parameters
    ----------
    i : int
        The i-th scale degree
    base_note : float
        The key of the scale
    scale : list[int]
        The intervals of the scale

    Returns
    -------
    float
        The frequency of the note
    """
    return get_freq_from_interval(base_note, scale[i])

def get_freqs_from_scale__fixed_interval(t, interval, base_note, scale):
    """Returns the same notes from the scale periodically

    Ever wanted to repeat the same scale over and over and over and over?
    Wait no more, use this function and be happy :)

    Parameters
    ----------
    t : float
        The time
    interval : float
        The time interval to which change scale note
    base_note : float
        The frequency of the base note
    scale : list[int]
        The intervals of the scale to repeat

    Returns
    -------
    float
        The frequency of the note
    """
    i = int(t // interval) % len(scale)
    return get_freq_from_scale_degree(i, 440.0, scale)
