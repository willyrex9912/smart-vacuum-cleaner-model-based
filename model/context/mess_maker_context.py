from typing import List
from model.quadrant import Quadrant
from model.context.context import Context
import threading


class MessMakerContext(Context):

    def __init__(self, quadrants: List[Quadrant]):
        self.quadrants = quadrants

    def run(self):
        quadrant_name = input("Type quadrant name to be dirty:\n")
        quadrant = self.find_quadrant(quadrant_name)
        if quadrant is not None:
            quadrant.is_cleaned = False
        threading.Timer(1, self.run).start()

    def find_quadrant(self, quadrant_name):
        for quadrant in self.quadrants:
            if quadrant.name == quadrant_name:
                return quadrant
        return None
