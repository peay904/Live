#!/bin/bash
# Setup script for automatic EPG generation

echo "========================================="
echo "EPG Auto-Generator Setup"
echo "========================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_SCRIPT="$SCRIPT_DIR/generate_epg.py"
OUTPUT_FILE="$SCRIPT_DIR/epg.xml"

# Make the Python script executable
chmod +x "$PYTHON_SCRIPT"

echo "✓ Python script made executable"
echo ""

# Test run
echo "Running test generation..."
python3 "$PYTHON_SCRIPT" --days 14 -o "$OUTPUT_FILE"
echo ""

if [ -f "$OUTPUT_FILE" ]; then
    echo "✓ Test successful! EPG file created at: $OUTPUT_FILE"
    echo ""
else
    echo "✗ Error: EPG file was not created"
    exit 1
fi

# Cron job setup
echo "========================================="
echo "Cron Job Setup"
echo "========================================="
echo ""
echo "Would you like to set up automatic weekly EPG regeneration? (y/n)"
read -r SETUP_CRON

if [ "$SETUP_CRON" = "y" ] || [ "$SETUP_CRON" = "Y" ]; then
    # Cron job to run every Sunday at 2 AM
    CRON_CMD="0 2 * * 0 cd $SCRIPT_DIR && /usr/bin/python3 $PYTHON_SCRIPT --days 14 -o $OUTPUT_FILE >> $SCRIPT_DIR/epg_update.log 2>&1"
    
    echo ""
    echo "Add this line to your crontab (opens crontab editor):"
    echo ""
    echo "$CRON_CMD"
    echo ""
    echo "This will regenerate the EPG every Sunday at 2:00 AM"
    echo ""
    echo "Press Enter to open crontab editor, or Ctrl+C to skip..."
    read
    
    # Add to crontab
    (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
    
    echo "✓ Cron job added successfully!"
    echo ""
    echo "To view your cron jobs, run: crontab -l"
    echo "To edit cron jobs, run: crontab -e"
else
    echo ""
    echo "Skipping cron setup. You can manually run the script with:"
    echo "  python3 $PYTHON_SCRIPT --days 14"
    echo ""
    echo "Or add this to your crontab manually:"
    echo "  0 2 * * 0 cd $SCRIPT_DIR && /usr/bin/python3 $PYTHON_SCRIPT --days 14 -o $OUTPUT_FILE"
fi

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "EPG Location: $OUTPUT_FILE"
echo ""
echo "In Jellyfin:"
echo "  1. Go to Dashboard → Live TV → Guide Data Providers"
echo "  2. Add XMLTV → Enter path: $OUTPUT_FILE"
echo "  3. Save and refresh guide data"
echo ""
echo "Manual regeneration:"
echo "  python3 $PYTHON_SCRIPT --days 14"
echo ""
