# world_frame/places.py

class Place:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name


# Minimal canonical places
HOSPITAL = Place("hospital")
HOME = Place("home")
CAR = Place("car")
OUTSIDE = Place("outside")
ROOM = Place("room")