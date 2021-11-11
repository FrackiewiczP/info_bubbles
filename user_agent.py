"""
Module with agents representing users implementations


"""

from mesa import Agent
import numpy as np
from integration_function import check_integration


class UserAgent(Agent):
    def __init__(
        self,
        unique_id,
        model,
        communication,
        initial_position,
        memory_capacity,
        user_latitude,
        user_sharpness,
    ):
        super().__init__(unique_id, model)
        self.user_friends = list()
        self.user_latitude = user_latitude
        self.user_sharpness = user_sharpness
        self.communication = communication
        self.user_position = initial_position
        self.info_count = 0

        initial_info_bit = np.insert(
            initial_position.copy(), 0, self.generate_info_id()
        )
        self.user_memory = self.Memory(initial_info_bit, memory_capacity)

    class Memory:
        """
        Internal class representing user memory and providing methods to modify and read it
        """

        def __init__(self, first_info_bit, mem_capacity):
            self.mem_capacity = mem_capacity
            self.info_bits = np.reshape(first_info_bit, (1, 3))

        def get_size(self):
            """
            Returns number of info_bits currently saved in memory

            :return:   number of info_bits in memory
            :rtype: int
            """

            return self.info_bits.shape[0]

        def add_new_info_bit(self, info_bit):
            """
            Saves new info_bit in user memory, if memory is full
            it replace one random info_bit from memory with the new one.

            :param info_bit: matrix with information id and coordinates
            on political spectrum
            :type info_bit: numpy.ndarray
            """
            # removing random info_bit if memory is full
            if self.info_bits.shape[0] >= self.mem_capacity:
                info_bit_to_remove = np.random.randint(self.mem_capacity)
                self.info_bits[info_bit_to_remove] = info_bit
            # appending memory with new info otherwise
            else:
                self.info_bits = np.concatenate([self.info_bits, info_bit], axis=0)

        def calculate_user_position(self):
            """
            Calculates user position based on positions of info_bits in user memory

            :return: new user position on political spectrum
            :rtype: numpy.ndarray

            """

            return np.mean(self.info_bits[:, 1:3], axis=0)

    def update_position(self):
        """
        Updates user_position with new position calculated by user memory

        :return: new user position on political spectrum
        :rtype: numpy.ndarray
        """
        self.user_position = self.user_memory.calculate_user_position()

        return self.user_position

    def try_to_integrate_info_bit(self, info_bit):
        """
        Tries to integrate new info bit to user memory based on attitude
         distance between user and info bit, user latitude and user sharpness

        :param info_bit: matrix with information id and coordinates
            on political spectrum
        :type info_bit: numpy.ndarray
        :return: logical indicator if info_bit was successfully integrated
        :rtype: bool
        """

        if check_integration(
            self.user_position,
            info_bit[:, 1:3],
            self.user_latitude,
            self.user_sharpness,
        ):
            self.user_memory.add_new_info_bit(info_bit)
            self.model.register_user_movement(self.unique_id)
            return True
        else:
            return False

    def send_info_to_friends(self):
        info = np.reshape(
            self.user_memory.info_bits[np.random.randint(self.user_memory.get_size())],
            (1, 3),
        )
        for friend in self.user_friends:
            self.model.forward_info_bit(friend, info)

    def generate_info_id(self):
        self.info_count += 1
        return float(f"{self.unique_id}.{self.info_count}")

    def communicate(self):
        info = self.communication.create_info_bit(
            self.user_position, self.generate_info_id()
        )
        self.try_to_integrate_info_bit(info)
