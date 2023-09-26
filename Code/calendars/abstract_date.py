class AbstractDate:
    """
    Basis for all classes representing calendars.
    This class is abstract and must be downtyped by concrete calendar classes, such as Gregorian calendar.
    Based upon:

    RDM:
        Reingold, Edward M., and Nachum Dershowitz. Calendrical Calculations: The Millenium Edition. 3rd Edition.
        Cambridge: Cambridge University Press, 2001, 422 p. ISBN 0521-777526. doi 10.1017/cbo9781107051119.

    RDU:
        Reingold, Edward M., and Nachum Dershowitz. Calendrical Calculations: The Ultimate Edition. 4th edition.
        Cambridge; New York: Cambridge University Press, 2018, 662 p. ISBN 978-1-107-68316-7. doi 10.1017/9781107415058.

    Uses the RDM's RD (rata die) value as the basis for all time measuring calendrical systems.
    """
    def to_moment(self) -> float:
        """
        Converts the date expressed in terms of the calendar class, into the RD time moment.
        E.g. for the Gregorian calendar it converts Gregorian year, month and day into the RD time moment.
        :return: The RD time moment.
        """
        pass

    def from_moment(self, t: float) -> None:
        """
        Converts an RD time moment to an instance of a calendrical date in a specific system, e.g. Gregorian date.
        :param t: The RD time moment to convert.
        :return: None. The instance of the specific calendrical class will be generated instead.
        """
        pass

    def to_string(self, format: str = None) -> str:
        """
        String representation.
        Differs from class to class, with some offering more formatting choices than the others.
        :param format: String defining how to format the output string.
        :return: Formatted string representation.
        """
        return self.__repr__()
