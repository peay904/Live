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
    {"id": "broads.ip",      "name": "Norfolk Broads-England Live",        "title": "Norfolk Broads-England Live Stream 24/7"},
    {"id": "windjammer.ip",  "name": "Windjammer Beach Club Live",         "title": "Windjammer Beach Club Live Stream 24/7"},
    {"id": "tydz.ip",        "name": "RipTydz Oceanfront Grille Live",     "title": "RipTydz Oceanfront Grille Live Stream 24/7"},
    {"id": "golazo.ip",      "name": "Golazo Network",                     "title": "Golazo Network"},
    {"id": "bird.ip",        "name": "Birfeeder",                          "title": "Birdfeeder"},
    {"id": "pebble.ip",      "name": "Pebble Beach 18th Green",            "title": "Pebble Beach 18th Green"},
    {"id": "seals.ip",       "name": "Piedras Blancas Elephant Seals",     "title": "Piedras Blancas Elephant Seals"},
    {"id": "yosemite.ip",    "name": "Yosemite Falls",                     "title": "Yosemite Falls"},
    {"id": "niagara.ip",     "name": "Niagara Falls Live",                 "title": "Niagara Falls Live Stream 24/7"},
    {"id": "peggy.ip",       "name": "Peggy's Cove Lighthouse Live",       "title": "Peggy's Cove Lighthouse Live Stream 24/7"},
    {"id": "conch.ip",       "name": "Grand Cayman - Cracked Conch Live",  "title": "Grand Cayman - Cracked Conch Live Stream 24/7"},
    {"id": "sevenfalls.ip",  "name": "Seven Falls - Colorado Live",        "title": "Seven Falls - Colorado Live Stream 24/7"},
    {"id": "cloudcamp.ip",   "name": "Cloud Camp Live",                    "title": "Cloud Camp Live Stream 24/7"},
    {"id": "pikes.ip",       "name": "Pikes Peak Summit Live",             "title": "Pikes Peak Summit Live Stream 24/7"},
    {"id": "glenwood.ip",    "name": "Glenwood Hot Springs Live",          "title": "Glenwood Hot Springs Live Stream 24/7"},
    {"id": "princeton.ip",   "name": "Mt. Princeton Live",                 "title": "Mt. Princeton Live Stream 24/7"},
    {"id": "meigs.ip",       "name": "Meigs Point Nature Center Live",     "title": "Meigs Point Nature Center Live Stream 24/7"},
    {"id": "flamingo.ip",    "name": "Flamingo Cam Live",                  "title": "Flamingo Cam Live Stream 24/7"},
    {"id": "wynwood.ip",     "name": "Wynwood Miami Live",                 "title": "Wynwood Miami Live Stream 24/7"},
    {"id": "navarre.ip",     "name": "Navarre Beach Live",                 "title": "Navarre Beach Live Stream 24/7"},
    {"id": "balance.ip",     "name": "Balance Gaming Live",                "title": "Balance Gaming Live Stream 24/7"},
    {"id": "budalley.ip",    "name": "Bud & Alleys Live",                  "title": "Bud & Alleys Live Stream 24/7"},
    {"id": "ponycam.ip",     "name": "Geboltskirchen Ponycam Live",        "title": "Geboltskirchen Ponycam Live Stream 24/7"},
    {"id": "vogel.ip",       "name": "Osttirol Birdfeeder Live",           "title": "Osttirol Vogelfütterung Birdfeeder Live Stream 24/7"},
    {"id": "ossiach.ip",     "name": "Ossiachersee Boat Trip Live",        "title": "Ossiachersee Boat Trip Live Stream 24/7"},
    {"id": "chicagoriver.ip",     "name": "Chicago River Live",                    "title": "Chicago River Live Stream 24/7"},
    {"id": "boonecounty.ip",      "name": "Boone County Clerk Live",               "title": "Boone County Clerk Live Stream 24/7"},
    {"id": "catsmeow.ip",         "name": "Cats Meow Balcony - Bourbon St Live",   "title": "Cats Meow Balcony - Bourbon St Live Stream 24/7"},
    {"id": "bostonosprey.ip",     "name": "Boston Osprey Cam Live",                "title": "Boston Osprey Cam Live Stream 24/7"},
    {"id": "barharbor.ip",        "name": "Bar Harbor Osprey Live",                "title": "Bar Harbor Osprey Live Stream 24/7"},
    {"id": "barbershop.ip",       "name": "Grand Slam Barbershop Live",            "title": "Grand Slam Barbershop Live Stream 24/7"},
    {"id": "wolf.ip",             "name": "International Wolf Center Live",        "title": "International Wolf Center Live Stream 24/7"},
    {"id": "volleyball.ip",       "name": "MN Select Volleyball Center Live",      "title": "MN Select Volleyball Center Live Stream 24/7"},
    {"id": "como.ip",             "name": "Como Conservatory - St. Paul Live",     "title": "Como Conservatory - St. Paul Live Stream 24/7"},
    {"id": "oldfaithful.ip",      "name": "Old Faithful Live",                     "title": "Old Faithful Live Stream 24/7"},
    {"id": "bellagio.ip",         "name": "Bellagio Conservatory Live",            "title": "Bellagio Conservatory Live Stream 24/7"},
    {"id": "sphere.ip",           "name": "Las Vegas Sphere Live",                 "title": "Las Vegas Sphere Live Stream 24/7"},
    {"id": "spoklaundromat.ip",   "name": "Spokane Laundromat Live",               "title": "Spokane Laundromat Live Stream 24/7"},
    {"id": "greatfalls.ip",       "name": "Great Falls Live",                      "title": "Great Falls Live Stream 24/7"},
    {"id": "temple.ip",           "name": "Asa'Mai Hindu Temple Live",             "title": "Asa'Mai Hindu Temple Live Stream 24/7"},
    {"id": "broadway.ip",         "name": "Broadway Live",                         "title": "Broadway Live Stream 24/7"},
    {"id": "niagara2.ip",         "name": "Niagara Falls - Maid of the Mist Live", "title": "Niagara Falls - Maid of the Mist Live Stream 24/7"},
    {"id": "blueridge.ip",        "name": "Blue Ridge Mountains Live",             "title": "Blue Ridge Mountains Live Stream 24/7"},
    {"id": "sealion.ip",          "name": "Newport Sea Lion Docks Live",           "title": "Newport Sea Lion Docks Live Stream 24/7"},
    {"id": "sxm.ip",              "name": "SXM Island Cam Live",                   "title": "SXM Island Cam Live Stream 24/7"},
    {"id": "hheagle.ip",          "name": "Hilton Head Eagles Nest Live",          "title": "Hilton Head Eagles Nest Live Stream 24/7"},
    {"id": "windjammerdeck.ip",   "name": "Windjammer Deck Live",                  "title": "Windjammer Deck Live Stream 24/7"},
    {"id": "windjammerdeck2.ip",  "name": "Windjammer Deck 2 Live",                "title": "Windjammer Deck 2 Live Stream 24/7"},
    {"id": "windjammerdeck3.ip",  "name": "Windjammer Deck 3 Live",                "title": "Windjammer Deck 3 Live Stream 24/7"},
    {"id": "bristol.ip",          "name": "Bristol Motor Speedway Live",           "title": "Bristol Motor Speedway Live Stream 24/7"},
    {"id": "elephantsanctuary.ip","name": "Elephant Sanctuary Live",               "title": "Elephant Sanctuary Live Stream 24/7"},
    {"id": "butler.ip",           "name": "Butler Pitch Chip and Putt Live",       "title": "Butler Pitch Chip and Putt Courtyard Live Stream 24/7"},
    {"id": "butlert.ip",          "name": "Butler Pitch Chip and Putt 1st Tee",    "title": "Butler Pitch Chip and Putt 1st Tee 24/7"},
    {"id": "bigtexan.ip",         "name": "Big Texan 72oz Steak Challenge Live",   "title": "Big Texan 72oz Steak Challenge Live Stream 24/7"},
    {"id": "spokanefalls.ip",     "name": "Spokane Falls Live",                    "title": "Spokane Falls Live Stream 24/7"},
    {"id": "lazyranch.ip",        "name": "Lazy Ranch Live",                       "title": "Lazy Ranch Live Stream 24/7"},
    {"id": "chalten.ip",          "name": "El Chalten",                            "title": "El Chalten Live Stream 24/7"},
    {"id": "balsa.ip",            "name": "Santos - Balsa Santos/Guarujá Live",    "title": "Santos - Balsa Santos/Guarujá Live Stream 24/7"},
    {"id": "nath.ip",             "name": "Muzaffarpur - Garib Nath Mandir Live",  "title": "Muzaffarpur - Garib Nath Mandir Live Stream 24/7"},
    {"id": "sri.ip",              "name": "Dewata Beach - Sri Lanka Live",         "title": "Dewata Beach - Sri Lanka Live Stream 24/7"},
    {"id": "sainte.ip",           "name": "Sainte-Rose Live",                      "title": "Sainte-Rose Live Stream 24/7"},
    {"id": "athos.ip",            "name": "New Athos - Waterfall Live",            "title": "New Athos - Waterfall Live Stream 24/7"},
    {"id": "storks.ip",           "name": "Slovakia Storks Live",                  "title": "Slovakia Storks Live Stream 24/7"},
    {"id": "trash.ip",            "name": "Metro South Trash Live",                "title": "Metro South Trash Live Stream 24/7"},
    {"id": "trav.ip",             "name": "Myrtle Beach Travel Park Live",         "title": "Myrtle Beach Travel Park Live Stream 24/7"},
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
