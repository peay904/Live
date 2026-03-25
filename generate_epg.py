#!/usr/bin/env python3
"""
Generate XMLTV EPG with rolling 24-hour programme entries.
Run daily via GitHub Actions to keep EPG current and avoid layout crashes.
"""

from datetime import datetime, timedelta, timezone
import xml.etree.ElementTree as ET

DAYS_AHEAD = 3
OUTPUT_FILE = "epg.xml"

CHANNELS = [
    {"id": "Maui.ip",        "name": "Lahaina Maui Live",                  "title": "Lahaina Maui Live Stream 24/7"},
    {"id": "Bald.ip",        "name": "Bald Eagle's Nest Live",             "title": "Bald Eagle's Nest Live Stream 24/7"},
    {"id": "Tongass.ip",     "name": "Tongass National Forest Live",       "title": "Tongass National Forest Live Stream 24/7"},
    {"id": "Aurora.ip",      "name": "Aurora Borealis Live",               "title": "Aurora Borealis Live Stream 24/7"},
    {"id": "Reef.ip",        "name": "Underwater Reef Cam Live",           "title": "Underwater Reef Live Stream 24/7"},
    {"id": "Pup.ip",         "name": "Puppy Cam Live",                     "title": "Puppy Cam Live Stream 24/7"},
    {"id": "Elephant.ip",    "name": "Africam: Elephant Park Live",        "title": "Africam: Elephant Park Live Stream 24/7"},
    {"id": "Waterhole.ip",   "name": "Africam: Tau Waterhole Live",        "title": "Africam: Tau Waterhole Live Stream 24/7"},
    {"id": "Joe.ip",         "name": "Sloppy Joe's Bar - Key West Live",   "title": "Sloppy Joe's Bar Live Stream 24/7"},
    {"id": "Inn.ip",         "name": "Sunset Inn, Marathon FL Live",       "title": "Sunset Inn Live Stream 24/7"},
    {"id": "car.ip",         "name": "Mississuaga Car Wash Live",          "title": "Mississuaga Car Wash Live Stream 24/7"},
    {"id": "Skate.ip",       "name": "Nova Gorica skatepark Live",         "title": "Nova Gorica skatepark Live Stream 24/7"},
    {"id": "cavallino.ip",   "name": "Cavallino-Treporti Live",            "title": "Cavallino-Treporti Live Stream 24/7"},
    {"id": "Pigs.ip",        "name": "Costa Mesa pigs Live",               "title": "Costa Mesa pigs Live Stream 24/7"},
    {"id": "pickleball.ip",  "name": "Head Island pickleball Live",        "title": "Head Island pickleball Live Stream 24/7"},
    {"id": "archery.ip",     "name": "Dead On Archery Live",               "title": "Dead On Archery Live Stream 24/7"},
    {"id": "outdog.ip",      "name": "Doggy Day Care Outdoor",             "title": "Doggy Day Care Outdoor Live Stream 24/7"},
    {"id": "indog.ip",       "name": "Doggy Day Care Indoor",              "title": "Doggy Day Care Indoor Live Stream 24/7"},
    {"id": "laudbts.ip",     "name": "Lauderdale-By-The-Sea Live",        "title": "Lauderdale-By-The-Sea Live Stream 24/7"},
    {"id": "ccafe.ip",       "name": "Cat Cafe Live",                      "title": "Cat Cafe Live Stream 24/7"},
    {"id": "space.ip",       "name": "Live From Space",                    "title": "Earth From Space Live Stream 24/7"},
]

def generate_epg():
    tv = ET.Element("tv")

    for ch in CHANNELS:
        channel = ET.SubElement(tv, "channel", id=ch["id"])
        ET.SubElement(channel, "display-name").text = ch["name"]

    now = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

    for ch in CHANNELS:
        for day in range(DAYS_AHEAD):
            start = now + timedelta(days=day)
            stop  = start + timedelta(hours=24)
            prog  = ET.SubElement(tv, "programme", attrib={
                "start":   start.strftime("%Y%m%d%H%M%S +0000"),
                "stop":    stop.strftime("%Y%m%d%H%M%S +0000"),
                "channel": ch["id"],
            })
            ET.SubElement(prog, "title", lang="en").text = ch["title"]
            ET.SubElement(prog, "desc",  lang="en").text = "This programming runs continuously without interruption."

    tree = ET.ElementTree(tv)
    ET.indent(tree, space="  ")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(f, encoding="unicode", xml_declaration=False)

    print(f"Generated {OUTPUT_FILE}: {DAYS_AHEAD} days x {len(CHANNELS)} channels = {DAYS_AHEAD * len(CHANNELS)} entries.")

if __name__ == "__main__":
    generate_epg()
