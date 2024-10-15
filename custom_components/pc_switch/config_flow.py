
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_MAC, CONF_IP, CONF_SHUTDOWN_COMMAND

class PCControlConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="PC Control", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_MAC): str,
                vol.Required(CONF_IP): str,
                vol.Required(CONF_SHUTDOWN_COMMAND): str,
            }),
            errors=errors,
        )