import csv,random

class csvRead:

    def __init__(self, file):
        try:
            file= open(file)
        except FileNotFoundError:
            print("File not found")
        self.file = file
        self.reader = csv.DictReader(self.file)

    def read(self):
        # Reading data randomly
        return random.choice(list(self.reader))
