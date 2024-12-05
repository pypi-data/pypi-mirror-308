from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	def get_le_1_m(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PACKets:AUDio:LENergy[:LE1M] \n
		Snippet: value: int = driver.configure.rxQuality.search.packets.audio.lowEnergy.get_le_1_m() \n
		Defines the number of data packets to be measured per measurement cycle (statistics cycle) .
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..:NMODe:LENergy:LRANge..) are available.
			- LE UTP test mode: Commands ..:TMODe:LENergy:.. are available.
			- LE audio: Commands ..:AUDio:LENergy.. are available. \n
			:return: number_packets: numeric Range: 1 to 30E+3
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PACKets:AUDio:LENergy:LE1M?')
		return Conversions.str_to_int(response)

	def set_le_1_m(self, number_packets: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PACKets:AUDio:LENergy[:LE1M] \n
		Snippet: driver.configure.rxQuality.search.packets.audio.lowEnergy.set_le_1_m(number_packets = 1) \n
		Defines the number of data packets to be measured per measurement cycle (statistics cycle) .
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..:NMODe:LENergy:LRANge..) are available.
			- LE UTP test mode: Commands ..:TMODe:LENergy:.. are available.
			- LE audio: Commands ..:AUDio:LENergy.. are available. \n
			:param number_packets: numeric Range: 1 to 30E+3
		"""
		param = Conversions.decimal_value_to_str(number_packets)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PACKets:AUDio:LENergy:LE1M {param}')
