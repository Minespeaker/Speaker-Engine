def load(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()

    return(file_content)

class execute:
    def __init__(self, screen, base_vars):
        """
        Initialise the Container
        
        :param self: The Container
        :param screen: A Tuple of the size of the Screen, leave as empty Tuple for no screen
        :param base_vars: Variables that are existant by default
        """
        self.container = {} if base_vars == None else dict(base_vars)
        self.frame = 0
        if screen != ():
            self.add_class("pygame", "display", "")
            self.add_class("freetype", "fonts", "pygame")
            self.run_code("display.init()")
            self.run_code("fonts.init()")
            self.run_code(f"screen = display.Surface({screen})\n")
            self.run_code(f"font = [fonts.SysFont('Arial', s) for s in range (500)]")

    def add_class(self, classv, targ_class_name, parclass):
        if isinstance(targ_class_name, str):
            if parclass != "":
                exec(f"from {parclass} import {classv} as {targ_class_name}", self.container, self.container)
            else:
                exec(f"import {classv} as {targ_class_name}", self.container, self.container)
        else:
            self.container[targ_class_name] = classv

    def set_screen_size(self, size):
        self.run_code(f"screen = display.Surface({size})\n")

    def run_code(self, code):
        tmp = self.container
        try:
            exec(code, self.container, self.container)
            return ""
        except Exception as e:
            self.container = tmp
            return str(e)

    def run_display(self, code):
        prev_frame = self.container
        self.container["FRAME"] = self.frame
        try:
            exec(code, self.container, self.container)
        except Exception as e:
            self.container = prev_frame
            return self.container["screen"], str(e)
        self.frame += 1
        self._loop = code
        return self.container["screen"], ""
        
    def get_var(self, var=str):
        return self.container[var]
    
    def getout(self, code):
        if isinstance(code, str):
            code = [code]
        import copy
        tmp = copy.deepcopy(self.container)
        code[-1] = "out = "+str(code[-1])
        exec("\n".join(code), tmp, tmp)
        return tmp["out"]
    
    def get_code():
        out = []