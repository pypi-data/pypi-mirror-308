from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LeSignalingCls:
	"""LeSignaling commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("leSignaling", core, parent)

	def get_ccentral(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:WFCMap:LESignaling:CCENtral \n
		Snippet: value: int = driver.configure.connection.wfcMap.leSignaling.get_ccentral() \n
		Specifies the number of connection events to wait before checking the channel map change. \n
			:return: wait_for_ch_map: numeric Range: 6 to 100
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:WFCMap:LESignaling:CCENtral?')
		return Conversions.str_to_int(response)

	def set_ccentral(self, wait_for_ch_map: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:WFCMap:LESignaling:CCENtral \n
		Snippet: driver.configure.connection.wfcMap.leSignaling.set_ccentral(wait_for_ch_map = 1) \n
		Specifies the number of connection events to wait before checking the channel map change. \n
			:param wait_for_ch_map: numeric Range: 6 to 100
		"""
		param = Conversions.decimal_value_to_str(wait_for_ch_map)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:WFCMap:LESignaling:CCENtral {param}')
