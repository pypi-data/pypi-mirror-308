from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NsEventsCls:
	"""NsEvents commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nsEvents", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:NSEVents:LESignaling \n
		Snippet: value: int = driver.configure.connection.audio.nsEvents.get_le_signaling() \n
		Sets the number of subevents for LE audio. \n
			:return: no_subevents: numeric Range: 1 to 31
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:NSEVents:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, no_subevents: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:NSEVents:LESignaling \n
		Snippet: driver.configure.connection.audio.nsEvents.set_le_signaling(no_subevents = 1) \n
		Sets the number of subevents for LE audio. \n
			:param no_subevents: numeric Range: 1 to 31
		"""
		param = Conversions.decimal_value_to_str(no_subevents)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:NSEVents:LESignaling {param}')
