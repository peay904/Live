#!/usr/bin/env python3
"""
EPG Generator for 24/7 Live Streams
Generates XMLTV format EPG data for Dispatcharr/Jellyfin
"""

from datetime import datetime, timedelta
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
from xml.dom import minidom
import argparse

# Channel configuration
CHANNELS = [
    {
        'id': 'Monkeys.yt',
        'display_name': 'Live Monkey Cam',
        'title': 'Live Monkey Cam',
        'description': '24/7 live stream from Awaji Monkey Center, Japan',
        'category': 'Animals',
        'timezone': '-0500'
    },
    {
        'id': 'BaldEagle.yt',
        'display_name': 'Live Bald Eagle Nest',
        'title': 'Bald Eagle Nest Cam',
        'description': '24/7 live bald eagle nest observation in Los Angeles',
        'category': 'Animals',
        'timezone': '-0500'
    },
    {
        'id': 'ShibuyaScramble.yt',
        'display_name': 'Shibuya Scramble Crossing',
        'title': 'Shibuya Scramble Crossing',
        'description': '24/7 live view of Shibuya Crossing, Tokyo',
        'category': 'Live',
        'timezone': '-0500'
    },
    {
        'id': 'Pandas.yt',
        'display_name': 'Live Panda Cam',
        'title': 'Giant Panda Cam',
        'description': '24/7 live giant panda observation from China',
        'category': 'Animals',
        'timezone': '-0500'
    }
]


def format_time(dt, timezone):
    """Format datetime to XMLTV format: YYYYMMDDHHmmss +/-HHMM"""
    return dt.strftime('%Y%m%d%H%M%S') + ' ' + timezone


def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = tostring(elem, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')


def generate_epg(days=14, output_file='epg.xml'):
    """
    Generate EPG XML file for the specified number of days
    
    Args:
        days: Number of days to generate EPG data for (default: 14)
        output_file: Output filename (default: epg.xml)
    """
    # Create root element
    tv = Element('tv')
    tv.set('generator-info-name', 'Live Stream EPG Generator')
    
    # Add channel definitions
    for channel in CHANNELS:
        channel_elem = SubElement(tv, 'channel')
        channel_elem.set('id', channel['id'])
        
        display_name = SubElement(channel_elem, 'display-name')
        display_name.text = channel['display_name']
    
    # Generate program entries
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    for day in range(days):
        current_day = start_date + timedelta(days=day)
        next_day = current_day + timedelta(days=1)
        
        for channel in CHANNELS:
            programme = SubElement(tv, 'programme')
            programme.set('start', format_time(current_day, channel['timezone']))
            programme.set('stop', format_time(next_day, channel['timezone']))
            programme.set('channel', channel['id'])
            
            title = SubElement(programme, 'title')
            title.set('lang', 'en')
            title.text = channel['title']
            
            desc = SubElement(programme, 'desc')
            desc.set('lang', 'en')
            desc.text = channel['description']
            
            category = SubElement(programme, 'category')
            category.set('lang', 'en')
            category.text = channel['category']
    
    # Write to file with pretty formatting
    xml_string = prettify_xml(tv)
    
    # Add DOCTYPE declaration
    doctype = '<!DOCTYPE tv SYSTEM "xmltv.dtd">\n'
    xml_lines = xml_string.split('\n')
    xml_lines.insert(1, doctype)
    final_xml = '\n'.join(xml_lines)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_xml)
    
    print(f"✓ EPG generated successfully: {output_file}")
    print(f"✓ Generated {days} days of programming for {len(CHANNELS)} channels")
    print(f"✓ Date range: {start_date.strftime('%Y-%m-%d')} to {(start_date + timedelta(days=days-1)).strftime('%Y-%m-%d')}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate EPG XML for 24/7 live streams',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_epg.py                    # Generate 14 days (default)
  python generate_epg.py --days 30          # Generate 30 days
  python generate_epg.py -o custom.xml      # Custom output filename
  python generate_epg.py --days 7 -o epg.xml
        """
    )
    
    parser.add_argument(
        '--days',
        type=int,
        default=14,
        help='Number of days to generate EPG data for (default: 14)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='epg.xml',
        help='Output filename (default: epg.xml)'
    )
    
    args = parser.parse_args()
    
    if args.days < 1:
        parser.error("Days must be at least 1")
    
    generate_epg(days=args.days, output_file=args.output)


if __name__ == '__main__':
    main()
