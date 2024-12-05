from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Le2MCls:
	"""Le2M commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("le2M", core, parent)

	def set(self, ant_3_minus_2_enable: bool, ant_2_minus_ref_enable: bool, ant_ref_minus_1_enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:ANTMeanamp:LIMit:LENergy:LE2M \n
		Snippet: driver.configure.rxQuality.iqDrange.antMeanAmp.limit.lowEnergy.le2M.set(ant_3_minus_2_enable = False, ant_2_minus_ref_enable = False, ant_ref_minus_1_enable = False) \n
		Disables/enables the limit check for the IQ dynamic range results to monitor the requirement: MeanANT3 < MeanANT2 <
		MeanANT0 < MeanANT1 \n
			:param ant_3_minus_2_enable: No help available
			:param ant_2_minus_ref_enable: No help available
			:param ant_ref_minus_1_enable: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('ant_3_minus_2_enable', ant_3_minus_2_enable, DataType.Boolean), ArgSingle('ant_2_minus_ref_enable', ant_2_minus_ref_enable, DataType.Boolean), ArgSingle('ant_ref_minus_1_enable', ant_ref_minus_1_enable, DataType.Boolean))
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:ANTMeanamp:LIMit:LENergy:LE2M {param}'.rstrip())

	# noinspection PyTypeChecker
	class Le2MStruct(StructBase):
		"""Response structure. Fields: \n
			- Ant_3_Minus_2_Enable: bool: No parameter help available
			- Ant_2_Minus_Ref_Enable: bool: No parameter help available
			- Ant_Ref_Minus_1_Enable: bool: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Ant_3_Minus_2_Enable'),
			ArgStruct.scalar_bool('Ant_2_Minus_Ref_Enable'),
			ArgStruct.scalar_bool('Ant_Ref_Minus_1_Enable')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ant_3_Minus_2_Enable: bool = None
			self.Ant_2_Minus_Ref_Enable: bool = None
			self.Ant_Ref_Minus_1_Enable: bool = None

	def get(self) -> Le2MStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:ANTMeanamp:LIMit:LENergy:LE2M \n
		Snippet: value: Le2MStruct = driver.configure.rxQuality.iqDrange.antMeanAmp.limit.lowEnergy.le2M.get() \n
		Disables/enables the limit check for the IQ dynamic range results to monitor the requirement: MeanANT3 < MeanANT2 <
		MeanANT0 < MeanANT1 \n
			:return: structure: for return value, see the help for Le2MStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:ANTMeanamp:LIMit:LENergy:LE2M?', self.__class__.Le2MStruct())
