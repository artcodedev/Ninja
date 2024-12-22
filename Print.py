



class Print:
    
    # class bcs:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    
    @staticmethod
    def error(txt): print(f"{Print.FAIL}{txt}{Print.ENDC}")
    
    @staticmethod
    def warning(txt): print(f"{Print.WARNING}{txt}{Print.ENDC}")
    
    @staticmethod
    def log(txt): print(f"{Print.OKCYAN}{txt}{Print.ENDC}")
    
    @staticmethod
    def ok(txt): print(f'{Print.OKGREEN}{txt}{Print.ENDC}')
    
