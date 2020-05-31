import random
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
        start_frames = [random.randint(0, 3000) for i in range(len(self.activity_tubes))]#BasicScheduler().schedule(self.activity_tubes)
        super(ActivityAnnealer, self).__init__(start_frames)

    def move(self):
        """
        Change the start frame of random activity to random start frame between 0 and 1.25 * L.
        L is the length of current video.
        """

        ind = random.randint(0, len(self.activity_tubes)-1)
        prev  = self.state[ind]
        new_start_frame = random.randint(max([prev-500, 0]), prev+500)
        self.state[ind] = new_start_frame

    def energy(self):
        """
        Compute current energy using the energy_calculator.
        :return: energy of current state.
        :rtype: float
        """
        e = self.energy_calculator.compute_energy(self.activity_tubes, self.state)
        # print(e)
        return e


class SimAnnealingScheduler(AbstractScheduler):

    def schedule(self, activity_tubes: List[ActivityTube]) -> List[int]:
        """
        Schedule using simulated annealing.
        :param activity_tubes: The list of activity tubes to be scheduled.
        :return: List of integers with same length as the activity_tubes list.
            Each integer represents the starting frame of the activity tube -with the same index- in the synopsis video.
        :rtype: List[int]
        """
        energy_calculator = SimpleEnergyCalculator(.0001)
        annealer = ActivityAnnealer(activity_tubes, energy_calculator)
        print("Starting Energy ", annealer.energy())
        # print(annealer.auto(minutes=1, steps=100))
        # {'tmax': 4800000.0, 'tmin': 6700.0, 'steps': 780, 'updates': 100} : 100
        # annealer.set_schedule(annealer.auto(minutes=1, steps=100))
        annealer.set_schedule(annealer.auto(minutes=1))
        annealer.copy_strategy = "slice"
        start_frames, energy = annealer.anneal()
        return start_frames
