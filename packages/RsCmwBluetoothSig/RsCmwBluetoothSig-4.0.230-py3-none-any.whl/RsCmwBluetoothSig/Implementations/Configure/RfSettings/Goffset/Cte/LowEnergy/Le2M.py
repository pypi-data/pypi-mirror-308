from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Le2MCls:
	"""Le2M commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("le2M", core, parent)

	def set(self, ant_1_gain_offset: float, ant_2_gain_offset: float, ant_3_gain_offset: float) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:GOFFset:CTE:LENergy:LE2M \n
		Snippet: driver.configure.rfSettings.goffset.cte.lowEnergy.le2M.set(ant_1_gain_offset = 1.0, ant_2_gain_offset = 1.0, ant_3_gain_offset = 1.0) \n
		Specifies the gain offset for non-reference antennas relative to the gain (or attenuation) of reference antenna for IQ
		sample dynamic range measurements. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:param ant_1_gain_offset: numeric Range: -20 dB to 6 dB
			:param ant_2_gain_offset: numeric Range: -20 dB to 6 dB
			:param ant_3_gain_offset: numeric Range: -20 dB to 6 dB
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('ant_1_gain_offset', ant_1_gain_offset, DataType.Float), ArgSingle('ant_2_gain_offset', ant_2_gain_offset, DataType.Float), ArgSingle('ant_3_gain_offset', ant_3_gain_offset, DataType.Float))
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:GOFFset:CTE:LENergy:LE2M {param}'.rstrip())

	# noinspection PyTypeChecker
	class Le2MStruct(StructBase):
		"""Response structure. Fields: \n
			- Ant_1_Gain_Offset: float: numeric Range: -20 dB to 6 dB
			- Ant_2_Gain_Offset: float: numeric Range: -20 dB to 6 dB
			- Ant_3_Gain_Offset: float: numeric Range: -20 dB to 6 dB"""
		__meta_args_list = [
			ArgStruct.scalar_float('Ant_1_Gain_Offset'),
			ArgStruct.scalar_float('Ant_2_Gain_Offset'),
			ArgStruct.scalar_float('Ant_3_Gain_Offset')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ant_1_Gain_Offset: float = None
			self.Ant_2_Gain_Offset: float = None
			self.Ant_3_Gain_Offset: float = None

	def get(self) -> Le2MStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:GOFFset:CTE:LENergy:LE2M \n
		Snippet: value: Le2MStruct = driver.configure.rfSettings.goffset.cte.lowEnergy.le2M.get() \n
		Specifies the gain offset for non-reference antennas relative to the gain (or attenuation) of reference antenna for IQ
		sample dynamic range measurements. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:return: structure: for return value, see the help for Le2MStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:GOFFset:CTE:LENergy:LE2M?', self.__class__.Le2MStruct())
