from .base import get_freq_from_interval
import random

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

