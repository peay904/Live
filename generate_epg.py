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
    {"id": "Skate.ip",       "name": "Nova Gorica skatepark Live",         "title": "Nova Gorica skatepark Live Stream 24/7"},
    {"id": "Pigs.ip",        "name": "Costa Mesa pigs Live",               "title": "Costa Mesa pigs Live Stream 24/7"},
    {"id": "pickleball.ip",  "name": "Head Island pickleball Live",        "title": "Head Island pickleball Live Stream 24/7"},
    {"id": "lion.ip",        "name": "Smithsonian Lion Cam",               "title": "Smithsonian Lion Cam Live Stream 24/7"},
    {"id": "penguin.ip",     "name": "Penguins Live Cam",                  "title": "Penguins Live Stream 24/7"},
    {"id": "tiger.ip",       "name": "Live Tiger Cam",                     "title": "Tigers Live Stream 24/7"},
    {"id": "smpark.ip",      "name": "Santa Monica-Pacific Park",          "title": "Santa Monica-Pacific Park Live Stream 24/7"},
    {"id": "smpier.ip",      "name": "Santa Monica Pier Live",             "title": "Santa Monica Pier Live Stream 24/7"},
    {"id": "bay.ip",         "name": "Bayfront Park, Miami Live",          "title": "Bayfront Park, Miami Live Stream 24/7"},
    {"id": "cedar.ip",       "name": "Cedar Key Live",                     "title": "Cedar Key Live Stream 24/7"},
    {"id": "butterfly.ip",   "name": "Butterfly House Live",               "title": "Butterfly House Live Stream 24/7"},
    {"id": "jelly.ip",       "name": "Moon Jellies Live",                  "title": "Moon Jellies Live Stream 24/7"},
    {"id": "petes.ip",       "name": "Peg Leg Petes Live",                 "title": "Peg Leg Petes Live Stream 24/7"},
    {"id": "sharkbeach.ip",  "name": "Sharkys Beach Cam Live",             "title": "Sharkys Beach Cam Live Stream 24/7"},
    {"id": "sharkdeck.ip",   "name": "Sharkys Deck Cam Live",              "title": "Sharkys Deck Cam Live Stream 24/7"},
    {"id": "schooners.ip",   "name": "Schooners Bar Live",                 "title": "Schooners Bar Live Stream 24/7"},
    {"id": "wharf.ip",       "name": "Schooners Wharf Live",               "title": "Schooners Wharf Live Stream 24/7"},
    {"id": "willy.ip",       "name": "Pineapple Willys Live",              "title": "Pineapple Willys Live Stream 24/7"},
    {"id": "fish.ip",        "name": "North Carolina Fishing Pier Live",   "title": "North Carolina Fishing Pier Live Stream 24/7"},
    {"id": "oban.ip",        "name": "Oban,Scotland Pier Live",            "title": "Oban,Scotland Pier Live Stream 24/7"},
    {"id": "ferry.ip",       "name": "Windermere Ferry Live",              "title": "Windermere Ferry Live Stream 24/7"},
    {"id": "broads.ip",      "name": "Norfolk Broads-England Live",        "title": "Norfolk Broads-England Live Stream 24/7"},
    {"id": "windjammer.ip",  "name": "Windjammer Beach Club Live",         "title": "Windjammer Beach Club Live Stream 24/7"},
    {"id": "dead.ip",        "name": "Dead Dog Saloon Live",               "title": "Dead Dog Saloon Live Stream 24/7"},
    {"id": "tydz.ip",        "name": "RipTydz Oceanfront Grille Live",     "title": "RipTydz Oceanfront Grille Live Stream 24/7"},
    {"id": "merry.ip",       "name": "Merrymoor Inn Live",                 "title": "Merrymoor Inn Live Stream 24/7"},
    {"id": "robin.ip",       "name": "Robinhoods Bay Live",                "title": "Robinhoods Bay Live Stream 24/7"},
    {"id": "golazo.ip",      "name": "Golazo Network",                     "title": "Golazo Network"},
    {"id": "bali.ip",        "name": "Bali Elephant Cam Live",             "title": "Bali Elephant Cam Live Stream 24/7"},
    {"id": "wine.ip",        "name": "Gourmet Vinegar & Wines Warehouse",  "title": "Gourmet Vinegar & Wines Warehouse"},
    {"id": "box.ip",         "name": "Gourmet Vinegar & Wines Bag in Box", "title": "Gourmet Vinegar & Wines Bag in a Box"},
    {"id": "pack.ip",        "name": "Gourmet Vinegar & Wines Packaging",  "title": "Gourmet Vinegar & Wines Packaging"},
    {"id": "german.ip",      "name": "Großröhrsdorf - Bretnig-Hauswalde",  "title": "Großröhrsdorf - Bretnig-Hauswalde"},
    {"id": "tbd.ip",         "name": "tbd",                                "title": "tbd"},
    {"id": "rocks.ip",       "name": "Red Rocks",                          "title": "Red Rocks"},
    {"id": "tip.ip",         "name": "Black Tip Reef",                     "title": "Black Tip Reef"},
    {"id": "pebble.ip",      "name": "Pebble Beach 18th Green",            "title": "Pebble Beach 18th Green"},
    {"id": "seals.ip",       "name": "Piedras Blancas Elephant Seals",     "title": "Piedras Blancas Elephant Seals"},
    {"id": "yosemite.ip",    "name": "Yosemite Falls",                     "title": "Yosemite Falls"},
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
