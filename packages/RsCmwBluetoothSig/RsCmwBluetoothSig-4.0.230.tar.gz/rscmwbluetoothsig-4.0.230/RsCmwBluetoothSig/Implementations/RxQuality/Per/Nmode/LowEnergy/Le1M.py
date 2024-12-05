from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


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
			- Packets_Received: int: decimal Number of correct packets received and reported by the EUT. Range: 0 to 30E+3"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Per'),
			ArgStruct.scalar_int('Packets_Received')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Per: float = None
			self.Packets_Received: int = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:PER:NMODe:LENergy:LE1M \n
		Snippet: value: ResultData = driver.rxQuality.per.nmode.lowEnergy.le1M.fetch() \n
		Return all results of the signaling LE Rx measurement for LE direct test, LE connection tests, and LE audio.
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- LE audio: Commands (..:AUDio:LENergy..) are available. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:PER:NMODe:LENergy:LE1M?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:SIGNaling<Instance>:RXQuality:PER:NMODe:LENergy:LE1M \n
		Snippet: value: ResultData = driver.rxQuality.per.nmode.lowEnergy.le1M.read() \n
		Return all results of the signaling LE Rx measurement for LE direct test, LE connection tests, and LE audio.
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- LE audio: Commands (..:AUDio:LENergy..) are available. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:SIGNaling<Instance>:RXQuality:PER:NMODe:LENergy:LE1M?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal See 'Reliability indicator'
			- Per: float or bool: float Packet error rate Range: 0 % to 100 %, Unit: %
			- Packets_Received: float or bool: decimal Number of correct packets received and reported by the EUT. Range: 0 to 30E+3"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float_ext('Per'),
			ArgStruct.scalar_float_ext('Packets_Received')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Per: float or bool = None
			self.Packets_Received: float or bool = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:SIGNaling<Instance>:RXQuality:PER:NMODe:LENergy:LE1M \n
		Snippet: value: CalculateStruct = driver.rxQuality.per.nmode.lowEnergy.le1M.calculate() \n
		Return all results of the signaling LE Rx measurement for LE direct test, LE connection tests, and LE audio.
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- LE direct test mode: Commands for uncoded LE 1M PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available.
			- LE connection tests (normal mode) : Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- LE audio: Commands (..:AUDio:LENergy..) are available. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:SIGNaling<Instance>:RXQuality:PER:NMODe:LENergy:LE1M?', self.__class__.CalculateStruct())
