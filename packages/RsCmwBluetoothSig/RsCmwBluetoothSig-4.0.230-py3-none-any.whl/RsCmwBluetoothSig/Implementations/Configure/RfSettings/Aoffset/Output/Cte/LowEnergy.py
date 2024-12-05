from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	def set(self, ant_1_out_at_offset: float, ant_2_out_at_offset: float, ant_3_out_at_offset: float) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AOFFset:OUTPut:CTE:LENergy \n
		Snippet: driver.configure.rfSettings.aoffset.output.cte.lowEnergy.set(ant_1_out_at_offset = 1.0, ant_2_out_at_offset = 1.0, ant_3_out_at_offset = 1.0) \n
		Specifies the offset of external attenuation per EUT antenna relative to the reference antenna. For the reference antenna,
		the offset is fixed and set to 0 dB. The commands for input and output path are available. An SUA is required. \n
			:param ant_1_out_at_offset: numeric Range: -3 dB to 3 dB
			:param ant_2_out_at_offset: numeric Range: -3 dB to 3 dB
			:param ant_3_out_at_offset: numeric Range: -3 dB to 3 dB
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('ant_1_out_at_offset', ant_1_out_at_offset, DataType.Float), ArgSingle('ant_2_out_at_offset', ant_2_out_at_offset, DataType.Float), ArgSingle('ant_3_out_at_offset', ant_3_out_at_offset, DataType.Float))
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AOFFset:OUTPut:CTE:LENergy {param}'.rstrip())

	# noinspection PyTypeChecker
	class LowEnergyStruct(StructBase):
		"""Response structure. Fields: \n
			- Ant_1_Out_At_Offset: float: numeric Range: -3 dB to 3 dB
			- Ant_2_Out_At_Offset: float: numeric Range: -3 dB to 3 dB
			- Ant_3_Out_At_Offset: float: numeric Range: -3 dB to 3 dB"""
		__meta_args_list = [
			ArgStruct.scalar_float('Ant_1_Out_At_Offset'),
			ArgStruct.scalar_float('Ant_2_Out_At_Offset'),
			ArgStruct.scalar_float('Ant_3_Out_At_Offset')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ant_1_Out_At_Offset: float = None
			self.Ant_2_Out_At_Offset: float = None
			self.Ant_3_Out_At_Offset: float = None

	def get(self) -> LowEnergyStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AOFFset:OUTPut:CTE:LENergy \n
		Snippet: value: LowEnergyStruct = driver.configure.rfSettings.aoffset.output.cte.lowEnergy.get() \n
		Specifies the offset of external attenuation per EUT antenna relative to the reference antenna. For the reference antenna,
		the offset is fixed and set to 0 dB. The commands for input and output path are available. An SUA is required. \n
			:return: structure: for return value, see the help for LowEnergyStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AOFFset:OUTPut:CTE:LENergy?', self.__class__.LowEnergyStruct())
