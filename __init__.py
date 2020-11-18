"""Component to integrate with persist_persistent_notifications."""

import logging
import asyncio
from .const import (
        DOMAIN,
        SENSOR_PLATFORM,
        SENSOR
)
_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
    """Set up this component using YAML."""
    if config.get(DOMAIN) is None:
        # We get here if the integration is set up using config flow
        return True

async def async_setup_entry(hass, entry):
    """Set up this component using YAML."""
    #init the sensor entity
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, SENSOR_PLATFORM))

    def erase_and_save_notifications(event):
        hass.data[DOMAIN][SENSOR_PLATFORM][SENSOR].reset_persistent_notifications()
        save_notifications(event)

    def save_notifications(event):
        """ retrieve the persistent notification and store them in the sensor """
        _LOGGER.debug("saving persistent notification")
        sensor = hass.data[DOMAIN][SENSOR_PLATFORM][SENSOR]
        for pn_id in hass.states.entity_ids("persistent_notification"):
            pn = hass.states.get(pn_id)
            if sensor.is_new(pn.attributes):
                sensor.async_add_persistent_notification(pn.as_dict()["attributes"])
            #else:
            #    await asyncio.sleep(0)

    def restore_notifications(event):
        """ recreate the persistent notification based on the sensor attributes """
        _LOGGER.debug("restoring persistent notification")
        sensor = hass.data[DOMAIN][SENSOR_PLATFORM][SENSOR]
        for pn in sensor.persistent_notifications:
            service_data = {}
            service_data["message"] = pn["message"]
            if "title" in pn:
                service_data["title"] = pn["title"]
            #do not generate an id
            hass.services.async_call("persistent_notification", "create", service_data, blocking=False)


    hass.bus.async_listen("homeassistant_stop", erase_and_save_notifications)
    #hass.bus.listen_once("homeassistant_stop", erase_and_save_notifications)
    #also on the persistent_notification in case HA is not shut own gently
    #call erase_and_save and not just save to deal with dismiss & dismiss all
    hass.bus.async_listen("persistent_notifications_updated", erase_and_save_notifications)
    hass.bus.async_listen("homeassistant_start", restore_notifications)
    #restore_notifications(None)
    
    return True

