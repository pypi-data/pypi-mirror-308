from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	def reset(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: CALL:BLUetooth:SIGNaling<Instance>:LENergy:RESet \n
		Snippet: driver.call.lowEnergy.reset() \n
		Sends the HCI reset command to the EUT via USB. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'CALL:BLUetooth:SIGNaling<Instance>:LENergy:RESet', opc_timeout_ms)
