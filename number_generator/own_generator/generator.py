from datetime import datetime


class NumberGenerator():
    def __init__(self, number):
        self.number_of_elements = number
        self.elements = []

    def generate(self):
        # basis for generation
        base = datetime.now().time()

        self.elements = []

    def get_numbers(self):
        return self.elements
