import os

class AccountMaker:
    def __init__(self, user):
        path = os.path.dirname(os.path.abspath(__file__))

        # Path of the new directory to be created
        new_acc = os.path.join(path, user)

        if not os.path.exists(new_acc):
            os.mkdir(new_acc)
            
            try:
                new_path = os.path.join(new_acc, user)
                open(new_path + ".txt", "x")
                
            except:
                print("File already exists")
        