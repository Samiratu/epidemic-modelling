# Status
# susceptible = 3
# infected = 2
# immune = 1
# dead = 0
# Methods
# is infected
# has recovered
# has died
from random import *
from disease import *


class Person:
    def __init__(self, status, disease):
        self.status = status
        if self.status == 2:
            self.disease = disease
        else:
            self.disease = None

    def is_infected(self, someperson):
        if someperson.status == 2 and self.status == 3:
            if randint(1, 100) <= someperson.disease.rate_of_infection:
                return True

    def has_recovered(self):
        if self.status == 2:
            if randint(1, 100) <= self.disease.rate_of_recovery:
                return True

    def is_susceptible(self):
        if self.status == 3:
            return True

    def has_died(self):
        if self.status == 2:
            if randint(1, 100) <= self.disease.rate_of_lethality:
                return True


