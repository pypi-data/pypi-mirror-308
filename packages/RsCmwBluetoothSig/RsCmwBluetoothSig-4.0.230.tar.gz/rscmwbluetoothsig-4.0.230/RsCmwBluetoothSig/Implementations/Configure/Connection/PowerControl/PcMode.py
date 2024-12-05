from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PcModeCls:
	"""PcMode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pcMode", core, parent)

	def get_le_signaling(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:PCMode:LESignaling \n
		Snippet: value: bool = driver.configure.connection.powerControl.pcMode.get_le_signaling() \n
		Specifies, whether the power commands respect the reported EUT capabilities or ignore them. \n
			:return: override_capabilites: OFF | ON OFF: The reported EUT capabilities are respected. ON: The reported EUT capabilities are ignored.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:PCMode:LESignaling?')
		return Conversions.str_to_bool(response)

	def set_le_signaling(self, override_capabilites: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:PCMode:LESignaling \n
		Snippet: driver.configure.connection.powerControl.pcMode.set_le_signaling(override_capabilites = False) \n
		Specifies, whether the power commands respect the reported EUT capabilities or ignore them. \n
			:param override_capabilites: OFF | ON OFF: The reported EUT capabilities are respected. ON: The reported EUT capabilities are ignored.
		"""
		param = Conversions.bool_to_str(override_capabilites)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:PCMode:LESignaling {param}')
