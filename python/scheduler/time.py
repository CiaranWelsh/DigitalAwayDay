import time


class Time:

    def __init__(self, hours, minutes, seconds):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

        self._normalise_time()

    def __eq__(self, other):
        if not isinstance(other, Time):
            raise TypeError('Need Time object by got {}'.format(type(other)))
        if self.seconds == other.seconds and self.minutes == other.minutes and self.hours == other.hours:
            return True
        else:
            return False

    def __ne__(self, other):
        if not isinstance(other, Time):
            raise TypeError('Need Time object by got {}'.format(type(other)))
        if self.seconds == other.seconds and self.minutes == other.minutes and self.hours == other.hours:
            return False
        else:
            return True

    def __gt__(self, other):

        if not isinstance(other, Time):
            raise TypeError('Need Time object by got {}'.format(type(other)))
        if self.hours > other.hours:
            return True
        elif self.hours < other.hours:
            return False

        if self.minutes > other.minutes:
            return True
        elif self.minutes < other.minutes:
            return False

        if self.seconds > other.seconds:
            return True
        elif self.seconds < other.seconds:
            return False
        return False

    def __lt__(self, other):

        if not isinstance(other, Time):
            raise TypeError('Need Time object by got {}'.format(type(other)))
        if self.hours < other.hours:
            return True
        elif self.hours > other.hours:
            return False

        if self.minutes < other.minutes:
            return True
        elif self.minutes > other.minutes:
            return False

        if self.seconds < other.seconds:
            return True
        elif self.seconds > other.seconds:
            return False
        return False

    def __le__(self, other):

        if not isinstance(other, Time):
            raise TypeError('Need Time object by got {}'.format(type(other)))
        if self.hours <= other.hours:
            return True
        elif self.hours >= other.hours:
            return False

        if self.minutes <= other.minutes:
            return True
        elif self.minutes >= other.minutes:
            return False

        if self.seconds <= other.seconds:
            return True
        elif self.seconds >= other.seconds:
            return False
        return False

    def __ge__(self, other):
        if not isinstance(other, Time):
            raise TypeError('Need Time object by got {}'.format(type(other)))
        if self.hours >= other.hours:
            return True
        elif self.hours <= other.hours:
            return False

        if self.minutes >= other.minutes:
            return True
        elif self.minutes <= other.mintes:
            return False

        if self.seconds >= other.seconds:
            return True
        elif self.seconds <= other.seconds:
            return False
        return False

    def __str__(self):
        return "{:0>2d}:{:0>2d}:{:0>2d}".format(self.hours, self.minutes, self.seconds)

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if not isinstance(other, Time):
            raise ValueError('Can only add Time object to Time instance. Got {}'.format(type(other)))
        seconds = self.seconds + other.seconds
        minutes = self.minutes + other.minutes
        hours = self.hours + other.hours
        return Time(hours, minutes, seconds)

    def __sub__(self, other):
        if not isinstance(other, Time):
            raise ValueError('Can only subtract Time object to Time instance. Got {}'.format(type(other)))

        seconds = self.seconds - other.seconds
        # if seconds < 0:

        minutes = self.minutes - other.minutes
        hours = self.hours - other.hours
        return Time(hours, minutes, seconds)

    def _normalise_time(self):
        """
        Ensure integrity of time format (i.e. hours < 60
        :return:
        """
        if self.seconds > 59:
            self.minutes += int(self.seconds / 60)
            self.seconds = self.seconds % 60

        elif self.seconds < 0:
            self.minutes -= 1
            self.seconds = 60 + self.seconds  # plus because seconds is negative

        if self.minutes > 59:
            self.hours += int(self.minutes / 60)
            self.minutes = self.minutes % 60

        elif self.minutes < 0:
            self.hours -= 1
            self.minutes = 60 + self.minutes

        if self.hours > 23:
            raise NotImplementedError('times > 24h are not presently supported')

        if self.hours < 0:
            raise NotImplementedError('Cannot go lower than 0h')

    def to_minutes(self):
        return self.hours * 60 + self.minutes + self.seconds / 60

    def is_between(self, start, end):
        if start > end:
            raise ValueError('start "{}" cannot be greater than end "{}"'.format(start, end))
        if self >= start and self < end:
            return True
        return False
