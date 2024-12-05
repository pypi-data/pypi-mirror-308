from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	def get_le_2_m(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:PACKets:LENergy:LE2M \n
		Snippet: value: int = driver.configure.rxQuality.iqCoherency.packets.lowEnergy.get_le_2_m() \n
		Defines the number of packets to be sent per measurement cycle (statistics cycle) . Commands for uncoded LE 1M PHY (..
		:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:return: packets: numeric Range: 1 to 6.4E+6
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:PACKets:LENergy:LE2M?')
		return Conversions.str_to_int(response)

	def set_le_2_m(self, packets: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:PACKets:LENergy:LE2M \n
		Snippet: driver.configure.rxQuality.iqCoherency.packets.lowEnergy.set_le_2_m(packets = 1) \n
		Defines the number of packets to be sent per measurement cycle (statistics cycle) . Commands for uncoded LE 1M PHY (..
		:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:param packets: numeric Range: 1 to 6.4E+6
		"""
		param = Conversions.decimal_value_to_str(packets)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:PACKets:LENergy:LE2M {param}')

	def get_le_1_m(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:PACKets:LENergy:LE1M \n
		Snippet: value: int = driver.configure.rxQuality.iqCoherency.packets.lowEnergy.get_le_1_m() \n
		Defines the number of packets to be sent per measurement cycle (statistics cycle) . Commands for uncoded LE 1M PHY (..
		:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:return: packets: numeric Range: 1 to 6.4E+6
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:PACKets:LENergy:LE1M?')
		return Conversions.str_to_int(response)

	def set_le_1_m(self, packets: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:PACKets:LENergy:LE1M \n
		Snippet: driver.configure.rxQuality.iqCoherency.packets.lowEnergy.set_le_1_m(packets = 1) \n
		Defines the number of packets to be sent per measurement cycle (statistics cycle) . Commands for uncoded LE 1M PHY (..
		:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:param packets: numeric Range: 1 to 6.4E+6
		"""
		param = Conversions.decimal_value_to_str(packets)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:PACKets:LENergy:LE1M {param}')
