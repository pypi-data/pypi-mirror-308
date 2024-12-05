from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CmwCls:
	"""Cmw commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cmw", core, parent)

	def get_le_signaling(self) -> str:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:ADDRess:CMW:LESignaling \n
		Snippet: value: str = driver.configure.connection.address.cmw.get_le_signaling() \n
		Sets the public address of R&S CMW \n
			:return: cmw_address: hex Range: #H0 to #HFFFFFFFFFFFF
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:ADDRess:CMW:LESignaling?')
		return trim_str_response(response)

	def set_le_signaling(self, cmw_address: str) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:ADDRess:CMW:LESignaling \n
		Snippet: driver.configure.connection.address.cmw.set_le_signaling(cmw_address = rawAbc) \n
		Sets the public address of R&S CMW \n
			:param cmw_address: hex Range: #H0 to #HFFFFFFFFFFFF
		"""
		param = Conversions.value_to_str(cmw_address)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:ADDRess:CMW:LESignaling {param}')
