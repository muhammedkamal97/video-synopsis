from random import random
from typing import List

from synopsis.scheduling.abstract_scheduler import AbstractScheduler
from synopsis.scheduling.energy_calculators import SimpleEnergyCalculator, AbstractEnergyCalculator
from synopsis.scheduling.scheduler_utils import *
from simanneal import Annealer


class ActivityAnnealer(Annealer):
    """
    An module that perform simulated annealing to find the optimal schedule for the activity tubes.
    """

    def __init__(self, activity_tubes: List[ActivityTube], energy_calculator: AbstractEnergyCalculator):
        """
        Initialize the annealer with the activity tubes and the energy calculator.
        :param activity_tubes: The list of activity tubes to be scheduled.
        :param energy_calculator: the energy calculator class
        """
        self.activity_tubes = activity_tubes
        self.energy_calculator = energy_calculator
        self.start_frames = [0 for x in activity_tubes]
        super(ActivityAnnealer, self).__init__(self.start_frames)

    def move(self):
        """
        Change the start frame of random activity to random start frame between 0 and 1.25 * L.
        L is the length of current video.
        """

        ind = random.randint(0, len(self.activity_tubes))
        cur_video_length = get_video_length(self.activity_tubes, self.start_frames)
        new_start_frame = random.randint(0, int(cur_video_length * 1.25))
        self.start_frames[ind] = new_start_frame

    def energy(self):
        """
        Compute current energy using the energy_calculator.
        :return: energy of current state.
        :rtype: float
        """
        return self.energy_calculator.compute_energy(self.activity_tubes, self.start_frames)


class SimAnnealingScheduler(AbstractScheduler):

    def schedule(self, activity_tubes: List[ActivityTube]) -> List[int]:
        """
        Schedule using simulated annealing.
        :param activity_tubes: The list of activity tubes to be scheduled.
        :return: List of integers with same length as the activity_tubes list.
            Each integer represents the starting frame of the activity tube -with the same index- in the synopsis video.
        :rtype: List[int]
        """
        energy_calculator = SimpleEnergyCalculator()
        annealer = ActivityAnnealer(activity_tubes, energy_calculator)
        annealer.set_schedule(annealer.auto(minutes=0.2))
        annealer.copy_strategy = "slice"
        start_frames, energy = annealer.anneal()
        return start_frames
