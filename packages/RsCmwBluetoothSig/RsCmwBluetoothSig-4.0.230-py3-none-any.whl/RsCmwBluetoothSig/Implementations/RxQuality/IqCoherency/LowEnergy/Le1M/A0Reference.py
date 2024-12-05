from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class A0ReferenceCls:
	"""A0Reference commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("a0Reference", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal See 'Reliability indicator'
			- Trans_Packets: int: decimal No. of transmitted packets Range: 0 to 200E+6
			- Rec_Events: float: No parameter help available
			- Rec_Events_Val_Crc: int: No parameter help available
			- No_Valid_Iqp_Airs: int: decimal No. of received valid IQ sample pairs
			- Valid_Iq_Pairs_Rec: float: float Percentage of received valid IQ sample pairs related to all received IQ pairs
			- Mean_Phase_Diff: float: float Mean current phase difference Unit: rad/Pi
			- Rec_Events_Cnt: int: decimal No. of received events
			- Pro_Events_Cnt: int: decimal No. of processed events
			- Pro_Events_Val_Crc: int: No parameter help available
			- Nof_Pos_Pha: int: decimal No. of possible phase measurements determined by CTE length, slot length and number of antennas
			- Mrpd_Avg: float: float Mean reference phase deviation (RPD) - average value
			- Mrpd_Min: float: float Mean RPD - minimum value
			- Mrpd_Max: float: float Mean RPD - maximum value"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Trans_Packets'),
			ArgStruct.scalar_float('Rec_Events'),
			ArgStruct.scalar_int('Rec_Events_Val_Crc'),
			ArgStruct.scalar_int('No_Valid_Iqp_Airs'),
			ArgStruct.scalar_float('Valid_Iq_Pairs_Rec'),
			ArgStruct.scalar_float('Mean_Phase_Diff'),
			ArgStruct.scalar_int('Rec_Events_Cnt'),
			ArgStruct.scalar_int('Pro_Events_Cnt'),
			ArgStruct.scalar_int('Pro_Events_Val_Crc'),
			ArgStruct.scalar_int('Nof_Pos_Pha'),
			ArgStruct.scalar_float('Mrpd_Avg'),
			ArgStruct.scalar_float('Mrpd_Min'),
			ArgStruct.scalar_float('Mrpd_Max')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Trans_Packets: int = None
			self.Rec_Events: float = None
			self.Rec_Events_Val_Crc: int = None
			self.No_Valid_Iqp_Airs: int = None
			self.Valid_Iq_Pairs_Rec: float = None
			self.Mean_Phase_Diff: float = None
			self.Rec_Events_Cnt: int = None
			self.Pro_Events_Cnt: int = None
			self.Pro_Events_Val_Crc: int = None
			self.Nof_Pos_Pha: int = None
			self.Mrpd_Avg: float = None
			self.Mrpd_Min: float = None
			self.Mrpd_Max: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LENergy:LE1M:A0Reference \n
		Snippet: value: ResultData = driver.rxQuality.iqCoherency.lowEnergy.le1M.a0Reference.read() \n
		Return the results of IQ samples coherency RPD measurements for the reference antenna. Commands for uncoded LE 1M PHY (..
		:LE1M..) and LE 2M PHY (..:LE2M..) are available. The values described below are returned by FETCh and READ commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LENergy:LE1M:A0Reference?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LENergy:LE1M:A0Reference \n
		Snippet: value: ResultData = driver.rxQuality.iqCoherency.lowEnergy.le1M.a0Reference.fetch() \n
		Return the results of IQ samples coherency RPD measurements for the reference antenna. Commands for uncoded LE 1M PHY (..
		:LE1M..) and LE 2M PHY (..:LE2M..) are available. The values described below are returned by FETCh and READ commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LENergy:LE1M:A0Reference?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal See 'Reliability indicator'
			- Trans_Packets: float or bool: decimal No. of transmitted packets Range: 0 to 200E+6
			- Rec_Events: float or bool: No parameter help available
			- Rec_Events_Val_Crc: float or bool: No parameter help available
			- No_Valid_Iqp_Airs: enums.ResultStatus2: decimal No. of received valid IQ sample pairs
			- Valid_Iq_Pairs_Rec: enums.ResultStatus2: float Percentage of received valid IQ sample pairs related to all received IQ pairs
			- Mean_Phase_Diff: enums.ResultStatus2: float Mean current phase difference Unit: rad/Pi
			- Rec_Events_Cnt: enums.ResultStatus2: decimal No. of received events
			- Pro_Events_Cnt: enums.ResultStatus2: decimal No. of processed events
			- Pro_Events_Val_Crc: enums.ResultStatus2: No parameter help available
			- Nof_Pos_Pha: enums.ResultStatus2: decimal No. of possible phase measurements determined by CTE length, slot length and number of antennas
			- Mrpd_Avg: enums.ResultStatus2: float Mean reference phase deviation (RPD) - average value
			- Mrpd_Min: enums.ResultStatus2: float Mean RPD - minimum value
			- Mrpd_Max: enums.ResultStatus2: float Mean RPD - maximum value"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float_ext('Trans_Packets'),
			ArgStruct.scalar_float_ext('Rec_Events'),
			ArgStruct.scalar_float_ext('Rec_Events_Val_Crc'),
			ArgStruct.scalar_enum('No_Valid_Iqp_Airs', enums.ResultStatus2),
			ArgStruct.scalar_enum('Valid_Iq_Pairs_Rec', enums.ResultStatus2),
			ArgStruct.scalar_enum('Mean_Phase_Diff', enums.ResultStatus2),
			ArgStruct.scalar_enum('Rec_Events_Cnt', enums.ResultStatus2),
			ArgStruct.scalar_enum('Pro_Events_Cnt', enums.ResultStatus2),
			ArgStruct.scalar_enum('Pro_Events_Val_Crc', enums.ResultStatus2),
			ArgStruct.scalar_enum('Nof_Pos_Pha', enums.ResultStatus2),
			ArgStruct.scalar_enum('Mrpd_Avg', enums.ResultStatus2),
			ArgStruct.scalar_enum('Mrpd_Min', enums.ResultStatus2),
			ArgStruct.scalar_enum('Mrpd_Max', enums.ResultStatus2)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Trans_Packets: float or bool = None
			self.Rec_Events: float or bool = None
			self.Rec_Events_Val_Crc: float or bool = None
			self.No_Valid_Iqp_Airs: enums.ResultStatus2 = None
			self.Valid_Iq_Pairs_Rec: enums.ResultStatus2 = None
			self.Mean_Phase_Diff: enums.ResultStatus2 = None
			self.Rec_Events_Cnt: enums.ResultStatus2 = None
			self.Pro_Events_Cnt: enums.ResultStatus2 = None
			self.Pro_Events_Val_Crc: enums.ResultStatus2 = None
			self.Nof_Pos_Pha: enums.ResultStatus2 = None
			self.Mrpd_Avg: enums.ResultStatus2 = None
			self.Mrpd_Min: enums.ResultStatus2 = None
			self.Mrpd_Max: enums.ResultStatus2 = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LENergy:LE1M:A0Reference \n
		Snippet: value: CalculateStruct = driver.rxQuality.iqCoherency.lowEnergy.le1M.a0Reference.calculate() \n
		Return the results of IQ samples coherency RPD measurements for the reference antenna. Commands for uncoded LE 1M PHY (..
		:LE1M..) and LE 2M PHY (..:LE2M..) are available. The values described below are returned by FETCh and READ commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LENergy:LE1M:A0Reference?', self.__class__.CalculateStruct())
