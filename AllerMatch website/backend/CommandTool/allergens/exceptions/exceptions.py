class WrongInputException(Exception):
    """
    The input file contains no correct DNA or protein sequence
    """
    def __init__(self, message="Wrong character in DNA/AA input sequence or wrong format"):
        self.message = message
        super().__init__(self.message)