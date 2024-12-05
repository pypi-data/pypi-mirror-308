from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	def get_le_1_m(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:UNITs:CTE:LENergy:LE1M \n
		Snippet: value: int = driver.configure.connection.packets.units.cte.lowEnergy.get_le_1_m() \n
		Sets the number of CTE units. One CTE unit corresponds to 8 us. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY
		(..:LE2M..) are available. \n
			:return: cte_units: integer Range: 2 to 20
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:UNITs:CTE:LENergy:LE1M?')
		return Conversions.str_to_int(response)

	def set_le_1_m(self, cte_units: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:UNITs:CTE:LENergy:LE1M \n
		Snippet: driver.configure.connection.packets.units.cte.lowEnergy.set_le_1_m(cte_units = 1) \n
		Sets the number of CTE units. One CTE unit corresponds to 8 us. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY
		(..:LE2M..) are available. \n
			:param cte_units: integer Range: 2 to 20
		"""
		param = Conversions.decimal_value_to_str(cte_units)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:UNITs:CTE:LENergy:LE1M {param}')

	def get_le_2_m(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:UNITs:CTE:LENergy:LE2M \n
		Snippet: value: int = driver.configure.connection.packets.units.cte.lowEnergy.get_le_2_m() \n
		Sets the number of CTE units. One CTE unit corresponds to 8 us. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY
		(..:LE2M..) are available. \n
			:return: cte_units: integer Range: 2 to 20
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:UNITs:CTE:LENergy:LE2M?')
		return Conversions.str_to_int(response)

	def set_le_2_m(self, cte_units: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:UNITs:CTE:LENergy:LE2M \n
		Snippet: driver.configure.connection.packets.units.cte.lowEnergy.set_le_2_m(cte_units = 1) \n
		Sets the number of CTE units. One CTE unit corresponds to 8 us. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY
		(..:LE2M..) are available. \n
			:param cte_units: integer Range: 2 to 20
		"""
		param = Conversions.decimal_value_to_str(cte_units)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:UNITs:CTE:LENergy:LE2M {param}')
