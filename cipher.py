# Objects for linear and differential
class Cryptanalysis:
    # the inputs that visualise() takes. Here to check what needs to be part of the object
    # inputString, numOfBits, numOfRounds, sBoxes, sBox, pBox, type, first, tr, pbs, p_fin, svalues
    sbox = []
    pbox = []
    num_rounds = 0
    trail = []
    probabilities = []
    input_string = ""

    # Initialise the cryptanalysis class
    def __init__(self, type, sbox, pbox, num_rounds):
        self.sbox = sbox
        self.pbox = pbox
        self.num_rounds = num_rounds
        print("yhe")

  ######################
  # DIFFERENTIAL CLASS #
  ######################

class Differential(Cryptanalysis):
    print("yeh")
    """Class for differential cryptanalysis. This inherits from the cryptanalysis class."""
    # Initialise the differential class
    def __init__(self, sbox, pbox, type):
        # Call the super class initialiser
        super().__init__(type, sbox, pbox)


  ################
  # LINEAR CLASS #
  ################

class Linear(Cryptanalysis):
    print("ehy")

    # Initialise the linear class
    def __init__(self, sbox, pbox, type):
        # Call the super class initialiser
        super().__init__(type, sbox, pbox)
