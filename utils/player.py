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
        """Get the sample and play the enveloped instrument if not already done

        Parameters
        ----------
        t : float
            The time
        freq : float
            The frequency (note) to play
        dt : float
            1/fs, i.e. the time between two consecutive samples
        """

        if not self._envelope.pressed:
            self._envelope.press()
            self._t = 0
        self._t += dt
        if self._t > self._press_time:
            self._t = 0
            self._envelope.unpress()
        return self._instrument.get_sample(t, freq,
                                           self._envelope.get_amplitude(dt))
