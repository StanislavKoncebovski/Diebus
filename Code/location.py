from dataclasses import dataclass


@dataclass
class Location:
    """

    """
    name: str
    latitude: float     # Degrees
    longitude: float    # Degrees
    elevation: float    # m
    zone: float

    def __init__(self, name: str = "", latitude: float = 0, longitude: float = 0, elevation: float = 0,
                 zone: float = 0):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.zone = zone

# R&D Location constants
URBANA = Location("Urbana", 40.11059, -88.20727, 222, -6)
MECCA = Location("Mecca", 21.42664, 39.82563, 0, 2)
JERUSALEM = Location("Jerusalem", 31.76904,	35.21633, 0, 2)
# Elevation of Tehran is taken to be 0, as in RDU instead of 1100 which is nearer to truth.
TEHRAN = Location("Tehran", 35.696111, 51.423056, 0, 3.5)
HAIFA = Location("Haifa", 32.81841, 34.9885, 0, 2)

if __name__ == '__main__':
    print(URBANA)

    from numpy.polynomial.polynomial import Polynomial

    poly = Polynomial([1, 2, 3]) # 1.0 + 2.0 * x + 3.0 * x^2
    x = 0.5
    y = poly(x)
    print(y)
