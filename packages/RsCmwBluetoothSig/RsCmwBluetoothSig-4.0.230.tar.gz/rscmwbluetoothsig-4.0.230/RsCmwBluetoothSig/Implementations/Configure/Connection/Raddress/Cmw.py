from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CmwCls:
	"""Cmw commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cmw", core, parent)

	def get_le_signaling(self) -> str:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:RADDress:CMW:LESignaling \n
		Snippet: value: str = driver.configure.connection.raddress.cmw.get_le_signaling() \n
		Queries the randomly generated address of R&S CMW \n
			:return: cmw_address: hex Range: #H0 to #HFFFFFFFFFFFF
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:RADDress:CMW:LESignaling?')
		return trim_str_response(response)
