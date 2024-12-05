from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePyCls:
	"""TypePy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("typePy", core, parent)

	# noinspection PyTypeChecker
	def get_le_signaling(self) -> enums.AddressType:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:ADDRess:TYPE:LESignaling \n
		Snippet: value: enums.AddressType = driver.configure.connection.address.typePy.get_le_signaling() \n
		Selects public or random addressing. \n
			:return: addr_type: PUBLic | RANDom
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:ADDRess:TYPE:LESignaling?')
		return Conversions.str_to_scalar_enum(response, enums.AddressType)

	def set_le_signaling(self, addr_type: enums.AddressType) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:ADDRess:TYPE:LESignaling \n
		Snippet: driver.configure.connection.address.typePy.set_le_signaling(addr_type = enums.AddressType.PUBLic) \n
		Selects public or random addressing. \n
			:param addr_type: PUBLic | RANDom
		"""
		param = Conversions.enum_scalar_to_str(addr_type, enums.AddressType)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:ADDRess:TYPE:LESignaling {param}')
