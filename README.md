# EPG Auto-Generator for 24/7 Live Streams

Automatically generates XMLTV format EPG data for your live stream channels in Dispatcharr and Jellyfin.

## Quick Start

### 1. Generate EPG File

```bash
# Generate 14 days of EPG data (default)
python3 generate_epg.py

# Generate 30 days
python3 generate_epg.py --days 30

# Custom output filename
python3 generate_epg.py -o /path/to/epg.xml
```

### 2. Setup Automatic Updates (Optional)

```bash
# Run the setup script
chmod +x setup_epg.sh
./setup_epg.sh
```

This will:
- Test the EPG generator
- Optionally set up a weekly cron job to auto-regenerate

## Configure Jellyfin

1. **Navigate to EPG Settings**
   - Dashboard → Live TV → Guide Data Providers → Add XMLTV

2. **Add EPG File**
   - File path: `/path/to/epg.xml`
   - Or use a URL if hosted on a web server

3. **Refresh Guide Data**
   - Dashboard → Live TV → Refresh Guide Data

## Configure Dispatcharr

In your Dispatcharr configuration, point to the generated `epg.xml` file:

```yaml
epg:
  source: /path/to/epg.xml
  refresh_interval: 86400  # 24 hours
```

## Customization

### Add/Modify Channels

Edit the `CHANNELS` list in `generate_epg.py`:

```python
CHANNELS = [
    {
        'id': 'YourChannel.id',           # Must match M3U tvg-id
        'display_name': 'Channel Name',   # Display name
        'title': 'Program Title',         # Show in guide
        'description': 'Description',     # Program description
        'category': 'Category',           # Genre/category
        'timezone': '+0900'               # Timezone offset
    },
    # Add more channels...
]
```

### Timezone Reference

Common timezones:
- `+0900` - Japan (JST)
- `+0800` - China (CST)
- `-0800` - Pacific (PST)
- `-0700` - Pacific (PDT)
- `-0500` - Eastern (EST)
- `-0400` - Eastern (EDT)
- `+0000` - UTC

## Automation Options

### Option 1: Cron Job (Linux/Mac)

Generate EPG every Sunday at 2 AM:

```bash
crontab -e
```

Add:
```
0 2 * * 0 cd /path/to/scripts && /usr/bin/python3 generate_epg.py --days 14 -o epg.xml
```

### Option 2: Systemd Timer (Linux)

Create `/etc/systemd/system/epg-generator.service`:

```ini
[Unit]
Description=EPG Generator

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /path/to/generate_epg.py --days 14 -o /path/to/epg.xml
User=yourusername
```

Create `/etc/systemd/system/epg-generator.timer`:

```ini
[Unit]
Description=Weekly EPG Generation

[Timer]
OnCalendar=Sun *-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable:
```bash
sudo systemctl enable epg-generator.timer
sudo systemctl start epg-generator.timer
```

### Option 3: Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Weekly, Sunday, 2:00 AM
4. Action: Start a program
   - Program: `python`
   - Arguments: `C:\path\to\generate_epg.py --days 14 -o C:\path\to\epg.xml`

### Option 4: Docker (if running Jellyfin in Docker)

Add to your docker-compose.yml:

```yaml
services:
  epg-generator:
    image: python:3-slim
    volumes:
      - ./scripts:/scripts
      - ./epg:/epg
    command: >
      sh -c "while true; do
        python3 /scripts/generate_epg.py --days 14 -o /epg/epg.xml;
        sleep 604800;
      done"
    restart: unless-stopped
```

## Troubleshooting

### EPG Not Showing in Jellyfin

1. **Check file path**: Ensure Jellyfin can read the EPG file
2. **Permissions**: Make sure the file has read permissions
3. **Refresh**: Dashboard → Live TV → Refresh Guide Data
4. **Logs**: Check Jellyfin logs for EPG errors

### Wrong Timezone

Edit the `timezone` field for each channel in `generate_epg.py` to match the stream's location.

### Program Data Not Updating

- Check that your cron job is running: `crontab -l`
- Check logs: `cat epg_update.log`
- Manually regenerate: `python3 generate_epg.py`

## File Structure

```
.
├── generate_epg.py      # Main EPG generator script
├── setup_epg.sh         # Quick setup script
├── epg.xml              # Generated EPG file (created after first run)
├── epg_update.log       # Cron job logs (if using cron)
└── README.md            # This file
```

## Requirements

- Python 3.6 or higher
- No additional Python packages required (uses standard library)

## License

Free to use and modify for personal use.

## Support

For issues with:
- **Jellyfin**: https://jellyfin.org/docs/
- **Dispatcharr**: Check Dispatcharr documentation
- **This script**: Open an issue or modify to fit your needs
