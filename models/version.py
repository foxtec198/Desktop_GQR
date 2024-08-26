class Version:
    def get_version(self):
        with open('version') as v: 
            oldVersion = v.read()
        return oldVersion