"""
Module with agents representing users implementations


"""
from random import random, choice

import numpy as np
from mesa import Agent

from information import Information
from integration_function import check_integration


class UserAgent(Agent):
    def __init__(
            self,
            unique_id,
            model,
            initial_position,
            memory_capacity,
            user_latitude,
            user_sharpness,
    ):
        super().__init__(unique_id, model)
        self.user_friends = list()
        self.user_latitude = user_latitude
        self.user_sharpness = user_sharpness
        self.user_position = initial_position
        self.info_count = 0

        position = list()
        position.append(random() * 2 - 1)
        position.append(random() * 2 - 1)
        initial_info_bit = Information(position)
        self.user_memory = self.Memory(initial_info_bit, memory_capacity)

    class Memory:
        """
        Internal class representing user memory and providing methods to modify and read it
        """

        def __init__(self, first_info_bit, mem_capacity):
            self.mem_capacity = mem_capacity
            self.info_bits = list()
            self.info_bits.append(first_info_bit)

        def get_size(self):
            """
            Returns number of info_bits currently saved in memory

            :return:   number of info_bits in memory
            :rtype: int
            """

            return len(self.info_bits)

        def add_new_info_bit(self, info_bit):
            """
            Saves new info_bit in user memory, if memory is full
            it replace one random info_bit from memory with the new one.

            :param info_bit: matrix with information id and coordinates
            on political spectrum
            :type info_bit: numpy.ndarray
            """
            # removing random info_bit if memory is full
            if len(self.info_bits) >= self.mem_capacity:
                info_bit_to_remove = np.random.randint(self.mem_capacity)
                self.info_bits[info_bit_to_remove] = info_bit
            # appending memory with new info otherwise
            else:
                for i in self.info_bits:
                    if (i == info_bit):
                        return
                self.info_bits.append(info_bit)

        def calculate_user_position(self):
            """
            Calculates user position based on positions of info_bits in user memory

            :return: new user position on political spectrum
            :rtype: numpy.ndarray

            """
            a = []
            for i in self.info_bits:
                b = i.getPosition()
                a.append(b)
            a = np.asarray(a)
            return np.mean(a, axis= 0)

        def getRandom(self):
            return choice(self.info_bits)

    def update_position(self):
        """
        Updates user_position with new position calculated by user memory

        :return: new user position on political spectrum
        :rtype: numpy.ndarray
        """
        self.user_position = self.user_memory.calculate_user_position()

        return self.user_position

    def try_to_integrate_info_bit(self, info_bit: Information):
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
                info_bit.getPosition(),
                self.user_latitude,
                self.user_sharpness,
        ):
            self.user_memory.add_new_info_bit(info_bit)
            self.model.register_user_movement(self.unique_id)
            return True
        else:
            return False

    def send_info_to_friends(self):
        info = self.user_memory.getRandom()
        for friend in self.user_friends:
            self.model.forward_info_bit(friend, info)
