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
    {"id": "outdog.ip",      "name": "Doggy Day Care Outdoor",             "title": "Doggy Day Care Outdoor Live Stream 24/7"},
    {"id": "indog.ip",       "name": "Doggy Day Care Indoor",              "title": "Doggy Day Care Indoor Live Stream 24/7"},
    {"id": "lion.ip",        "name": "Smithsonian Lion Cam",               "title": "Smithsonian Lion Cam Live Stream 24/7"},
    {"id": "nyc.ip",         "name": "Times Square Live Cam",              "title": "Times Square Live Cam 24/7"},
    {"id": "penguin.ip",     "name": "Penguins Live Cam",                  "title": "Penguins Live Stream 24/7"},
    {"id": "tiger.ip",       "name": "Live Tiger Cam",                     "title": "Tigers Live Stream 24/7"},
    {"id": "smpark.ip",      "name": "Santa Monica-Pacific Park",          "title": "Santa Monica-Pacific Park Live Stream 24/7"},
    {"id": "smpier.ip",      "name": "Santa Monica Pier Live",             "title": "Santa Monica Pier Live Stream 24/7"},
    {"id": "lodge.ip",       "name": "Nessie Cam-Shoreland Lodges",        "title": "Nessie Cam-Shoreland Lodges Live Stream 24/7"},
    {"id": "pine.ip",        "name": "Nessie Cam-Pinewood Steading Live",  "title": "Nessie Cam-Pinewood Steading Live Stream 24/7"},
    {"id": "bay.ip",         "name": "Bayfront Park, Miami Live",          "title": "Bayfront Park, Miami Live Stream 24/7"},
    {"id": "wrogley.ip",     "name": "Wrigley Field Live",                 "title": "Wrigley Field Live Stream 24/7"},
    {"id": "cedar.ip",       "name": "Cedar Key Live",                     "title": "Cedar Key Live Stream 24/7"},
    {"id": "butterfly.ip",   "name": "Butterfly House Live",               "title": "Butterfly House Live Stream 24/7"},
    {"id": "jelly.ip",       "name": "Moon Jellies Live",                  "title": "Moon Jellies Live Stream 24/7"},
    {"id": "ohio.ip",        "name": "Ohio Birdfeeder Live",               "title": "Ohio Birdfeeder Live Stream 24/7"},
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
    {"id": "glades.ip",      "name": "Port Everglades Live",               "title": "Port Everglades Live Stream 24/7"},
    {"id": "miami.ip",       "name": "Port Miami Live",                    "title": "Port Miami Live Stream 24/7"},
    {"id": "kwharbor.ip",    "name": "Key West Harbor Live",               "title": "Key West Harbor Live Stream 24/7"},
    {"id": "nassau.ip",      "name": "Port Nassau Live",                   "title": "Port Nassau Live Stream 24/7"},
    {"id": "juneau.ip",      "name": "Juneau Harbor Live",                 "title": "Juneau Harbor Live Stream 24/7"},
    {"id": "usa.ip",         "name": "Rotating USA Weather Cams",          "title": "Rotating USA Weather Cams 24/7"},
    {"id": "gar.ip",         "name": "Gar Woods Pier Bar Live",            "title": "Gar Woods Pier Bar Live Stream 24/7"},
    {"id": "meow.ip",        "name": "Cats Meow Karaoke Live",             "title": "Cats Meow Karaoke Live Stream 24/7"},
    {"id": "windjammer.ip",  "name": "Windjammer Beach Club Live",         "title": "Windjammer Beach Club Live Stream 24/7"},
    {"id": "dead.ip",        "name": "Dead Dog Saloon Live",               "title": "Dead Dog Saloon Live Stream 24/7"},
    {"id": "tydz.ip",        "name": "RipTydz Oceanfront Grille Live",     "title": "RipTydz Oceanfront Grille Live Stream 24/7"},
    {"id": "merry.ip",       "name": "Merrymoor Inn Live",                 "title": "Merrymoor Inn Live Stream 24/7"},
    {"id": "robin.ip",       "name": "Robinhoods Bay Live",                "title": "Robinhoods Bay Live Stream 24/7"},
    {"id": "golazo.ip",      "name": "Golazo Network",                     "title": "Golazo Network"},
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
