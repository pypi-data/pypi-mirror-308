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
			- Ant_3_Minus_2: float: float MeanAmplitudeANT3 - MeanAmplitudeANT2 Range: -256 to 128
			- Ant_2_Minus_Ref: float: float MeanAmplitudeANT2 - MeanAmplitudeANT0 Range: -256 to 128
			- Ant_Ref_Minus_1: float: float MeanAmplitudeANT0 - MeanAmplitudeANT1 Range: -256 to 128"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Ant_3_Minus_2'),
			ArgStruct.scalar_float('Ant_2_Minus_Ref'),
			ArgStruct.scalar_float('Ant_Ref_Minus_1')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Ant_3_Minus_2: float = None
			self.Ant_2_Minus_Ref: float = None
			self.Ant_Ref_Minus_1: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:ANTMeanamp:LENergy:LE1M \n
		Snippet: value: ResultData = driver.rxQuality.iqDrange.antMeanAmp.lowEnergy.le1M.read() \n
		Returns the results of IQ dynamic range Rx measurement for the antenna mean amplitude differences. Commands for uncoded
		LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. The values described below are returned by FETCh and READ
		commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:ANTMeanamp:LENergy:LE1M?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:ANTMeanamp:LENergy:LE1M \n
		Snippet: value: ResultData = driver.rxQuality.iqDrange.antMeanAmp.lowEnergy.le1M.fetch() \n
		Returns the results of IQ dynamic range Rx measurement for the antenna mean amplitude differences. Commands for uncoded
		LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. The values described below are returned by FETCh and READ
		commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:ANTMeanamp:LENergy:LE1M?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal See 'Reliability indicator'
			- Ant_3_Minus_2: float or bool: float MeanAmplitudeANT3 - MeanAmplitudeANT2 Range: -256 to 128
			- Ant_2_Minus_Ref: float or bool: float MeanAmplitudeANT2 - MeanAmplitudeANT0 Range: -256 to 128
			- Ant_Ref_Minus_1: float or bool: float MeanAmplitudeANT0 - MeanAmplitudeANT1 Range: -256 to 128"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float_ext('Ant_3_Minus_2'),
			ArgStruct.scalar_float_ext('Ant_2_Minus_Ref'),
			ArgStruct.scalar_float_ext('Ant_Ref_Minus_1')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Ant_3_Minus_2: float or bool = None
			self.Ant_2_Minus_Ref: float or bool = None
			self.Ant_Ref_Minus_1: float or bool = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:ANTMeanamp:LENergy:LE1M \n
		Snippet: value: CalculateStruct = driver.rxQuality.iqDrange.antMeanAmp.lowEnergy.le1M.calculate() \n
		Returns the results of IQ dynamic range Rx measurement for the antenna mean amplitude differences. Commands for uncoded
		LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. The values described below are returned by FETCh and READ
		commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:ANTMeanamp:LENergy:LE1M?', self.__class__.CalculateStruct())
