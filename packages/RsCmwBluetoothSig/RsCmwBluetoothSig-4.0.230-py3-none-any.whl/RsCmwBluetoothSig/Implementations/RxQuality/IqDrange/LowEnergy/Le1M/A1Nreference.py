from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class A1NreferenceCls:
	"""A1Nreference commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("a1Nreference", core, parent)

	# noinspection PyTypeChecker
	class ReadStruct(StructBase):
		"""Response structure. Fields: \n
			- Trans_Packets: float: decimal No. of transmitted packets Range: 0 to 200E+6
			- Rec_Events: float: No parameter help available
			- Rec_Events_Val_Crc: float: No parameter help available
			- No_Valid_Iqp_Airs: float: decimal No. of valid measurements Range: 0 to 100E+3
			- Valid_Iq_Pairs_Rec: float: float Percentage of received valid IQ sample pairs related to all received IQ pairs Range: 0 % to 100 % , Unit: %
			- Mean_Amplitude: float: float Mean amplitude Range: 0 to 1 , Unit: dBFS
			- Max_Amplitude: float: float Max amplitude Range: 0 to 1 , Unit: dBFS
			- Rec_Events_Cnt: int: decimal No. of received events
			- Pro_Events_Cnt: int: decimal No. of processed events
			- Pro_Events_Val_Crc: int: No parameter help available
			- Nof_Pos_Amp: int: decimal No. of possible amplitude measurements determined by CTE length, slot length and number of antennas"""
		__meta_args_list = [
			ArgStruct.scalar_float('Trans_Packets'),
			ArgStruct.scalar_float('Rec_Events'),
			ArgStruct.scalar_float('Rec_Events_Val_Crc'),
			ArgStruct.scalar_float('No_Valid_Iqp_Airs'),
			ArgStruct.scalar_float('Valid_Iq_Pairs_Rec'),
			ArgStruct.scalar_float('Mean_Amplitude'),
			ArgStruct.scalar_float('Max_Amplitude'),
			ArgStruct.scalar_int('Rec_Events_Cnt'),
			ArgStruct.scalar_int('Pro_Events_Cnt'),
			ArgStruct.scalar_int('Pro_Events_Val_Crc'),
			ArgStruct.scalar_int('Nof_Pos_Amp')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Trans_Packets: float = None
			self.Rec_Events: float = None
			self.Rec_Events_Val_Crc: float = None
			self.No_Valid_Iqp_Airs: float = None
			self.Valid_Iq_Pairs_Rec: float = None
			self.Mean_Amplitude: float = None
			self.Max_Amplitude: float = None
			self.Rec_Events_Cnt: int = None
			self.Pro_Events_Cnt: int = None
			self.Pro_Events_Val_Crc: int = None
			self.Nof_Pos_Amp: int = None

	def read(self) -> ReadStruct:
		"""SCPI: READ:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:LENergy:LE1M:A1NReference \n
		Snippet: value: ReadStruct = driver.rxQuality.iqDrange.lowEnergy.le1M.a1Nreference.read() \n
		Returns the results of IQ dynamic range Rx measurement for the specified antenna. Commands for uncoded LE 1M PHY (..:LE1M.
		.) and LE 2M PHY (..:LE2M..) are available. Commands for reference antenna (...:A0Reference) , mandatory second
		non-reference antenna (...:A1NReference) , and optional third and fourth non-reference antennas are available. The values
		described below are returned by FETCh and READ commands. CALCulate commands return limit check results instead, one value
		for each result listed below. \n
		Use RsCmwBluetoothSig.reliability.last_value to read the updated reliability indicator. \n
			:return: structure: for return value, see the help for ReadStruct structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:LENergy:LE1M:A1NReference?', self.__class__.ReadStruct())

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Trans_Packets: int: decimal No. of transmitted packets Range: 0 to 200E+6
			- Rec_Events: float: No parameter help available
			- Rec_Events_Val_Crc: int: No parameter help available
			- No_Valid_Iqp_Airs: int: decimal No. of valid measurements Range: 0 to 100E+3
			- Valid_Iq_Pairs_Rec: float: float Percentage of received valid IQ sample pairs related to all received IQ pairs Range: 0 % to 100 % , Unit: %
			- Mean_Amplitude: float: float Mean amplitude Range: 0 to 1 , Unit: dBFS
			- Max_Amplitude: float: float Max amplitude Range: 0 to 1 , Unit: dBFS
			- Rec_Events_Cnt: int: decimal No. of received events
			- Pro_Events_Cnt: int: decimal No. of processed events
			- Pro_Events_Val_Crc: int: No parameter help available
			- Nof_Pos_Amp: int: decimal No. of possible amplitude measurements determined by CTE length, slot length and number of antennas"""
		__meta_args_list = [
			ArgStruct.scalar_int('Trans_Packets'),
			ArgStruct.scalar_float('Rec_Events'),
			ArgStruct.scalar_int('Rec_Events_Val_Crc'),
			ArgStruct.scalar_int('No_Valid_Iqp_Airs'),
			ArgStruct.scalar_float('Valid_Iq_Pairs_Rec'),
			ArgStruct.scalar_float('Mean_Amplitude'),
			ArgStruct.scalar_float('Max_Amplitude'),
			ArgStruct.scalar_int('Rec_Events_Cnt'),
			ArgStruct.scalar_int('Pro_Events_Cnt'),
			ArgStruct.scalar_int('Pro_Events_Val_Crc'),
			ArgStruct.scalar_int('Nof_Pos_Amp')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Trans_Packets: int = None
			self.Rec_Events: float = None
			self.Rec_Events_Val_Crc: int = None
			self.No_Valid_Iqp_Airs: int = None
			self.Valid_Iq_Pairs_Rec: float = None
			self.Mean_Amplitude: float = None
			self.Max_Amplitude: float = None
			self.Rec_Events_Cnt: int = None
			self.Pro_Events_Cnt: int = None
			self.Pro_Events_Val_Crc: int = None
			self.Nof_Pos_Amp: int = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:LENergy:LE1M:A1NReference \n
		Snippet: value: FetchStruct = driver.rxQuality.iqDrange.lowEnergy.le1M.a1Nreference.fetch() \n
		Returns the results of IQ dynamic range Rx measurement for the specified antenna. Commands for uncoded LE 1M PHY (..:LE1M.
		.) and LE 2M PHY (..:LE2M..) are available. Commands for reference antenna (...:A0Reference) , mandatory second
		non-reference antenna (...:A1NReference) , and optional third and fourth non-reference antennas are available. The values
		described below are returned by FETCh and READ commands. CALCulate commands return limit check results instead, one value
		for each result listed below. \n
		Use RsCmwBluetoothSig.reliability.last_value to read the updated reliability indicator. \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:LENergy:LE1M:A1NReference?', self.__class__.FetchStruct())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Trans_Packets: float or bool: decimal No. of transmitted packets Range: 0 to 200E+6
			- Rec_Events: float or bool: No parameter help available
			- Rec_Events_Val_Crc: float or bool: No parameter help available
			- No_Valid_Iqp_Airs: enums.ResultStatus2: decimal No. of valid measurements Range: 0 to 100E+3
			- Valid_Iq_Pairs_Rec: enums.ResultStatus2: float Percentage of received valid IQ sample pairs related to all received IQ pairs Range: 0 % to 100 % , Unit: %
			- Mean_Amplitude: enums.ResultStatus2: float Mean amplitude Range: 0 to 1 , Unit: dBFS
			- Max_Amplitude: enums.ResultStatus2: float Max amplitude Range: 0 to 1 , Unit: dBFS
			- Rec_Events_Cnt: enums.ResultStatus2: decimal No. of received events
			- Pro_Events_Cnt: enums.ResultStatus2: decimal No. of processed events
			- Pro_Events_Val_Crc: enums.ResultStatus2: No parameter help available
			- Nos_Pos_Amp: enums.ResultStatus2: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float_ext('Trans_Packets'),
			ArgStruct.scalar_float_ext('Rec_Events'),
			ArgStruct.scalar_float_ext('Rec_Events_Val_Crc'),
			ArgStruct.scalar_enum('No_Valid_Iqp_Airs', enums.ResultStatus2),
			ArgStruct.scalar_enum('Valid_Iq_Pairs_Rec', enums.ResultStatus2),
			ArgStruct.scalar_enum('Mean_Amplitude', enums.ResultStatus2),
			ArgStruct.scalar_enum('Max_Amplitude', enums.ResultStatus2),
			ArgStruct.scalar_enum('Rec_Events_Cnt', enums.ResultStatus2),
			ArgStruct.scalar_enum('Pro_Events_Cnt', enums.ResultStatus2),
			ArgStruct.scalar_enum('Pro_Events_Val_Crc', enums.ResultStatus2),
			ArgStruct.scalar_enum('Nos_Pos_Amp', enums.ResultStatus2)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Trans_Packets: float or bool = None
			self.Rec_Events: float or bool = None
			self.Rec_Events_Val_Crc: float or bool = None
			self.No_Valid_Iqp_Airs: enums.ResultStatus2 = None
			self.Valid_Iq_Pairs_Rec: enums.ResultStatus2 = None
			self.Mean_Amplitude: enums.ResultStatus2 = None
			self.Max_Amplitude: enums.ResultStatus2 = None
			self.Rec_Events_Cnt: enums.ResultStatus2 = None
			self.Pro_Events_Cnt: enums.ResultStatus2 = None
			self.Pro_Events_Val_Crc: enums.ResultStatus2 = None
			self.Nos_Pos_Amp: enums.ResultStatus2 = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:LENergy:LE1M:A1NReference \n
		Snippet: value: CalculateStruct = driver.rxQuality.iqDrange.lowEnergy.le1M.a1Nreference.calculate() \n
		Returns the results of IQ dynamic range Rx measurement for the specified antenna. Commands for uncoded LE 1M PHY (..:LE1M.
		.) and LE 2M PHY (..:LE2M..) are available. Commands for reference antenna (...:A0Reference) , mandatory second
		non-reference antenna (...:A1NReference) , and optional third and fourth non-reference antennas are available. The values
		described below are returned by FETCh and READ commands. CALCulate commands return limit check results instead, one value
		for each result listed below. \n
		Use RsCmwBluetoothSig.reliability.last_value to read the updated reliability indicator. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:LENergy:LE1M:A1NReference?', self.__class__.CalculateStruct())
