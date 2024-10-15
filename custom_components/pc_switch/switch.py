
import asyncio
from wakeonlan import send_magic_packet
import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, CONF_MAC, CONF_IP, CONF_SHUTDOWN_COMMAND

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    mac = entry.data[CONF_MAC]
    ip = entry.data[CONF_IP]
    shutdown_command = entry.data[CONF_SHUTDOWN_COMMAND]
    async_add_entities([PCControlSwitch(mac, ip, shutdown_command)], True)

class PCControlSwitch(SwitchEntity):
    def __init__(self, mac: str, ip: str, shutdown_command: str):
        self._mac = mac
        self._ip = ip
        self._shutdown_command = shutdown_command
        self._is_on = False
        self._attr_name = "PC Power"
        self._attr_unique_id = f"pc_control_{mac.replace(':', '')}"

    @property
    def is_on(self) -> bool:
        return self._is_on

    async def async_turn_on(self, **kwargs) -> None:
        send_magic_packet(self._mac)
        await self._async_update_state()

    async def async_turn_off(self, **kwargs) -> None:
        await asyncio.create_subprocess_shell(self._shutdown_command)
        await self._async_update_state()

    async def async_update(self) -> None:
        await self._async_update_state()

    async def _async_update_state(self) -> None:
        ping_result = await self.hass.async_add_executor_job(self._ping)
        self._is_on = ping_result == 0

    def _ping(self) -> int:
        return os.system(f"ping -c 1 -W 1 {self._ip} > /dev/null 2>&1")