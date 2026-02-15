# Quick Start Guide - EPG Generator

## Immediate Use (3 Steps)

### 1. Generate Your EPG File

```bash
python3 generate_epg.py
```

This creates `epg.xml` with 14 days of programming data.

### 2. Add to Jellyfin

**Dashboard → Live TV → Guide Data Providers**
- Click "+" to add XMLTV
- File path: `/path/to/epg.xml`
- Click Save
- Click "Refresh Guide Data"

### 3. Done!

Your channels now have EPG data in Jellyfin.

---

## Customization

### Change Number of Days

```bash
# 30 days instead of 14
python3 generate_epg.py --days 30
```

### Add More Channels

Edit `generate_epg.py`, find the `CHANNELS` list, and add:

```python
{
    'id': 'YourChannel.id',        # Must match M3U tvg-id
    'display_name': 'Channel Name',
    'title': 'Show Title',
    'description': 'Description here',
    'category': 'Animals',         # or 'Live', 'News', etc.
    'timezone': '+0000'            # Adjust for location
}
```

### Auto-Update Weekly

```bash
chmod +x setup_epg.sh
./setup_epg.sh
```

Follow the prompts to set up automatic weekly regeneration.

---

## Common Timezones

- Japan: `+0900`
- China: `+0800`
- Los Angeles: `-0800` (PST) or `-0700` (PDT)
- New York: `-0500` (EST) or `-0400` (EDT)
- London: `+0000` (GMT) or `+0100` (BST)
- UTC: `+0000`

---

## Troubleshooting

**EPG not showing in Jellyfin?**
1. Check file path is correct
2. Click "Refresh Guide Data" in Jellyfin
3. Restart Jellyfin

**Wrong times?**
- Adjust the `timezone` field in the CHANNELS list

**Need more help?**
See the full README.md for detailed instructions.

