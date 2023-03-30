import os

class FileHandler:
    def __init__(self, user):
        self.user = user
        self.path = os.path.join("users", self.user, self.user + ".txt")
        
    # Copied from https://stackoverflow.com/questions/4710067/how-to-delete-a-specific-line-in-a-text-file-using-python
    def deleteLine(self, delPhrase):
        condition = False
        
        with open(self.path, "r") as file:
            text = file.readlines()
        with open(self.path, "w") as file:
            for i in text:
                if i.strip("\n") == delPhrase and condition == False:
                    condition = True
                else:
                    file.write(i)