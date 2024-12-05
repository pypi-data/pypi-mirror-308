from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CecOffsetCls:
	"""CecOffset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cecOffset", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CECoffset:LESignaling \n
		Snippet: value: int = driver.configure.connection.audio.cecOffset.get_le_signaling() \n
		Specifies the connection event count offset for LE audio. \n
			:return: con_evnt_cnt_oset: numeric Range: 10 to 500
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CECoffset:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, con_evnt_cnt_oset: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CECoffset:LESignaling \n
		Snippet: driver.configure.connection.audio.cecOffset.set_le_signaling(con_evnt_cnt_oset = 1) \n
		Specifies the connection event count offset for LE audio. \n
			:param con_evnt_cnt_oset: numeric Range: 10 to 500
		"""
		param = Conversions.decimal_value_to_str(con_evnt_cnt_oset)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CECoffset:LESignaling {param}')
