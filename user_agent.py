"""
Module with agents representing users implementations


"""

from mesa import Agent
import numpy as np


class UserAgent(Agent):
    def __init__(self, unique_id, model, communication, starting_position, memory_size, user_latitude,
                 user_sharpness):
        super().__init__(unique_id, model)
        self.user_latitde = user_latitude
        self.user_sharpness = user_sharpness
        self.communication = communication
        self.user_memory = self.Memory(starting_position, memory_size)

    class Memory():
        """
        Internal class representing user memory and providing methods to modify and read it
        """

        def __init__(self, first_info_bit, mem_size):
            self.mem_size = mem_size
            self.user_position = first_info_bit
            self.info_bits = np.reshape(first_info_bit, (1, 2))

        def add_new_info_bit(self, info_bit):
            """
            Saves new info_bit in user memory
            """
            # removing random info_bit if memory is full
            if (self.info_bits.shape[1] > self.mem_size):
                info_bit_to_remove = np.randint(self.mem_size)
                self.info_bits[info_bit_to_remove] = info_bit
            # appending memory with new info otherwise
            else:
                self.info_bits = np.concatenate(info_bit, info_bit)

        def calculate_user_position(self):
            """
            Calculates user position based on positions in user memory
            """
            return np.mean(self.info_bits, axis=0)

    def try_to_integrate_info_bit(self, info_bit):
        """
        Tries to integrate new info bit to user memory based on attitude
         distance between user and info bit, user latitude and user sharpness
        """
        dist = np.linalg.norm(self.user_position - info_bit)
        probability = self.user_latitde ** self.user_sharpness / (
                dist ** self.user_sharpness + self.user_latitde ** self.user_sharpness)
        if np.random >= probability:
            return True
        else:
            return False
