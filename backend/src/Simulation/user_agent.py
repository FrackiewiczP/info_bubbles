"""
Module with UserAgent class implementation.

"""

import numpy as np
from mesa import Agent, Model
from Simulation.information import Information

from Simulation.integration_function import check_integration


class UserAgent(Agent):
    """UserAgent is a class representing user of some social website in our simulation.

    UserAgent has internal class called Memory that represents user memory.
    """

    def __init__(
        self,
        unique_id: int,
        model: Model,
        memory_capacity: int,
        user_latitude: float,
        user_sharpness: float,
    ):
        """
        Creates new UserAgent with given parameters.

        Args:
            unique_id (int): unique id of our user
            model (Model): model of simulation in which our UserAgent participate
            memory_capacity (int): Maximal number of informations that user can have in it's memory
            user_latitude (float): Latitude of acceptance of our UserAgent
            user_sharpness (float): Sharpness of acceptance of our UserAgent
        """
        super().__init__(unique_id, model)
        self.latitude = user_latitude
        self.sharpness = user_sharpness
        self.info_count = 0

        self.memory = self.Memory(Information(), memory_capacity)
        self.position = self.memory.calculate_user_position()
        self.mean_info_dist = self.memory.calculate_mean_distance(self.position)

    class Memory:
        """
        Internal class representing user memory and providing methods to modify and read it
        """

        def __init__(self, first_info_bit: Information, mem_capacity: int):
            """Creates new Memory with one Information and given capacity

            Args:
                first_info_bit (Information): Information that will be stored in info_bits
                mem_capacity (int): Capacity of Memory, how many Information it will be able to store
            """
            self.mem_capacity = mem_capacity
            self.info_bits = np.zeros(shape=(mem_capacity, 3))
            self.size = 0
            self.add_new_info_bit(first_info_bit)

        def add_new_info_bit(self, info_bit: Information):
            """Saves new Information user memory, if memory is full
            it replace one random info_bit from memory with the new one.
            Information is stored as row in matrix. In first column id's of Informations are stored and
            every other column represents Informations positions in specific dimension

            Args:
                info_bit (Information): Information to save
            """
            # removing random info_bit if memory is full
            if self.size >= self.mem_capacity:
                info_bit_to_remove = np.random.randint(self.mem_capacity)
                self.info_bits[info_bit_to_remove] = info_bit.to_numpy()
            # appending memory with new info otherwise
            else:
                self.info_bits[self.size] = info_bit.to_numpy()
                self.size += 1

        def calculate_user_position(self) -> np.ndarray:
            """Calculates user position based on positions of info_bits in user memory

            Returns:
                np.ndarray: new user position, mean of all informations in memory
            """
            return np.mean(self.info_bits[: self.size, 1:3], axis=0)

        def get_random_information(self) -> Information:
            """Creates Information based on random row from info_bits attribute

            Returns:
                Information: New Information based on existing one
            """
            if self.size == 0:
                return None
            return Information(
                self.info_bits[np.random.randint(self.size), :].reshape((1, 3))
            )

        def get_info_bits_ids(self) -> np.ndarray:
            """Returns id's of all Informations in info_bits

            Returns:
                np.ndarray: Array of all Information id's in info_bits
            """
            return self.info_bits[: self.size, 0]

        def calculate_mean_distance(self, position: np.ndarray) -> float:
            """
            Calculates mean distance from position passed as parameter and Informations in UserAgent Memory

            Args:
                position (np.ndarray): Position from which mean distance should be calculated

            Returns:
                float: Mean distance
            """
            distances = np.linalg.norm(
                self.info_bits[: self.size, 1:3] - position, axis=1
            )
            return np.mean(distances)

    def get_random_information(self) -> Information:
        """Creates new Information based on random Information from UserAgent Memory

        Returns:
            Information: New Information based on existing one

        """
        return self.memory.get_random_information()

    def update_position(self) -> np.ndarray:
        """Updates position with new position calculated by UserAgent Memory
            Also updates mean_info_dist attribute, value of mean distance between user and Informations in his memory

        Returns:
            np.ndarray: [description]
        """
        self.position = self.memory.calculate_user_position()
        self.mean_info_dist = self.memory.calculate_mean_distance(self.position)
        return self.position

    def try_to_integrate_info_bit(self, info_bit: Information) -> bool:
        """Tries to integrate new Information to UserAgent Memory memory based on attitude
        distance between UserAgent and Information, UserAgent latitude and sharpness.

        If id of Information is already present in UserAgent Memory, method
        returns False before trying to integrate these Information.

        Args:
            info_bit (Information): Information that UserAgent tries to integrate

        Returns:
            bool: indicator if integration was succesfull
        """

        # if user already knows this info
        if info_bit.get_id() in self.memory.get_info_bits_ids():
            return False
        if check_integration(
            self.position,
            info_bit.position,
            self.latitude,
            self.sharpness,
        ):
            self.memory.add_new_info_bit(info_bit)
            return True
        else:
            return False
