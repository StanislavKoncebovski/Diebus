import tools
from location import Location


# region Time conversions
def local_to_universal(t_local: float, location: Location) -> float:
    """
    Converts local time to universal time.
    Universal Time (U.T.C.) is the local mean solar time, reckoned from midnight,
    at the observatory in Greenwich, England, the 0◦ meridian. (RD).
    Local time is the mean solar time at the locality.
    RDM (12.6)
    :param t_local: The local time.
    :param location: The location.
    :return: The Universal time.
    """
    return t_local - location.longitude / 360


def universal_to_local(t_universal: float, location: Location) -> float:
    """
    Converts universal time to local time.
    RDM (12.7)
    :param t_universal: The universal time.
    :param location: The location.
    :return: The local time.
    :return: The local time.
    """
    return t_universal + location.longitude / 360


def universal_to_standard(t_universal: float, location: Location) -> float:
    """
    Converts universal time to standard local time.
    RDM (12.8)
    :param t_universal: The universal time.
    :param location: The location.
    :return: The standard time.
    """
    return t_universal + location.zone / 24


def standard_to_universal(t_standard: float, location: Location) -> float:
    """
    Converts universal time to standard time.
    RDM (12.9)
    :param t_standard: The universal time.
    :param location: The location.
    :return: The standard time in the locality.
    """
    return t_standard - location.zone / 24


def local_to_standard(t_local: float, location: Location) -> float:
    """
    Converts local time to standard time.
    RDM (12.10).
    :param t_local: The local time.
    :param location: The location.
    :return: The standard time.
    """
    return universal_to_standard(local_to_universal(t_local, location), location)


def standard_to_local(t_standard: float, location: Location) -> float:
    """
    Converts standard time to local time.
    RDM (12.11).
    :param t_standard: The standard time.
    :param location: The location.
    :return: The universal time.
    """
    return universal_to_local(standard_to_universal(t_standard, location), location)
# endregion

def ephemeris_correction(t: float) -> float:
    """

    :param t:
    :return:
    """
    year = tools.gregorian_year_from_rata_die(t)
    pass
