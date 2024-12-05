from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CteCls:
	"""Cte commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cte", core, parent)

	def get_low_energy(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:NANTenna:CTE:LENergy \n
		Snippet: value: int = driver.configure.rfSettings.nantenna.cte.get_low_energy() \n
		Specifies the number of EUT's antennas. One reference and one non-reference antenna is mandatory. \n
			:return: no_of_antenna: numeric Range: 2 to 4
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:NANTenna:CTE:LENergy?')
		return Conversions.str_to_int(response)

	def set_low_energy(self, no_of_antenna: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:NANTenna:CTE:LENergy \n
		Snippet: driver.configure.rfSettings.nantenna.cte.set_low_energy(no_of_antenna = 1) \n
		Specifies the number of EUT's antennas. One reference and one non-reference antenna is mandatory. \n
			:param no_of_antenna: numeric Range: 2 to 4
		"""
		param = Conversions.decimal_value_to_str(no_of_antenna)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:NANTenna:CTE:LENergy {param}')
