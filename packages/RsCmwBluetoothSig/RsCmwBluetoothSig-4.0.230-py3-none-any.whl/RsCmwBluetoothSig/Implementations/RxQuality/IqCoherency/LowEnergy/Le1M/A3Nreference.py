from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class A3NreferenceCls:
	"""A3Nreference commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("a3Nreference", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Trans_Packets: int: decimal No. of transmitted packets Range: 0 to 200E+6
			- Rec_Events: float: No parameter help available
			- Rec_Events_Val_Crc: int: No parameter help available
			- No_Valid_Iqp_Airs: int: decimal No. of received valid IQ sample pairs
			- Valid_Iq_Pairs_Rec: float: float Percentage of received valid IQ sample pairs related to all received IQ pairs
			- Mean_Phase_Diff: float: No parameter help available
			- P_95_Mean_Ph_Diff: float: No parameter help available
			- Rec_Events_Cnt: int: decimal No. of received events
			- Pro_Events_Cnt: int: decimal No. of processed events
			- Pro_Events_Val_Crc: int: No parameter help available
			- Nof_Pos_Pha: int: decimal No. of possible phase measurements determined by CTE length, slot length and number of antennas"""
		__meta_args_list = [
			ArgStruct.scalar_int('Trans_Packets'),
			ArgStruct.scalar_float('Rec_Events'),
			ArgStruct.scalar_int('Rec_Events_Val_Crc'),
			ArgStruct.scalar_int('No_Valid_Iqp_Airs'),
			ArgStruct.scalar_float('Valid_Iq_Pairs_Rec'),
			ArgStruct.scalar_float('Mean_Phase_Diff'),
			ArgStruct.scalar_float('P_95_Mean_Ph_Diff'),
			ArgStruct.scalar_int('Rec_Events_Cnt'),
			ArgStruct.scalar_int('Pro_Events_Cnt'),
			ArgStruct.scalar_int('Pro_Events_Val_Crc'),
			ArgStruct.scalar_int('Nof_Pos_Pha')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Trans_Packets: int = None
			self.Rec_Events: float = None
			self.Rec_Events_Val_Crc: int = None
			self.No_Valid_Iqp_Airs: int = None
			self.Valid_Iq_Pairs_Rec: float = None
			self.Mean_Phase_Diff: float = None
			self.P_95_Mean_Ph_Diff: float = None
			self.Rec_Events_Cnt: int = None
			self.Pro_Events_Cnt: int = None
			self.Pro_Events_Val_Crc: int = None
			self.Nof_Pos_Pha: int = None

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LENergy:LE1M:A3NReference \n
		Snippet: value: ResultData = driver.rxQuality.iqCoherency.lowEnergy.le1M.a3Nreference.read() \n
		Returns the results of IQ samples coherency RP(m) measurement for the specified non-reference antenna. Commands for
		uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. Commands for the mandatory non-reference antenna (.
		..:A1NReference) , and optional third (...:A2NReference) and fourth (...:A3NReference) antennas are available. The values
		described below are returned by FETCh and READ commands. CALCulate commands return limit check results instead, one value
		for each result listed below. \n
		Use RsCmwBluetoothSig.reliability.last_value to read the updated reliability indicator. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LENergy:LE1M:A3NReference?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LENergy:LE1M:A3NReference \n
		Snippet: value: ResultData = driver.rxQuality.iqCoherency.lowEnergy.le1M.a3Nreference.fetch() \n
		Returns the results of IQ samples coherency RP(m) measurement for the specified non-reference antenna. Commands for
		uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. Commands for the mandatory non-reference antenna (.
		..:A1NReference) , and optional third (...:A2NReference) and fourth (...:A3NReference) antennas are available. The values
		described below are returned by FETCh and READ commands. CALCulate commands return limit check results instead, one value
		for each result listed below. \n
		Use RsCmwBluetoothSig.reliability.last_value to read the updated reliability indicator. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LENergy:LE1M:A3NReference?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Trans_Packets: float or bool: decimal No. of transmitted packets Range: 0 to 200E+6
			- Rec_Events: float or bool: No parameter help available
			- Rec_Events_Val_Crc: float or bool: No parameter help available
			- No_Valid_Iqp_Airs: enums.ResultStatus2: decimal No. of received valid IQ sample pairs
			- Valid_Iq_Pairs_Rec: enums.ResultStatus2: float Percentage of received valid IQ sample pairs related to all received IQ pairs
			- Mean_Phase_Diff: enums.ResultStatus2: No parameter help available
			- P_95_Mean_Ph_Diff: enums.ResultStatus2: No parameter help available
			- Rec_Events_Cnt: enums.ResultStatus2: decimal No. of received events
			- Pro_Events_Cnt: enums.ResultStatus2: decimal No. of processed events
			- Pro_Events_Val_Crc: enums.ResultStatus2: No parameter help available
			- Nof_Pos_Pha: enums.ResultStatus2: decimal No. of possible phase measurements determined by CTE length, slot length and number of antennas"""
		__meta_args_list = [
			ArgStruct.scalar_float_ext('Trans_Packets'),
			ArgStruct.scalar_float_ext('Rec_Events'),
			ArgStruct.scalar_float_ext('Rec_Events_Val_Crc'),
			ArgStruct.scalar_enum('No_Valid_Iqp_Airs', enums.ResultStatus2),
			ArgStruct.scalar_enum('Valid_Iq_Pairs_Rec', enums.ResultStatus2),
			ArgStruct.scalar_enum('Mean_Phase_Diff', enums.ResultStatus2),
			ArgStruct.scalar_enum('P_95_Mean_Ph_Diff', enums.ResultStatus2),
			ArgStruct.scalar_enum('Rec_Events_Cnt', enums.ResultStatus2),
			ArgStruct.scalar_enum('Pro_Events_Cnt', enums.ResultStatus2),
			ArgStruct.scalar_enum('Pro_Events_Val_Crc', enums.ResultStatus2),
			ArgStruct.scalar_enum('Nof_Pos_Pha', enums.ResultStatus2)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Trans_Packets: float or bool = None
			self.Rec_Events: float or bool = None
			self.Rec_Events_Val_Crc: float or bool = None
			self.No_Valid_Iqp_Airs: enums.ResultStatus2 = None
			self.Valid_Iq_Pairs_Rec: enums.ResultStatus2 = None
			self.Mean_Phase_Diff: enums.ResultStatus2 = None
			self.P_95_Mean_Ph_Diff: enums.ResultStatus2 = None
			self.Rec_Events_Cnt: enums.ResultStatus2 = None
			self.Pro_Events_Cnt: enums.ResultStatus2 = None
			self.Pro_Events_Val_Crc: enums.ResultStatus2 = None
			self.Nof_Pos_Pha: enums.ResultStatus2 = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LENergy:LE1M:A3NReference \n
		Snippet: value: CalculateStruct = driver.rxQuality.iqCoherency.lowEnergy.le1M.a3Nreference.calculate() \n
		Returns the results of IQ samples coherency RP(m) measurement for the specified non-reference antenna. Commands for
		uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. Commands for the mandatory non-reference antenna (.
		..:A1NReference) , and optional third (...:A2NReference) and fourth (...:A3NReference) antennas are available. The values
		described below are returned by FETCh and READ commands. CALCulate commands return limit check results instead, one value
		for each result listed below. \n
		Use RsCmwBluetoothSig.reliability.last_value to read the updated reliability indicator. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LENergy:LE1M:A3NReference?', self.__class__.CalculateStruct())
