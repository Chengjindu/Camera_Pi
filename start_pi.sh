#!/bin/bash

# Function to gracefully shutdown processes
cleanup() {
  echo "Stopping LED.py and GStreamer..."
  # Send SIGTERM to both processes
  kill $LED_PID $GST_PID
  wait $LED_PID $GST_PID 2>/dev/null
  echo "Processes stopped."
}

# Set trap to call cleanup function on SIGINT (Ctrl+C)
trap cleanup SIGINT

# Set permissions for GPIO access
sudo chown root:gpio /dev/gpiomem
sudo chmod g+rw /dev/gpiomem

# Source .bashrc - ensure this is necessary as it may not be needed for script execution
source ~/.bashrc

# Start LED.py in the background and save its PID
python /home/sbrp/Camera_Pi/LED.py &
LED_PID=$!

# Start GStreamer streaming in the background and save its PID
libcamera-vid -t 0 --inline --nopreview --width 640 --height 480 --framerate 30 \
--brightness 0.05 --shutter 0 --awbgains 1.0,0.85,0.85 -o - | \
gst-launch-1.0 fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! udpsink host=10.255.32.70 port=5000 &
GST_PID=$!

# Wait for both processes to exit
wait $LED_PID $GST_PID