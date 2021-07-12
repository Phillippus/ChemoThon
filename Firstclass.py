class Chemotherapy:
    def __str__(self):
        return "Toto je prvý pokus o triedu"
    
    def __init__(self, name, dose):
        self.name= name
        self.dose= dose
        print(name)
        print(dose)

print(Chemotherapy)