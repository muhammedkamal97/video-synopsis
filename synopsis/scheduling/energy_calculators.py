from abc import abstractmethod, ABC
from typing import List

from object.activity.activity_tube import ActivityTube
from synopsis.scheduling.scheduler_utils import get_video_length, compute_total_intersection
from itertools import permutations


class AbstractEnergyCalculator(ABC):

    @abstractmethod
    def compute_energy(self, activity_tubes: List[ActivityTube], start_frames: List[int]) -> float:
        """
        Compute the energy of the synopsis video.
        Energy is considered the cost so lower energy implies better results.

        :param activity_tubes: A list of all activity tubes.
        :param start_frames: A list of each activity starting frame in the synopsis video.
        :return: The energy of the synopsis video.
        :rtype: float
        """
        pass


class SimpleEnergyCalculator(AbstractEnergyCalculator):

    def __init__(self, alpha=0.0002, beta=.05):
        self.alpha = alpha
        self.beta = beta

    def compute_energy(self, activity_tubes: List[ActivityTube], start_frames: List[int]) -> float:
        """
        Compute the energy of the synopsis video.
        E = L + alpha * I
        E is the total energy.
        L is the length of the synopsis video in frames.
        alpha is a weighting constant that's given in the initialization (default = 1).
        I is the total intersection between the activity tubes in pixels.

        :param activity_tubes: A list of all activity tubes.
        :param start_frames: A list of each activity starting frame in the synopsis video.
        :return: The energy of the synopsis video.
        :rtype: float
        """

        # print("Video Length : ", end="")
        # print(get_video_length(activity_tubes, start_frames))
        energy = get_video_length(activity_tubes, start_frames)

        # print("Intersection : ", end="")
        # print(compute_total_intersection(activity_tubes, start_frames))
        energy += self.alpha * compute_total_intersection(activity_tubes, start_frames)

        disorder = 0
        for i,j in permutations(range(len(activity_tubes)), 2):
            if activity_tubes[i].start_frame < activity_tubes[j].start_frame and start_frames[i] > start_frames[j]:
                disorder += 1
            if activity_tubes[i].start_frame > activity_tubes[j].start_frame and start_frames[i] < start_frames[j]:
                disorder += 1

        # print("Disorder : ", end="")
        # print(disorder)
        energy += self.beta * disorder
        
        return energy
