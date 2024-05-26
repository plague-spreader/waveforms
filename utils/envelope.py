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
