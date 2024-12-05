from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EutCls:
	"""Eut commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("eut", core, parent)

	def get_le_signaling(self) -> str:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:ADDRess:EUT:LESignaling \n
		Snippet: value: str = driver.configure.connection.address.eut.get_le_signaling() \n
		Specifies the default EUT. \n
			:return: address_def: hex Range: #H0 to #HFFFFFFFFFFFF
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:ADDRess:EUT:LESignaling?')
		return trim_str_response(response)

	def set_le_signaling(self, address_def: str) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:ADDRess:EUT:LESignaling \n
		Snippet: driver.configure.connection.address.eut.set_le_signaling(address_def = rawAbc) \n
		Specifies the default EUT. \n
			:param address_def: hex Range: #H0 to #HFFFFFFFFFFFF
		"""
		param = Conversions.value_to_str(address_def)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:ADDRess:EUT:LESignaling {param}')
