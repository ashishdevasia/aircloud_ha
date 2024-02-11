from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (DOMAIN, PLATFORM_NAME, API, CONF_EMAIL, CONF_PASSWORD,
                    CONF_TEMP_ADJUST, SERVICE_EXEC_COMMAND, SERVICE_EXEC_COMMAND_DATA_SCHEMA,
                    ARG_ID, ARG_POWER, ARG_TARGET_TEMP, ARG_MODE,
                    ARG_FAN_SPEED, ARG_FAN_SWING, ARG_HUMIDITY)
from .api import AirCloudApi


async def async_setup(hass: HomeAssistant, config: dict):
    conf = config.get(DOMAIN)
    login = config[DOMAIN].get(CONF_EMAIL)
    password = config[DOMAIN].get(CONF_PASSWORD)
    temp_adjust = config[DOMAIN].get(CONF_TEMP_ADJUST)

    if conf:
        hass.data[DOMAIN] = {}
        hass.data[DOMAIN][API] = AirCloudApi(login, password)
        hass.data[DOMAIN][CONF_TEMP_ADJUST] = temp_adjust

    async def service_exec_command(service_call):
        service_data = service_call.data
        await hass.data[DOMAIN][API].execute_command(service_data[ARG_ID],
                                                     service_data[ARG_POWER],
                                                     service_data[ARG_TARGET_TEMP],
                                                     service_data[ARG_MODE],
                                                     service_data[ARG_FAN_SPEED],
                                                     service_data[ARG_FAN_SWING],
                                                     service_data[ARG_HUMIDITY])

    hass.services.async_register(
        DOMAIN,
        SERVICE_EXEC_COMMAND,
        service_exec_command,
        schema=SERVICE_EXEC_COMMAND_DATA_SCHEMA,
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, PLATFORM_NAME)
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    return await hass.config_entries.async_forward_entry_unload(entry, PLATFORM_NAME)
