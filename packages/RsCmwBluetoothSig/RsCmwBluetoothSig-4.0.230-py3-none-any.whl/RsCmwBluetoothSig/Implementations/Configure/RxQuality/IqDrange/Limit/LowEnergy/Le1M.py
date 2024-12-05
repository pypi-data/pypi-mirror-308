from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Le1MCls:
	"""Le1M commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("le1M", core, parent)

	def set(self, ref_ant_enable: bool, ant_1_enable: bool, ant_2_enable: bool, ant_3_enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:LIMit:LENergy:LE1M \n
		Snippet: driver.configure.rxQuality.iqDrange.limit.lowEnergy.le1M.set(ref_ant_enable = False, ant_1_enable = False, ant_2_enable = False, ant_3_enable = False) \n
		No command help available \n
			:param ref_ant_enable: No help available
			:param ant_1_enable: No help available
			:param ant_2_enable: No help available
			:param ant_3_enable: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('ref_ant_enable', ref_ant_enable, DataType.Boolean), ArgSingle('ant_1_enable', ant_1_enable, DataType.Boolean), ArgSingle('ant_2_enable', ant_2_enable, DataType.Boolean), ArgSingle('ant_3_enable', ant_3_enable, DataType.Boolean))
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:LIMit:LENergy:LE1M {param}'.rstrip())

	# noinspection PyTypeChecker
	class Le1MStruct(StructBase):
		"""Response structure. Fields: \n
			- Ref_Ant_Enable: bool: No parameter help available
			- Ant_1_Enable: bool: No parameter help available
			- Ant_2_Enable: bool: No parameter help available
			- Ant_3_Enable: bool: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Ref_Ant_Enable'),
			ArgStruct.scalar_bool('Ant_1_Enable'),
			ArgStruct.scalar_bool('Ant_2_Enable'),
			ArgStruct.scalar_bool('Ant_3_Enable')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ref_Ant_Enable: bool = None
			self.Ant_1_Enable: bool = None
			self.Ant_2_Enable: bool = None
			self.Ant_3_Enable: bool = None

	def get(self) -> Le1MStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:LIMit:LENergy:LE1M \n
		Snippet: value: Le1MStruct = driver.configure.rxQuality.iqDrange.limit.lowEnergy.le1M.get() \n
		No command help available \n
			:return: structure: for return value, see the help for Le1MStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:LIMit:LENergy:LE1M?', self.__class__.Le1MStruct())
