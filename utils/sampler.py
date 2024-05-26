import numpy as np

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
