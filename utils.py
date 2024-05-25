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

class Player:
    """
    Note player

    Attributes
    ----------
    press_time : float
        For how much time is a note pressed?
    """
    def __init__(self, instrument, envelope, press_time):
        """
        Parameters
        ----------
        instrument : Instrument
            The instrument to play
        envelope : Envelope
            The sound envelope
        press_time : float
            For how much time is a note pressed?
        """

        self._instrument = instrument
        self._envelope = envelope
        self._press_time = press_time

    def get_sample(self, t, freq, dt):
        if not self._envelope.pressed:
            self._envelope.press()
            self._t = 0
        self._t += dt
        if self._t > self._press_time:
            self._t = 0
            self._envelope.unpress()
        return self._instrument.get_sample(t, freq,
                                           self._envelope.get_amplitude(dt))

class Envelope:
    """
    Envelope base class
    
    Methods
    -------
    get_amplitude(dt)
        Returns the current amplitude
    """

    def get_amplitude(self, dt):
        return NotImplemented

class ADSR(Envelope):
    """
    ADSR Envelope class

    Attributes
    ----------
    attack : float
        The attack time
    decay : float
        The decay time
    sustain : float
        The sustain amplitude
    release : float
        The release time
    pressed : bool
        Is the note pressed?

    Methods
    -------
    press()
        Strike the note

    unpress()
        Release the note

    get_amplitude(dt)
        Get the amplitude value in the current time
    """
    ATTACK  = 0
    DECAY   = 1
    SUSTAIN = 2
    RELEASE = 3

    def __init__(self, attack, decay, sustain, release):
        """
        Parameters
        ----------
        attack : float
            The attack time
        decay : float
            The decay time
        sustain : float
            The sustain amplitude
        release : float
            The release time
        """

        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release
        self.pressed = False
        self._status = None

    def press(self):
        """Simulate a note press"""

        self._status = ADSR.ATTACK
        self._t = 0
        self._cur_vol = 0
        self.pressed = True

    def unpress(self):
        """Simulate a note release"""
        self.pressed = False

    def get_amplitude(self, dt):
        """Get the amplitude value at the current time

        Parameters
        ----------
        dt : float
            1/fs, i.e. the time between two consecutive samples

        Returns
        -------
        float
            The current amplitude value
        """

        if self._status == None:
            return 0
        elif self._status == ADSR.ATTACK:
            ret = self._t/self.attack
            if self._t > self.attack:
                self._t = 0
                self._status = ADSR.DECAY
                return 1
        elif self._status == ADSR.DECAY:
            ret = 1 - (1 - self.sustain)*self._t/self.decay
            if self._t > self.decay:
                self._t = 0
                self._status = ADSR.SUSTAIN
                return self.sustain
        elif self._status == ADSR.SUSTAIN:
            if self.pressed:
                return self.sustain
            else:
                self._status = ADSR.RELEASE
                self._t = 0
                return self.sustain
        elif self._status == ADSR.RELEASE:
            ret = self.sustain * (1 - self._t/self.release)
            if self._t > self.release:
                self._t = 0
                self._status = None
                return 0
        else:
            raise ValueError(f"Unexpected status value {self._status}")
        self._t += dt
        return ret

class Sampler:
    """
    Base class which exposes a get_sample(t) method

    Methods
    -------
    get_sample(t, f)
        Returns the sample to play
    """

    def get_sample(self, t, f):
        """Returns the sample to play

        Parameters
        ----------
        t : float
            The time
        f : float
            The frequency to which play this sample
        """
        return NotImplemented

class Instrument(Sampler):
    """
    Instrument which can be used to play notes

    An instrument is defined by its timbre and by 

    Methods
    -------
    get_sample(t, f)
        Returns the sample to play
    """

    def __init__(self, freqs, amps):
        """
        Parameters
        ----------
        freqs : list[float]
            The timbre frequency samples
        amps : list[float]
            The timbre amplitude samples
        """

        self.freqs = np.array(freqs)
        self.amps = np.array(amps)

    def get_sample(self, t, f, volume):
        """Returns the sample to play

        Parameters
        ----------
        t : float
            The time
        f : float
            The frequency to which play this sample
        volume : float
            The volume at which play this sample
        """
        return (volume * self.amps * np.sin(2 * np.pi * f * self.freqs * t)).\
                sum()

class Note:
    """
    Class which defines a note

    Attributes
    ----------
    pitch : float
        The frequency of the note
    duration : float
        The note duration
    """
    base_notes = {
            "C" : -9,
            "C#": -8,
            "Db": -8,
            "D" : -7,
            "D#": -6,
            "Eb": -6,
            "E" : -5,
            "F" : -4,
            "F#": -3,
            "Gb": -3,
            "G" : -2,
            "G#": -1,
            "Ab": -1,
            "A" :  0,
            "A#": +1,
            "Bb": +1,
            "B" : +2,
            }

    @staticmethod
    def note_str2freq(note):
        """Converts a note string representation to frequency

        The conversion is based on ISO16 (i.e. A4 = 440 Hz).
        The string representation is as follows:

             D#    4    +53.5
            |__|  |_|  |_____|
             |     |     |
             *-----+-----+----> base_note
                   |     |
                   *-----+----> octave
                         |
                         *----> cents (can be float)

        The base_note and octave are REQUIRED, the cents are optional.

        Parameters
        ----------
        note : str
            The note string representation (e.g. A4 or Gb6-87)

        Returns
        -------
        float
            The frequency of the note
        """
        # The note frequency is calculated with reference to A4 = 440Hz
        # That frequency will be shifted according to the note notation
        base_note = note[:2]
        if not base_note.endswith("#") and not base_note.endswith("b"):
            base_note = note[0]
        semitone_shift = Note.base_notes[base_note]

        cent_shift = 0
        i_cents = note.find("+")
        if i_cents == -1:
            i_cents = note.find("-")
        if i_cents == -1:
            i_cents = None
        else:
            cent_shift = float(note[i_cents:])

        octave_shift = int(note[len(base_note):i_cents]) - 4

        return 440 * 2**(octave_shift + semitone_shift/12 + cent_shift/1200)

    def __init__(self, pitch, duration):
        """
        Parameters
        ----------
        pitch : float or string
            The pitch of the note. Can be represented as string (e.g. A#4)
        duration : float
            The note duration
        """
        self.pitch = \
                Note.note_str2freq(pitch) if isinstance(pitch, str) else pitch
        self.duration = duration

class Score:
    """
    Base class which exposes a get_note(dt) method

    All classes subclassing this are required to keep track of the duration of
    the note and everytime get_note is called this duration will decrement
    acccordingly

    Methods
    -------
    get_note(dt)
        Returns the note to be played
    """

    def get_note(self, dt):
        """Returns the note to be played

        dt : float
            1/fs i.e. the time between two samples
        """
        return NotImplemented

class PresetScore(Score):
    """
    Class which stores a score to be played

    Attributes
    ----------
    score_end : bool
        Has the score ended?

    Methods
    -------
    get_note(dt)
        Returns the note to be played
    """

    def __init__(self, notes):
        """
        Parameters
        ----------
        notes : list[Note]
            The list of notes to play
        """

        self.score_end = False
        self._durations = []
        self._frequencies = []
        self._residual_duration = -1
        for note in notes:
            self._durations.append(note.duration)
            self._frequencies.append(note.pitch)

    def get_note(self, dt):
        """Returns the note to be played

        Parameters
        ----------
        dt : float
            1/fs, i.e. the time between two consecutive samples

        Returns
        -------
        float
            The frequency of the note to be played
        """
        try:
            if self._residual_duration < 0:
                self._current_note = self._frequencies.pop(0)
                self._residual_duration = self._durations.pop(0)
        except IndexError:
            # score ended, return silence
            self.score_end = True
            return 0
        self.score_end = False
        self._residual_duration -= dt
        return self._current_note

class ScaleRandomPlayer(Score):
    """
    Get random notes from some scale

    Methods
    -------
    get_note(dt)
        Returns the note (frequency) to play
    """

    def __init__(self, scale, base_note,
                 seed = None,
                 min_note_duration = 0.04,
                 max_note_duration = 2):
        """
        Parameters
        ----------
        seed : anything
            The seed to use to initialize the inner random number generator
        base_note : float or callable
            The key of the scale. If it is a callable a float should be
            returned (useful to change the key)
        min_note_duration : float or callable (default: 0.04 seconds)
            The minimum duration of a note. If it is a callable a float should
            be returned (useful for change in times)
        max_note_duration : float or callable (default: 2 seconds)
            The maximum duration of a note. If it is a callable a float should
            be returned (useful for change in times)
        """

        self.rnd = random.Random(seed)
        self.scale = scale
        self.base_note = base_note
        self.min_note_duration = min_note_duration
        self.max_note_duration = max_note_duration
        self.note_duration = None
        self.note_freq = None

    @staticmethod
    def _get_or_call(var):
        if callable(var):
            return var()
        return var

    def get_note(self, dt):
        """Returns the note to be played

        Parameters
        ----------
        dt : float
            1/fs i.e. the time between two samples

        Returns
        -------
        float
            The note to be played
        """

        if self.note_duration is None or self.note_duration < 0:
            base_note = ScaleRandomPlayer._get_or_call(self.base_note)
            min_note_duration = ScaleRandomPlayer.\
                    _get_or_call(self.min_note_duration)
            max_note_duration = ScaleRandomPlayer.\
                    _get_or_call(self.max_note_duration)
            self.note_duration = self.rnd.uniform(min_note_duration,
                                                  max_note_duration)
            self.note_freq = get_freq_from_interval(base_note,
                                self.rnd.choice(self.scale))
        self.note_duration -= dt
        return self.note_freq

