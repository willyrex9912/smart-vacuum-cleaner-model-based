from typing import List

from enums.state_enum import StateEnum
from enums.action_enum import ActionEnum
from enums.perception_enum import PerceptionEnum
from model.rule import Rule
from model.quadrant import Quadrant
import logging
import time

logging.basicConfig(level=logging.INFO, format='[%(threadName)s] (%(levelname)s) %(message)s')


class VacuumCleaner:

    def __init__(self, initial_quadrant: Quadrant):
        self.current_quadrant = initial_quadrant
        self.rules = [
            Rule(StateEnum.QUADRANT_CHECKED, ActionEnum.QUADRANT_CHECK),
            Rule(StateEnum.QUADRANT_CLEANED, ActionEnum.QUADRANT_CLEANING),
            Rule(StateEnum.QUADRANT_CHANGED, ActionEnum.QUADRANT_CHANGE),
        ]
        self.state = None
        self.action = None

    def update_state(self, perception: PerceptionEnum) -> StateEnum:
        if self.state is None and self.action is None and perception is None:
            return StateEnum.QUADRANT_CHECKED
        elif self.state == StateEnum.QUADRANT_CHECKED and self.action == ActionEnum.QUADRANT_CHECK and perception == PerceptionEnum.DIRTY_QUADRANT:
            return StateEnum.QUADRANT_CLEANED
        elif self.state == StateEnum.QUADRANT_CHECKED and self.action == ActionEnum.QUADRANT_CHECK and perception == PerceptionEnum.CLEANED_QUADRANT:
            return StateEnum.QUADRANT_CHANGED
        elif self.state == StateEnum.QUADRANT_CLEANED and self.action == ActionEnum.QUADRANT_CLEANING and perception == PerceptionEnum.DIRTY_QUADRANT:
            return StateEnum.QUADRANT_CLEANED
        elif self.state == StateEnum.QUADRANT_CLEANED and self.action == ActionEnum.QUADRANT_CLEANING and perception == PerceptionEnum.CLEANED_QUADRANT:
            return StateEnum.QUADRANT_CHANGED
        elif self.state == StateEnum.QUADRANT_CHANGED and self.action == ActionEnum.QUADRANT_CHANGE and perception == PerceptionEnum.DIRTY_QUADRANT:
            return StateEnum.QUADRANT_CLEANED
        elif self.state == StateEnum.QUADRANT_CHANGED and self.action == ActionEnum.QUADRANT_CHANGE and perception == PerceptionEnum.CLEANED_QUADRANT:
            return StateEnum.QUADRANT_CHANGED
        else:
            return StateEnum.QUADRANT_CHECKED

    def match_rule(self, state: StateEnum) -> Rule:
        for rule in self.rules:
            if rule.condition == state:
                return rule
        return self.rules[0]

    def work(self, perception: PerceptionEnum, quadrants: List[Quadrant]):
        self.state = self.update_state(perception)
        rule = self.match_rule(self.state)
        self.action = rule.action

        if self.action == ActionEnum.QUADRANT_CHECK:
            self.is_necessary_to_clean(quadrants)
        elif self.action == ActionEnum.QUADRANT_CLEANING:
            self.clean()
        elif self.action == ActionEnum.QUADRANT_CHANGE:
            self.move(quadrants)

    def is_necessary_to_clean(self, quadrants: List[Quadrant]):
        logging.info("Testing if its necessary to clean the quadrant")
        if self.current_quadrant.is_cleaned:
            self.work(PerceptionEnum.CLEANED_QUADRANT, quadrants)
        else:
            self.work(PerceptionEnum.DIRTY_QUADRANT, quadrants)

    def clean(self):
        time.sleep(5)
        self.current_quadrant.is_cleaned = True
        logging.info("Quadrant " + self.current_quadrant.name + " is cleaned")

    def move(self, quadrants: List[Quadrant]):
        if self.current_quadrant.name == "A":
            self.move_right(quadrants)
        else:
            self.move_left(quadrants)
        logging.info("Cleaner moved to quadrant " + self.current_quadrant.name)

    def move_left(self, quadrants: List[Quadrant]):
        self.current_quadrant = quadrants[0]

    def move_right(self, quadrants: List[Quadrant]):
        self.current_quadrant = quadrants[1]
