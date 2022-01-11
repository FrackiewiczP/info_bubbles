"""
Module with agents representing users implementations


"""

import numpy as np
from mesa import Agent
from Simulation.information import Information

from Simulation.integration_function import check_integration


class UserAgent(Agent):
    def __init__(
        self,
        unique_id,
        model,
        memory_capacity,
        user_latitude,
        user_sharpness,
    ):
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
            self.mem_capacity = mem_capacity
            self.info_bits = np.zeros(shape=(mem_capacity, 3))
            self.size = 0
            self.add_new_info_bit(first_info_bit)

        def add_new_info_bit(self, info_bit: Information):

            """
            Saves new info_bit in user memory, if memory is full
            it replace one random info_bit from memory with the new one.
            :param info_bit: matrix with information id and coordinates
            on political spectrum
            :type info_bit: numpy.ndarray
            """

            # removing random info_bit if memory is full

            if self.size >= self.mem_capacity:
                info_bit_to_remove = np.random.randint(self.mem_capacity)
                self.info_bits[info_bit_to_remove] = info_bit.to_numpy()
            # appending memory with new info otherwise
            else:
                self.info_bits[self.size] = info_bit.to_numpy()
                self.size += 1

        def calculate_user_position(self):
            """
            Calculates user position based on positions of info_bits in user memory
            :return: new user position on political spectrum
            :rtype: numpy.ndarray
            """
            return np.mean(self.info_bits[: self.size, 1:3], axis=0)

        def get_random_information(self):
            """
            Creates Information based on random row from info_bits
            :return: New Information based on existing one
            :rtype: Information
            """
            if self.size == 0:
                return None
            return Information(
                self.info_bits[np.random.randint(self.size), :].reshape((1, 3))
            )

        def get_info_bits_ids(self):
            # if self.size == 0:
            #     return list()
            return self.info_bits[: self.size, 0]

        def calculate_mean_distance(self, position):
            distances = np.linalg.norm(
                self.info_bits[: self.size, 1:3] - position, axis=1
            )
            return np.mean(distances)

    def get_random_information(self):
        return self.memory.get_random_information()

    def update_position(self):
        """
        Updates user_position with new position calculated by user memory

        :return: new user position on political spectrum
        :rtype: numpy.ndarray
        """
        self.position = self.memory.calculate_user_position()
        self.mean_info_dist = self.memory.calculate_mean_distance(self.position)
        return self.position

    def try_to_integrate_info_bit(self, info_bit: Information):

        """
        Tries to integrate new info bit to user memory based on attitude
        distance between user and info bit, user latitude and user sharpness.

        Unless id of info is already present in user memory in this case method
        returns False before trying to integrate new info_bit

        :param info_bit: matrix with information id and coordinates
            on political spectrum
        :type info_bit: numpy.ndarray
        :return: logical indicator if info_bit was successfully integrated
        :rtype: bool
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
