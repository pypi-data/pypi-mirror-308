from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	def get_tmode(self) -> float:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:FREQuency:TMODe \n
		Snippet: value: float = driver.configure.rfSettings.frequency.get_tmode() \n
		Queries the frequency used for LE UTP test mode. \n
			:return: rx_tx_freq: float Range: 100 MHz to 6 GHz
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:FREQuency:TMODe?')
		return Conversions.str_to_float(response)

	def get_dt_mode(self) -> float:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:FREQuency:DTMode \n
		Snippet: value: float = driver.configure.rfSettings.frequency.get_dt_mode() \n
		Queries the frequency used for direct test mode. \n
			:return: rx_tx_freq: float Range: 100 MHz to 6 GHz
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:FREQuency:DTMode?')
		return Conversions.str_to_float(response)

	def get_tx_test(self) -> float:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:FREQuency:TXTest \n
		Snippet: value: float = driver.configure.rfSettings.frequency.get_tx_test() \n
		Queries the frequency used by the TX test. \n
			:return: rx_tx_freq: float Range: 2402 MHz to 2480 MHz , Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:FREQuency:TXTest?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	class LoopbackStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Rx_Freq: float: float Range: 2402 MHz to 2480 MHz , Unit: Hz
			- Tx_Freq: float: float Range: 2402 MHz to 2480 MHz , Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_float('Rx_Freq'),
			ArgStruct.scalar_float('Tx_Freq')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rx_Freq: float = None
			self.Tx_Freq: float = None

	def get_loopback(self) -> LoopbackStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:FREQuency:LOOPback \n
		Snippet: value: LoopbackStruct = driver.configure.rfSettings.frequency.get_loopback() \n
		Queries EUT RX and EUT TX frequencies used by the loopback test. \n
			:return: structure: for return value, see the help for LoopbackStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:FREQuency:LOOPback?', self.__class__.LoopbackStruct())
