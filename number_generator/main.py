from own_generator import *


if __name__ == "__main__":

    generator = NumberGenerator(200)
    generator.generate()
    print(generator.get_numbers())
