# Persist the persistent notification after Home Assistant shutdown
The persistent notification will be saved in a new sensor `sensor.persist_persistent_notifications` when shutting down, and restored from this sensor after HA has restarted.

# Installation
- In your Home Assistant configuration directory (~/.homeassistant), create a directory custom_components if not already existing and navigate in it.
- `git clone https://github.com/slashback100/persist_persistent_notifications.git`
- Restart Home Assistant

# Configuration
No configuration
