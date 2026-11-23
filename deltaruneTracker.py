import requests as web
import subprocess, time, json

def checkDeltarune():
    site = web.get("https://www.deltarune.com/7b")

    text = site.text

    text = text.split("\n")

    newtext = [line for line in text if "<span class=\"font-mono" in line]

    tmp = list(newtext[0])

    idx = tmp.index("🗺")

    tmp.pop(idx)

    newtext[0] = "".join(tmp)
    
    cropbars = ["".join(list(i)[44:63]) for i in newtext]
    
    percent = [bar.count("▓")/20 for bar in cropbars]
    
    return percent

def notify(urgency, timeout, title, subtitle):
    """
    Args:
        urgency: Low, Normal, Critical
        
        timeout: Milliseconds
        
        title: Title of notification
        
        subtitle: Message of notification
    """
    
    subprocess.run(["notify-send",
            "-u", str(urgency),
            "-t", str(timeout),
            str(title), str(subtitle)])

def save(file, contents):
    with open(file, mode="w", encoding="utf8") as f:
        f.write(contents)
    f.close()

dr = checkDeltarune()

dr = json.dumps(dr)

save("data.json", dr)

notify("Normal", 10000, "Deltarune scanner active", "Scanning deltarune for 7B updates every 10 seconds")

while True:
    time.sleep(10)