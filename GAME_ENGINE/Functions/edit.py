import pygame

def edit_str(instr, blinkpos):

    global charpressed

    if blinkpos > len(instr):
        blinkpos = len(instr)
            
    inlst = list(instr)
    
    if charpressed == "BACKSPACE":
        if blinkpos != 0:
            blinkpos -= 1
            try:
                del inlst[blinkpos]
            except Exception:
                pass

    elif charpressed == "UP":
        blinkpos = 0
        
    elif charpressed == "DOWN":
        blinkpos = len(inlst)
        
    elif charpressed == "LEFT":
        if blinkpos != 0:
            blinkpos -= 1
        
    elif charpressed == "RIGHT":
        if blinkpos != len(inlst):
            blinkpos += 1
    
    elif charpressed == "WORD_LEFT":
        if blinkpos > 0:
            i = blinkpos - 1
            while i > 0 and inlst[i].isspace():
                i -= 1
            while i > 0 and not inlst[i-1].isspace():
                i -= 1
            blinkpos = i
    
    elif charpressed == "WORD_RIGHT":
        L = len(inlst)
        i = blinkpos
        while i < L and inlst[i].isspace():
            i += 1
        while i < L and not inlst[i].isspace():
            i += 1
        blinkpos = i
        
    elif charpressed != "":
        s = charpressed
        for ch in s:
            inlst.insert(blinkpos, ch)
            blinkpos += 1
    
    return([list_to_string(inlst, ""), blinkpos])

def warp(tfont, text, max_width):
    def text_width(s):
        return tfont.get_rect(s).width

    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = word if current_line == "" else current_line + " " + word

        if text_width(test_line) <= max_width:
            current_line = test_line
        else:
            if text_width(word) > max_width:

                if current_line:
                    lines.append(current_line)
                    current_line = ""

                chunk = ""
                for char in word:
                    test_chunk = chunk + char
                    if text_width(test_chunk) <= max_width:
                        chunk = test_chunk
                    else:
                        lines.append(chunk)
                        chunk = char
                if chunk:
                    current_line = chunk

            else:
                lines.append(current_line)
                current_line = word

    if current_line:
        lines.append(current_line)

    return lines

def list_to_string(my_list, separator):
    if isinstance(my_list, str):
        return my_list
    return separator.join(map(str, my_list))

def string_to_list(my_string, separator):
    """Splits a string back into a list based on the separator."""
    return my_string.split(separator)



def get_text_width(text, font_size, font_name="Arial"):

    text = str(text)
    
    font_size += 1
    
    if not pygame.display.get_init():
        pygame.display.init()
    

    font = pygame.freetype.SysFont(font_name, font_size)
    
    text_rect = font.get_rect(text)
    
    return(text_rect.width)

def replace_str(full_string, sub_string):
    """
    Removes the first occurrence of sub_string from full_string.
    """
    if sub_string in full_string:
        return full_string.replace(sub_string, "", 1)
    return full_string
