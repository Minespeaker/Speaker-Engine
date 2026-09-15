import pygame, os, math, time, pyperclip, sys, subprocess, multiprocessing, platform
from pygame import freetype
from Classes.editor import text, editor
from Classes.executer import execute
from Classes.pyselect import pyselect

OS = platform.system()

osvar = {"Windows": "Microsoft windows", "Linux": "Linux"}

OS = osvar[OS]

if OS == "Linux":
    OS = f"{OS}: {platform.freedesktop_os_release()["NAME"]} {platform.freedesktop_os_release()["VERSION_CODENAME"]} {platform.freedesktop_os_release()["VERSION"]}"
 
print(f"Detected OS Environment: {OS}")

time.sleep(1)

sep = "\\" if "Windows" in OS else "/"

debug = True
skip = True

tmp = os.path.dirname(__file__)
tmp = tmp.split(sep)
FILE_PATH = sep.join(tmp)+sep
print(FILE_PATH)
sys.path[0] = (FILE_PATH)

if not os.path.exists(os.path.join(FILE_PATH, "GAMES")):
    os.mkdir(os.path.join(FILE_PATH, "GAMES"))
    for i in os.listdir(os.path.join(FILE_PATH, "Quickaccess")):
        os.remove(os.path.join(FILE_PATH, "Quickaccess", i))

file_type = ".sngf"

def dprint(*args):
    global debug
    try:
        if debug:
            print(args)
    except NameError:
        debug = False


cpfl = None

ld = {"sx": 0, "sy": 0, "menu_open": False, "menu_slt": None, "rnm": False, "rnt": None}

from Functions.fileRW   import *
from Functions.fileSORT import *
from Functions.edit     import *
from Functions.export   import *
from Functions.math     import *
from Functions.colours  import *
from Functions.list     import *
from Functions.misc     import *

def listfiles(foldername, files, txtin, size, scrn, off, mx, my, mc, _parent=True, path=[], ogox=None, ogoy=None):
    global ld, sep
    if _parent:
        path = []
    pygame.init()
    freetype.init()
    ox, oy = off
    if ogox == None or ogoy == None:
        ogox, ogoy = ox, oy
    path.append(foldername)
    x, y = size
    _pos = 0
    linesize = 25
    indent = 25
    if x < 0: x = 0
    if y < 0: y = 0
    surf = pygame.Surface((x, y), pygame.SRCALPHA)
    txt = freetype.SysFont("Arial", linesize-2)
    scrnrect = pygame.Rect(ox, oy, x, y)
    hover = False
    
    scrnsz = scrn
    scrn = pygame.Surface(scrnsz, pygame.SRCALPHA)
    
    folders = set()

    if _parent:
        tmprect = pygame.Rect(ox, oy, x, linesize)
        if tmprect.collidepoint(mx, my) and scrnrect.collidepoint(mx, my):
            pygame.draw.rect(scrn, (192, 192, 192, 128), tmprect)
            if mc[0]:
                files = {foldername: (list(files[foldername])[0], not list(files[foldername])[1])}
            if mc[2]:
                ld["menu_open"] = True
                ld["menu_slt"] = path
                ld["sx"], ld["sy"] = mx, my
    if _parent:
        if list(files[foldername])[1]:
            txt.render_to(surf, (0, 0), f"{foldername} ▾", (255, 255, 255))
        else:
            txt.render_to(surf, (0, 0), f"{foldername} ▸", (255, 255, 255))
    else:
        txt.render_to(surf, (0, 1), f"|-{foldername} ▾", (255, 255, 255))

    unpackedfiles, headunpack = files[foldername]
    if headunpack:
        for name, data in unpackedfiles.items():
            _pos += 1   
            if type(data) == tuple:
                contents, unpack = data
                tmprect = pygame.Rect(-indent*(len(path)+1)+ox, _pos*linesize+oy, x+indent*(len(path)+1), linesize)
                if tmprect.collidepoint(mx, my) and scrnrect.collidepoint(mx, my):
                    hover = True
                    hoverpos = _pos
                    if mc[0]:
                        unpack = not unpack
                        unpackedfiles[name] = contents, unpack
                        data = unpackedfiles[name]
                    if mc[2]:
                        ld["menu_open"] = True
                        ld["menu_slt"] = path
                        ld["menu_slt"].append(name)
                        ld["sx"], ld["sy"] = mx, my
                if unpack:
                    childsurf, childfiles, childpos = listfiles(name, {name: data}, txtin, (x-indent, y-(_pos-linesize)), scrnsz, (ox+indent, oy+_pos*linesize), mx, my, mc, False, list(path), ogox, ogoy)
                    unpackedfiles[name] = childfiles, unpack
                    folders.add(childsurf)
                    for _ in range (childpos):
                        _pos += 1
                        txt.render_to(surf, (indent, _pos*linesize), "|", (255, 255, 255))
                else:
                    txt.render_to(surf, (indent, _pos*linesize), f"|-{name} ▸", (255, 255, 255))


            else:
                tmprect = pygame.Rect(-indent*(len(path)+1)+ox, _pos*linesize+oy, x+indent*(len(path)+1), linesize)
                if tmprect.collidepoint(mx, my) and scrnrect.collidepoint(mx, my):
                    hover = True
                    hoverpos = _pos
                    
                    if mc[2]:
                        ld["menu_open"] = True
                        ld["menu_slt"] = path
                        ld["menu_slt"].append(name)
                        ld["sx"], ld["sy"] = mx, my
                    
                txt.render_to(surf, (indent, _pos*linesize), f"|-{name}", (255, 255, 255))
    files = {foldername: (unpackedfiles, headunpack)}
    scrn.blit(surf, off)
    menu = pygame.Rect(ld["sx"], ld["sy"], 120, 150)
    
    if menu.collidepoint(mx, my) and ld["menu_open"]:
        hover = False
    if mc[0] and not menu.collidepoint(mx, my):
        ld["sx"], ld["sy"] = 0, 0
        ld["menu_open"] = False
        ld["menu_slt"] = None
        ld["rnt"] = None
        ld["rnm"] = False
    if hover:
        selrect = pygame.Surface((x+indent*(len(path)+1), linesize), pygame.SRCALPHA)
        pygame.draw.rect(selrect, (192, 192, 192, 128), (0, 0, ox+x, linesize))
        scrn.blit(selrect, (ogox, oy+hoverpos*linesize))
    pygame.draw.rect(surf, ((0, 0, 0, 1)), (indent, ((_pos+1)*linesize)-(linesize*0.525), 12, linesize*0.525))
    
    for folder in folders:
        scrn.blit(folder, (0, -1))
        
    if ld["menu_slt"] != None:
        if ld["menu_slt"] == path or ld["menu_slt"][:-1] == path:
            txt2 = freetype.SysFont("Arial", 20)
            slc = ld["menu_slt"] == path
            slf = ld["menu_slt"][-1]
            bx, by = ld["sx"], ld["sy"]
            pygame.draw.rect(scrn, col[64], menu, 0, 5)
            ls = 25
            nfl = pygame.Rect(bx, by+5, list(menu.size)[0], 20)
            nfd = pygame.Rect(bx, by+5+ls, list(menu.size)[0], 20)
            rnm = pygame.Rect(bx, by+5+(ls*2), list(menu.size)[0], 20)
            dlt = pygame.Rect(bx, by+5+(ls*3), list(menu.size)[0], 20)
            cpy = pygame.Rect(bx, by+5+(ls*4), list(menu.size)[0], 20)
            pst = pygame.Rect(bx, by+5+(ls*5), list(menu.size)[0], 20)
                
            global cpfl
            
            if nfl.collidepoint(mx, my):
                pygame.draw.rect(scrn, col[127], nfl)
            if nfd.collidepoint(mx, my):
                pygame.draw.rect(scrn, col[127], nfd)
            if rnm.collidepoint(mx, my):
                pygame.draw.rect(scrn, col[127], rnm)
                if mc[0] or ld["rnm"]:
                    if ld["rnm"]:
                        if txtin == "BACKSPACE":
                            ld["rnt"] = "".join(list(ld["rnt"])[:-1])
                            dprint("Listfiles: Bspace used")
                        elif txtin == "ENTER":
                            fd = loadbin(os.path.join(FILE_PATH, "GAMES", sep.join(ld["menu_slt"])))
                            savebin(os.path.join(FILE_PATH, "GAMES", sep.join(ld["menu_slt"][:-1]), ld["rnt"]), fd)
                            os.remove(os.path.join(FILE_PATH, "GAMES", sep.join(ld["menu_slt"])))
                            ld["menu_open"] = False
                            ld["menu_slt"] = None
                            ld["rnt"] = None
                            ld["rnm"] = False
                        else:
                            ld["rnt"] = f"{ld["rnt"]}{txtin}"
                    else:
                        ld["rnm"] = True
                        ld["rnt"] = ld["menu_slt"][-1]
            if dlt.collidepoint(mx, my):
                pygame.draw.rect(scrn, col[127], dlt)
                if mc[0]:
                    os.remove(os.path.join(FILE_PATH, "GAMES", sep.join(ld["menu_slt"])))
                    ld["menu_open"] = False
                    ld["menu_slt"] = None
            if cpy.collidepoint(mx, my):
                pygame.draw.rect(scrn, col[127], cpy)
                if mc[0]:
                    ld["menu_open"] = False
                    ld["menu_slt"] = None
                    ld["rnt"] = None
                    ld["rnm"] = False
                    if slc:
                        cpfl = slf, unpackedfiles
                    else:
                        cpfl = slf, list(unpackedfiles[slf])[0]
            if pst.collidepoint(mx, my):
                pygame.draw.rect(scrn, col[127], pst)
            
            txt2.render_to(scrn, (bx+5, by+5), "New File", col[255])
            txt2.render_to(scrn, (bx+5, by+5+ls), "New Folder", col[255])
            txt2.render_to(scrn, (bx+5, by+5+(ls*2)), ld["rnt"] if ld["rnm"] else "Rename", col[255])
            txt2.render_to(scrn, (bx+5, by+5+(ls*3)), "Delete", col[255])
            txt2.render_to(scrn, (bx+5, by+5+(ls*4)), "Copy", col[255])
            txt2.render_to(scrn, (bx+5, by+5+(ls*5)), "Paste", col[255 if cpfl != None else 127])
            
    path = path[:-1]
    if _parent:
        dprint("Listfiles: Parent subpro fi")
        dprint("Listfiles: Return Success")
        return scrn, files
        
    else:
        dprint("Listfiles: Child subpro fi")
        dprint(files)
        return scrn, unpackedfiles, _pos

def compile_files():
    
        global loading, max_dist, sort_order, files, screen_width

        max_dist = 0

        files = get_files(FILE_PATH+"Quickaccess")
        if debug:
            dprint(len(files))
        if len(screen) == 1:
            screen.append([None])
        file_infos = [(os.stat(os.path.join(FILE_PATH+"Quickaccess", files[i]))) for i in range (len(files))]

        file_btime = [file_infos[i].st_ctime for i in range (len(file_infos))]

        file_etime = [file_infos[i].st_mtime for i in range (len(file_infos))]

        if sort_order == "az":
            files = alph_list(files)
        elif sort_order == "za":
            files = alph_list(files)
            files.reverse()
        elif sort_order == "bn":
            files = sort(files, file_btime)
            files.reverse()
        elif sort_order == "bo":
            files = sort(files, file_btime)
        elif sort_order == "en":
            files = sort(files, file_etime)
            files.reverse()
        elif sort_order == "eo":
            files = sort(files, file_etime)


        file_infos = [(os.stat(FILE_PATH+"Quickaccess"+sep+files[i])) for i in range (len(files))]

        file_btime = [file_infos[i].st_ctime for i in range (len(file_infos))]

        file_etime = [file_infos[i].st_mtime for i in range (len(file_infos))]



        for i in range (len(files)):
            if len(screen[1]) <= i:
                screen[1].append(None)

            screen[1][i] = pygame.Surface((screen_width, (i*225)+300), pygame.SRCALPHA)
            name = files[i]

            file_info = os.stat(FILE_PATH+"Quickaccess"+sep+name)
            file_size = file_info.st_size
            file = string_to_list(load(os.path.join(FILE_PATH+"Quickaccess", name)), "\nbreak\n")



            file = string_to_list(load(FILE_PATH+"Quickaccess"+sep+name), "\nbreak\n")
            file[1] = replace_str(file[1], "")

            if len(file) == 1:
                file.append("Failed to get")

            if file[1] == "":
                file[1] = "Failed to get"

            if debug:
                dprint(name)
                dprint(file)

            file_disc = file[0]

            disc = warp(font[18], file_disc, screen_width-100)
            if len(disc) >= 4:
                txt = list(disc[3])
                txt[-1], txt[-2], txt[-3] = ".", ".", "."
                disc = [disc[0], disc[1], disc[2], "".join(txt)]


                

            toobig = True

            file_size_meas = ["B", "KB", "MB", "GB", "TB"]

            file_meas = 0

            while toobig:
                if file_size >= 1024:
                    file_size /= 1024
                    file_meas += 1
                else:
                    toobig = False
                if file_meas == len(file_size_meas):
                    toobig = False
            
            file_size = round(file_size*10)/10
            if str(file_size).__contains__(".0"):
                file_size = int(file_size)

            name = replace_str(name, file_type)

            btime = file_btime[i]
            etime = file_etime[i]
            dprint(etime-btime)
            btime = time.ctime(btime)
            etime = time.ctime(etime)
            if etime == btime:
                etime = "Never"



            pygame.draw.rect(screen[1][i], col[40], (15, math.floor(((i+3)*25)+(i*200)), screen_width-50, 200), 0, 25)
            dprint(screen_width)
            font[40].render_to(screen[1][i], (25, math.floor(((i+3)*25)+(i*200)+20)), name, fgcolor=col[255])
            font[18].render_to(screen[1][i], (25, math.floor(((i+3)*25)+(i*200)+65)), "Description:", fgcolor=col[255])
            if disc != []:
                for i2 in range (len(disc)):
                    font[14].render_to(screen[1][i], (25, math.floor(((i+3)*25)+(i*200)+((i2)*16)+85)), disc[i2], fgcolor=col[192])
            else:
                font[18].render_to(screen[1][i], (24, math.floor(((i+3)*25)+(i*200)+85)), "There is no description for this game", fgcolor=col[255])
            font[18].render_to(screen[1][i], (25, math.floor(((i+3)*25)+(i*200)+150)), "Details:", fgcolor=col[255])
            font[18].render_to(screen[1][i], (25, math.floor(((i+3)*25)+(i*200)+175)), "Size: "+str(file_size)+" "+file_size_meas[file_meas], fgcolor=col[255])
            font[18].render_to(screen[1][i], (250, math.floor(((i+3)*25)+(i*200)+150)), "Created: "+btime, fgcolor=col[255])
            font[18].render_to(screen[1][i], (252, math.floor(((i+3)*25)+(i*200)+175)), "Last Edited: "+etime, fgcolor=col[255])
            font[18].render_to(screen[1][i], (600, math.floor(((i+3)*25)+(i*200)+150)), "Type: "+replace_str(file[1], "\n"), fgcolor=col[255])

            max_dist = (((i+3)*25)+(i*200)+150+screen_height) - 1050
        screen[0][1] = (pygame.Surface((screen_width, (len(files)*300)+200), pygame.SRCALPHA))
        for i in range (len(files)):
            screen[0][1].blit(screen[1][i], (0, math.floor(i)))
        loading = False

        return(len(files))

def button(text, font, x, y, butt_col, select_col, text_col, width, height, id, corner_round):
    """
    Draws a button on the screen and checks for mouse hover/click.
    """
    global button_pushed_states, mx, my, mc
    
    try:
        screen = pygame.display.get_surface() 
    except:
        dprint("Error: Pygame screen surface not found.")
        return
    
    button_rect = pygame.Rect(x, y, width, height)
    action = False
    current_col = butt_col

    if button_rect.collidepoint((mx, my)):
        current_col = select_col
        
        if mc[0] == 1:
            action = True
            
            if id not in button_pushed_states or button_pushed_states[id] == False:
                 button_pushed_states[id] = True 
    
    if id in button_pushed_states and button_pushed_states[id] == True and not action:
          button_pushed_states[id] = False

    sx, sy, sw, sh = button_rect
    if current_col == select_col:
        pygame.draw.rect(screen, select_col, (sx-2, sy-2, sw+4, sh+4), 0, corner_round)
    pygame.draw.rect(screen, butt_col, button_rect, 0, corner_round)



    try:
        rendered = font.render(text, fgcolor=text_col)
    except TypeError:
        rendered = font.render(text, True, text_col)

    if isinstance(rendered, tuple):
        text_surface, text_rect = rendered[0], rendered[1]
        try:
            text_rect.center = button_rect.center
        except Exception:
            text_rect = text_surface.get_rect(center=button_rect.center)
    else:
        text_surface = rendered
        text_rect = text_surface.get_rect(center=button_rect.center)

    screen.blit(text_surface, text_rect)

def get_butt_pushed(id):
    """
    Checks if a specific button was clicked in the last frame.
    """
    global button_pushed_states
    
    return button_pushed_states.get(id, False)

def tick_new():

    global typeselect, file_type, auto, auto_halt, mc, auto_launch, nxtc, file_count, recent_push, gtype, ntargcol, charpressed, new_menu, newname, name_edit, framen, disc_edit, newdisc, framene, framede, ani_x, ani_y, nbpos, dbpos

    menu_x, menu_y = 50, (screen_height//2)-new_animation
    menu_w, menu_h = (screen_width-50)-menu_x, ((screen_height//2)+new_animation)-menu_y

    name_def_w = menu_w-66
    
    ani_x, ani_y = font[25].get_rect("x").size
    
    exitRect = pygame.Rect(((menu_x+menu_w)-15, menu_y, 15, 18))
    
    pygame.draw.rect(screen[0][0], col[ntargcol], exitRect, 0, 0, 0, 3, 7, 0)
    font[25].render_to(screen[0][0], ((menu_x+menu_w)-15, menu_y), 'x', fgcolor=col[255])
    
    #Text detection for Description
    
    if exitRect.collidepoint((mx, my)):
        if ntargcol != 128:
            ntargcol += 8
    
        if mc[0]:
            new_menu = False
            name_edit = False
            disc_edit = False
    
    else:
        if ntargcol != 64:
            ntargcol -= 8
        
    if mc[0]:
        name_edit = False
        disc_edit = False
    
    if name_edit == disc_edit == False and charpressed == "ESCAPE":
        new_menu = False
    
    font[25].render_to(screen[0][0], (menu_x+2, menu_y+2), "New Game", fgcolor=col[255])
    
    if disc_edit:
        if charpressed == "ESCAPE":
            disc_edit = False
            
        if disc_edit:
            name_edit = False
            newdiscbpos = edit_str(newdisc, dbpos)
            charpressed = ""
            newdisc = newdiscbpos[0]
            dbpos = newdiscbpos[1]
            framede += 1

        else:
            framede = 0
    
    #Text processing for name

    if inrange(mx, menu_x+35, (menu_x+menu_w)-35) and inrange(my, menu_y+180, menu_y+280):
        pygame.draw.rect(screen[0][0], col[128], (menu_x+33, menu_y+178, menu_w-66, 104), 0, 5)
        if mc[0]:
            disc_edit = True
    pygame.draw.rect(screen[0][0], col[48], (menu_x+35, menu_y+180, menu_w-70, 100), 0, 5)

    if name_edit:
        if charpressed == "ESCAPE":
            name_edit = False
            
        if name_edit:
            disc_edit = False
            newnamebpos = edit_str(newname, nbpos)
            charpressed = ""
            newname = newnamebpos[0]
            nbpos = newnamebpos[1]
            framene += 1

        else:
            framene = 0

    if list(newname+"_")[0] == " ":
        newname = "".join(list(newname)[i+1] for i in range (len(list(newname))-1))
        nbpos -= 1
        
    # Imma be honest i have no clue whats happening here
    
    # Future self making an extra note, me neither. I just needed some code for a texbox to rename files bro, what is this?

    newname2 = newname if newname != "" else " "

    newname3 = newname2
    newname2 = newname2 if list(newname2)[-1] != " " else "".join([list(newname2)[i] for i in range (len(list(newname2))-1)])

    while newname2 != newname3:
        newname3 = newname2
        if newname2 != "":
            newname2 = newname2 if list(newname2)[-1] != " " else "".join([list(newname2)[i] for i in range (len(list(newname2))-1)])
        else:
            newname3 = newname2

    #post-processing

    precursname = list_to_string(crop_lst(list(newname2), nbpos, False), "")
    postcursname = list_to_string(crop_lst(list(newname2), nbpos, True), "")

    precursdisc = list_to_string(crop_lst(list(newdisc), dbpos, False), "")
    postcursdisc = list_to_string(crop_lst(list(newdisc), dbpos, True), "")
    
    #rendering
    
    if get_text_width(newname, 50) <= name_def_w:
        if inrange(mx, menu_x+35, menu_x+name_def_w+35) and inrange(my, menu_y+80, menu_y+130):
            pygame.draw.rect(screen[0][0], col[128], (menu_x+33, menu_y+78, name_def_w+4, 54), 0, 5)
            if mc[0]:
                name_edit = True
        pygame.draw.rect(screen[0][0], col[48], (menu_x+35, menu_y+80, name_def_w, 50), 0, 5)
    else:
        if inrange(mx, menu_x+35, menu_x+48+get_text_width(newname, 50)) and inrange(my, menu_y+80, menu_y+130):
            pygame.draw.rect(screen[0][0], col[128], (menu_x+33, menu_y+78, get_text_width(newname, 50)+16, 54), 0, 5)
            if mc[0]:
                name_edit = True
        pygame.draw.rect(screen[0][0], col[48], (menu_x+35, menu_y+80, get_text_width(newname, 50)+12, 50), 0, 5)


    if (framene/60)*2 % 1 <= 0.5 and name_edit:
        pygame.draw.rect(screen[0][0], col[255], (menu_x+38+get_text_width(precursname, 50), menu_y+85, 2, 40))

    if (framede/60)*2 % 1 <= 0.5 and disc_edit:
        pygame.draw.rect(screen[0][0], col[255], (menu_x+38+get_text_width(precursdisc, 15), menu_y+182, 1, 11))


    font[25].render_to(screen[0][0], (menu_x+35, menu_y+50), "Name", fgcolor=col[255])
    
    font[50].render_to(screen[0][0], (menu_x+37, menu_y+82), precursname+postcursname, fgcolor=col[255])

    font[25].render_to(screen[0][0], (menu_x+35, menu_y+148), "Description", fgcolor=col[255])

    desc_text = precursdisc + postcursdisc
    max_desc_width = menu_w - 70 - 4

    desc_lines = []
    for p in desc_text.split("\n"):
        if p == "":
            desc_lines.append("")
        else:
            desc_lines.extend(warp(font[15], p, max_desc_width))

    line_h = 16
    max_lines = 100 // line_h
    for idx, line in enumerate(desc_lines[:max_lines]):
        font[15].render_to(screen[0][0], (menu_x+37, menu_y+180 + idx * line_h), line, fgcolor=col[255])

    if (framede/60)*2 % 1 <= 0.5 and disc_edit:
        prec_text = precursdisc
        prec_lines = []
        for p in prec_text.split("\n"):
            if p == "":
                prec_lines.append("")
            else:
                prec_lines.extend(warp(font[15], p, max_desc_width))

        if prec_lines:
            caret_line = len(prec_lines) - 1
            caret_x = get_text_width(prec_lines[-1], 15)
        else:
            caret_line = 0
            caret_x = 0

        pygame.draw.rect(screen[0][0], col[255], (menu_x+38+caret_x, menu_y+182 + caret_line * line_h, 1, 11))
    
    if not auto_halt:
        auto = "X" if auto_launch else ""

    button(auto, font[10], (menu_x+menu_w)-25, menu_y+25, col[48], col[128], col[255], 20, 20, 9999, 5)
    if get_butt_pushed(9999):
        if not auto_halt:
            auto_launch = not auto_launch
        auto_halt = True
    if not mc[0]:
        auto_halt = False
    
    font[18].render_to(screen[0][0], (((menu_x+menu_w)-25)-get_text_width("Immediatley load into editor: ", 18), menu_y+25), "Immediatley load into editor:", fgcolor=col[255])
        
    try:
        typeselect.draw(screen[0][0])
    except NameError:
        typeselect = pyselect.dropdown(types, font[25], menu_x+130, menu_y+10, 320, 60, col[48], col[128], col[255], col[16], col[32], 10, 10, False, False)

    if not mc[0]:
        recent_push = False

    if get_butt_pushed(0) and not recent_push:
        gtype = types[(types.index(gtype)+1) % (len(types))]
        recent_push = True

    button("CREATE!", font[40], ((menu_x+menu_w)-10)-get_text_width("CREATE!", 40), (menu_y+menu_h)-50, (32, 192, 32), col[128], col[255], get_text_width("CREATE!", 40)+5, 45, 1, 5)

    if get_butt_pushed(1):
        if newname == "":
            newname = "game"+str(file_count+1)
        dprint(f"Creating new game called {newname+file_type}")
        save(os.path.join(FILE_PATH, "Quickaccess", newname+file_type), list_to_string([newdisc, gtype], "\nbreak\n"))
        os.mkdir(os.path.join(FILE_PATH, "GAMES", newname))
        if auto_launch:
            global targ_item, run
            targ_item = newname
            run = False
        newname = ""
        newdisc = ""
        new_menu = False
        file_count = compile_files()


# Initialisations
if __name__ == "__main__":
    pygame.init()
    pygame.freetype.init()

    button_pushed_states = {}

    targ_item = ""

    nxtc = 0

    auto = ""

    auto_halt = False

    auto_launch = False

    recent_push = False

    gtype = "2D"

    types = ["2D"]

    nbpos = 0
    dbpos = 0

    col = [(i, i, i) for i in range (256)]

    font = [pygame.freetype.SysFont("Arial", size=i+1) for i in range (999)] # Create as many fonts as you could possibly need

    dprint(f"Debug: {debug}")

    screen_width = 1050
    screen_height = 750

    screen = []
    screen.append([None, None])

    screen[0][0] = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE) #why did i do this

    pygame.display.set_caption("Speaker Engine")

    icon = pygame.Surface((get_text_width("</>", 24), get_text_width("</>", 24)))

    icon.fill((col[243]))
    pygame.draw.rect(icon, col[0], (0, 0, icon.get_width(), icon.get_height()), 0, int(icon.get_width()/3.5))
    pygame.draw.rect(icon, col[48], (3, 3, icon.get_width()-6, icon.get_height()-6), 0, int(icon.get_width()/3.5))
    font[20].render_to(icon, ((get_text_width("</>", 24)//2)-(get_text_width("</>", 20)//2), (icon.get_height()//2)-10), "</>", fgcolor=(255, 127, 0))

    pygame.display.set_icon(icon)

    config = []

    try:
        config = string_to_list(load("Config"), "\nbreak\n")
        if config[0] == "":
            raise Exception("Config corrupted")
    except:
        config = ["az"]
        save("Config", list_to_string(config, "\nbreak\n"))

    sort_order = config[0]

    screenpos = 0
    screenpossmooth = 0.5
    screenspd = 0

    file_size_meas = ["Bytes", "KB", "MB", "GB", "TB"]

    sort_options = ["Alphabetical", "Reverse Alphabetical", "Recent", "Untouched", "Newest", "Oldest"]

    sort_order_lst = ["az", "za", "en", "eo", "bn", "bo"]

    sort_ord_opt = {
        sort_options[i]:sort_order_lst[i] for i in range (len(sort_options))
    }
    
    sort_ord_opt_invrt = {
            sort_order_lst[i]:sort_options[i] for i in range (len(sort_options))
        }

    max_dist = 0

    run = True

    framen = 0
    
    fs = False

    file_count = 0

    ntargcol = 64

    new_menu = False

    new_ani_fin = False

    clock = pygame.time.Clock()

    fps = 0

    new_animation = 0
    new_ani_spd = 0.5
    
    charpressed = ""

    newname = ""
    newdisc = ""
    name_edit = False
    disc_edit = False

    frameb = None
    framene = 0
    framede = 0

    del_menu = False


    dark = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    dark.fill((0, 0, 0, 160))
    
    sort_halt = False

    loading = False

    nb = pyselect.button("+", font[75], screen_width-75, 0, 75, 75, col[64], col[128], col[255], 5)
    
    sodo = pyselect.dropdown(sort_options, font[25], screen_width-350, 10, 250, 55, col[64], col[128], col[255], col[16], col[48], 5, 5, False, False, sort_ord_opt_invrt[sort_order])

    framenl = []
    
    file_count = compile_files()
    top = pygame.Surface((screen_width, 86))
    for y in range (17):
        color = round(32 - y)
        pygame.draw.rect(top, (color, color, color), (0, 75 + y, screen_width, 1))
        
        
# Main Loop
if __name__ == "__main__":
    while run:

        psw, psh = screen_width, screen_height
        screen_width, screen_height = screen[0][0].get_size()
        if (psw, psh) != (screen_width, screen_height):
            file_count = compile_files()
            top = pygame.Surface((screen_width, 86))
            for y in range (17):
                color = round(32 - y)
                pygame.draw.rect(top, (color, color, color), (0, 75 + y, screen_width, 1))
                
            dark = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            dark.fill((0, 0, 0, 160))

        nb.x, nb.y = screen_width-75, 0
        sodo.x, sodo.y = screen_width-350, 10

        screen[0][0].fill(col[24])

        charpressed = ""

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            if e.type == pygame.TEXTINPUT:
                charpressed = e.text
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    charpressed = "ESCAPE"
                if e.key == pygame.K_BACKSPACE:
                    charpressed = "BACKSPACE"
                if e.key == pygame.K_LEFT:
                    charpressed = "LEFT"
                if e.key == pygame.K_RIGHT:
                    charpressed = "RIGHT"
                if e.key == pygame.K_F2:
                    debug = not debug
                if e.key == pygame.K_F11:
                    if fs:
                        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        fs = False
                    else:
                        pygame.display.set_mode((0, 0), pygame.RESIZABLE)
                        fs = True
                        
            if e.type == pygame.MOUSEWHEEL:
                screenspd -= e.y*15

        dprint(f"Keypressed: {charpressed if charpressed != "" else "None"}")

        mx, my = pygame.mouse.get_pos()
        mc = pygame.mouse.get_pressed()

        
        if skip:
            if charpressed == "BACKSPACE":
                skip = False
            else:
                if framen > 1:
                    skip = False
                    run = False
                    try:
                        targ_item = "".join(list(get_files(os.path.join(FILE_PATH, "Quickaccess"))[0])[0:-5])
                    except IndexError:
                        del targ_item
                        run = True

        if not (new_menu or del_menu) and charpressed == "ESCAPE":
            run = False

        screen[0][0].blit(top, (0, 0))

        screenspd *= screenpossmooth
        screenpos += screenspd

        if screenpos > max_dist:
            screenspd = 0
            screenpos = max_dist
        if screenpos < 0:
            screenspd = 0
            screenpos = 0

        if (file_count == 0 and framen > 15):
            font[40].render_to(screen[0][0], (screen_width//2 - 225, 75), "You dont have any Games yet!", fgcolor=col[255])
        elif loading:
            font[25].render_to(screen[0][0], (25, 90), "Loading...", fgcolor=col[255])


        screen[0][0].blit(screen[0][1], (0, 0 - screenpos))

        for i in range (file_count):
            if inrange(-40, math.floor((((i+3)*25)+(i*200)+135) - screenpos), screen_height):
                dprint(file_count)
                button("Delete", font[18], screen_width - 160, math.floor((((i+3)*25)+(i*200)+135) - screenpos), (192, 0, 0), (255, 32, 32), (255, 255, 255), 100, 40, i+2, 5)
                if get_butt_pushed(i+2) and int(((new_animation/(screen_height//4)))*50) == 0:
                    del_item = files[i]
                    dprint(list(del_item)[:-5])
                    del_item = "".join(list(del_item)[:-5])
                    del_menu = True
            if inrange(-40, math.floor((((i+3)*25)+(i*200)+85) - screenpos), screen_height):
                button("Open", font[18], screen_width - 160, math.floor((((i+3)*25)+(i*200)+85) - screenpos), (0, 192, 0), (32, 255, 32), (255, 255, 255), 100, 40, i+99999, 5)
                if get_butt_pushed(i+99999) and int(((new_animation/(screen_height//4)))*50) == 0:
                    del_item = files[i]
                    dprint(list(del_item)[:-5])
                    targ_item = "".join(list(del_item)[:-5])
                    run = False

        if del_menu:
            pygame.Surface.blit(screen[0][0], dark, (0, 0))
            pygame.draw.rect(screen[0][0], col[64], (100, 100, screen_width-200, screen_height-200), 0, 25)
            font[40].render_to(screen[0][0], (screen_width//2 - (get_text_width("Are you sure you want to delete "+del_item+"?", 40)//2), (screen_height//2)-100), "Are you sure you want to delete "+del_item+"?", fgcolor=col[255])
            button("No", font[30], (screen_width//2)-150, (screen_height//2), (0, 192, 0), (32, 255, 32), (255, 255, 255), 100, 50, 999999, 5)
            button("Yes", font[30], (screen_width//2)+50, (screen_height//2), (192, 0, 0), (255, 32, 32), (255, 255, 255), 100, 50, 999998, 5)
            if get_butt_pushed(999999):
                del_menu = False
            if get_butt_pushed(999998):
                del_menu = False
                os.remove(os.path.join(FILE_PATH, "Quickaccess", del_item+file_type))
                file_count = compile_files()
                loading = True
            if charpressed == "ESCAPE":
                del_menu = False

        pygame.draw.rect(screen[0][0], col[32], (0, 0, screen_width, 75))

        font[50].render_to(screen[0][0], (0, 12), f"SPEAKER ENGINE {("FPS: "+str(fps)) if debug else ""}", fgcolor=col[255])

        sodo.draw(screen[0][0])

        if not mc[0]:
            sort_halt = False
            
        nb.draw(screen[0][0])
        if nb.was_clicked():
            new_menu = True


        if new_menu:
            screen[0][0].blit(dark, (0, 0))
            if new_animation < screen_height//4:
                new_animation += new_ani_spd
                new_ani_spd *= 1.125
            if new_animation+(new_ani_spd*0) > screen_height//4:
                new_ani_fin = True
        else:
            new_ani_fin = False
            if new_ani_spd >= 0.5:
                new_ani_spd /= 1.125
                new_animation -= new_ani_spd

        if not new_ani_fin:
            if charpressed == "UP":
                screenspd -= 15
            if charpressed == "DOWN":
                screenspd += 15



        if new_animation >= 0.0625:

            for a in range (2):
                
                b = 10 if a == 0 else 3
                i = a*8

                na = not a
                ni = na*8

                center_col = int(((new_animation/(screen_height//4)))*50)
                if a == 0:
                    center_col = 50
                
                pygame.draw.rect(screen[0][0], col[center_col+(2*i)], (42+i, ((screen_height//2)-new_animation)-ni, (screen_width-100)+(ni*2), (new_animation*2)+(2*ni)), 0, b)
        if new_ani_fin:
            tick_new()
            

        loading = sort_ord_opt[sodo.get_selected()] != sort_order
        sort_order = sort_ord_opt[sodo.get_selected()]
        config[0] = sort_order

        if loading:
            dprint("Refreshing")
            loading = False
            file_count = compile_files()

        fps = int(clock.get_fps())
        fps = fps if fps != 0 else 1

        clock.tick(60)
        pygame.display.update()
        framen += 1

        framenl.append(fps)

        if framen % (60) == 0:
            dprint(config)
            dprint(list_to_string(config, "\nbreak\n"))

            save("Config", list_to_string(config, "\nbreak\n"))

            dprint(string_to_list(load("Config"), "\nbreak\n"))
            dprint("saved")
            if framen % 3600 == 0:
                file_count = compile_files()
                dprint("Reloaded Page")


# Editors
if __name__ == "__main__":
    if targ_item != "":
        item = string_to_list(load(f"{FILE_PATH}Quickaccess{sep}{targ_item}{file_type}"), "\nbreak\n")
    else:
        pygame.quit()
        exit()

    dark = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    dark.fill((0, 0, 0, 64))
    framen = 0

    screen[0][0].fill(col[0])
    font[25].render_to(screen[0][0], ((screen_width//2)-(get_text_width("Loading...", 25, "Arial")//2), (screen_height//2)-(25)), "Loading...", col[255])
    font[25].render_to(screen[0][0], ((screen_width//2)-(get_text_width("Do not close", 25, "Arial")//2), (screen_height//2)+(25)), "Do not close", col[255])
    pygame.display.update()
    game_name = targ_item

    q = multiprocessing.Queue()
    scan = multiprocessing.Process(target=recursive_scan, args=(sep, os.path.join(FILE_PATH, "GAMES", game_name), q))
    scan.start()

    match item[1]:
        case "2D":
            run = True
            files = {}
            while run:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        exit()
                if not scan.is_alive():
                    files = q.get()
                    scan.join()
                    dprint(files)
                    run = False

            run = True
            del screen
            pygame.quit()
            pygame.init()
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            pygame.display.set_icon(icon)
            pygame.display.set_caption(f"SPEAKER ENGINE - {game_name}")
            sw, sh = screen.get_size()
            
            font = [freetype.SysFont("Arial", s) for s in range (200)]

            width = 3

            fs = False
            framen = 0
            uhold = False
            bgrs = False
            exitbool = False

            update_rate = 1
            prevfiles = files
            ms = 0
            
            edit = editor(0.2, (sw-(2*(sw//5)), sh), font[20])

            kp = {pygame.K_BACKSPACE: 0, pygame.K_RETURN: 0, pygame.K_RIGHT: 0, pygame.K_LEFT: 0, pygame.K_UP: 0, pygame.K_DOWN: 0}

            while run:
                txtin = ""
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        exitbool = True
                    if e.type == pygame.TEXTINPUT:
                        txtin = e.text
                    if e.type == pygame.KEYDOWN:
                        if e.key in kp:
                            kp[e.key] = 1
                    if e.type == pygame.KEYUP:
                        if e.key in kp:
                            kp[e.key] = 0
                            
                    if e.type == pygame.MOUSEWHEEL:
                        ms = e.y
                        
                for k, v in kp.items():
                    if v > 0:
                        kp[k] += 1
                    if v > 30 or v == 1:
                        if k == pygame.K_BACKSPACE: txtin = "BACKSPACE"
                        if k == pygame.K_RETURN: txtin = "RETURN"
                        if k == pygame.K_RIGHT: txtin = "RIGHT"
                        if k == pygame.K_LEFT: txtin = "LEFT"
                        if k == pygame.K_UP: txtin = "RIGHT"
                        if k == pygame.K_DOWN: txtin = "DOWN"
                    
                if (sw, sh) != screen.get_size():
                    sw, sh = screen.get_size()
                    edit.screen_size_x = sw-(2*(sw//5))
                    edit.screen_size_y = sh

                if framen % (60*update_rate) == (60*update_rate)/2 and not (bgrs or exitbool):
                    dprint("Updating files")
                    bgrs = True
                    q = multiprocessing.Queue()
                    scan = multiprocessing.Process(target=recursive_scan, args=(sep, os.path.join(FILE_PATH, "GAMES", game_name), q, files))
                    scan.start()
                sw, sh = screen.get_size()
                screen.fill(col[16])

                mx, my = pygame.mouse.get_pos()
                mc = list(pygame.mouse.get_pressed())
                
                edit.code_update(txtin, ms)
                
                if uhold and mc[0]:
                    mc[0] = False
                elif mc[0]:
                    uhold = True
                else:
                    uhold = False
                
                dprint(mx, my)
                
                if prevfiles != files or (inrange(width, my, width+((sh//2)-4)) and inrange(width, mx, width+(sw//5-(width*2)))) or ld["menu_open"] or framen == 0:
                    filesurf, files = listfiles(game_name, files, txtin, (sw//5-(width*2), (sh//2)-4), (sw, sh), (width, width), mx, my, mc)
                    final_load = 2
                elif final_load == 2:
                    final_load = 1
                    
                if final_load == 1:
                    filesurf, files = listfiles(game_name, files, txtin, (sw//5-(width*2), (sh//2)-4), (sw, sh), (width, width), mx, my, mc)
                    final_load = 0
                    
                if bgrs and not q.empty():
                    final_load = 1
                
                pygame.draw.rect(screen, col[32], (0, 0, sw//5, sh))
                pygame.draw.rect(screen, col[128], (0, 0, sw//5, (sh//2)+(width//2)), width)
                pygame.draw.rect(screen, col[128], (0, (sh//2)-1, sw//5, (sh//2)+(width//2)), width)
                
                screen.blit(filesurf, (0, 0))
                
                edit.draw(screen, ((sw//5)-4, 0))

                if framen != 0:
                    pygame.display.update()
                clock.tick(60)
                fps = clock.get_fps()
                pygame.display.set_caption(f"SPEAKER ENGINE - {game_name} - {round(fps)}")


                if bgrs and not q.empty():
                    dprint("Filescan Finished")
                    bgrs = False
                    prevfiles = files
                    files = q.get()
                    scan.join()
                framen += 1
                if not (not (exitbool) or bgrs):
                    run = False
        case _:
            raise Exception("Bad game type")
        
pygame.quit()