from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Le1MCls:
	"""Le1M commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("le1M", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal See 'Reliability indicator'
			- Per: float: float Packet error rate Range: 0 % to 100 %, Unit: %
			- Packets_Received: int: decimal Number of correct packets received and reported by the EUT Range: 0 to 30E+3
			- Search_Result: float: float TX level of the R&S CMW resulting in the configured PER search limit Range: -999 dBm to 0 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Per'),
			ArgStruct.scalar_int('Packets_Received'),
			ArgStruct.scalar_float('Search_Result')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Per: float = None
			self.Packets_Received: int = None
			self.Search_Result: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PER:AUDio:LENergy[:LE1M] \n
		Snippet: value: ResultData = driver.rxQuality.search.per.audio.lowEnergy.le1M.read() \n
		Return the results of PER search RX measurement for LE direct test mode, LE connection tests, and LE audio.
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- LE audio: Commands (..:AUDio:LENergy..) are available. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PER:AUDio:LENergy:LE1M?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PER:AUDio:LENergy[:LE1M] \n
		Snippet: value: ResultData = driver.rxQuality.search.per.audio.lowEnergy.le1M.fetch() \n
		Return the results of PER search RX measurement for LE direct test mode, LE connection tests, and LE audio.
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- LE audio: Commands (..:AUDio:LENergy..) are available. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PER:AUDio:LENergy:LE1M?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal See 'Reliability indicator'
			- Per: float or bool: float Packet error rate Range: 0 % to 100 %, Unit: %
			- Packets_Received: float or bool: decimal Number of correct packets received and reported by the EUT Range: 0 to 30E+3
			- Search_Result: float or bool: float TX level of the R&S CMW resulting in the configured PER search limit Range: -999 dBm to 0 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float_ext('Per'),
			ArgStruct.scalar_float_ext('Packets_Received'),
			ArgStruct.scalar_float_ext('Search_Result')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Per: float or bool = None
			self.Packets_Received: float or bool = None
			self.Search_Result: float or bool = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PER:AUDio:LENergy[:LE1M] \n
		Snippet: value: CalculateStruct = driver.rxQuality.search.per.audio.lowEnergy.le1M.calculate() \n
		Return the results of PER search RX measurement for LE direct test mode, LE connection tests, and LE audio.
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- LE audio: Commands (..:AUDio:LENergy..) are available. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:PER:AUDio:LENergy:LE1M?', self.__class__.CalculateStruct())
