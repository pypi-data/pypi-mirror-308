from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AdpCls:
	"""Adp commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("adp", core, parent)

	# noinspection PyTypeChecker
	class SbcStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- S_16_K: bool: No parameter help available
			- S_32_K: bool: No parameter help available
			- S_44_K: bool: No parameter help available
			- S_48_K: bool: No parameter help available
			- Cmmn: bool: No parameter help available
			- Cmdl: bool: No parameter help available
			- Cmst: bool: No parameter help available
			- Cmjs: bool: No parameter help available
			- B_04_B: bool: No parameter help available
			- B_08_B: bool: No parameter help available
			- B_12_B: bool: No parameter help available
			- B_16_B: bool: No parameter help available
			- Sb_4_B: bool: No parameter help available
			- Sb_8_B: bool: No parameter help available
			- Allocation: enums.AllocMethod: No parameter help available
			- Min_Bit_Pool: int: No parameter help available
			- Max_Bit_Pool: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('S_16_K'),
			ArgStruct.scalar_bool('S_32_K'),
			ArgStruct.scalar_bool('S_44_K'),
			ArgStruct.scalar_bool('S_48_K'),
			ArgStruct.scalar_bool('Cmmn'),
			ArgStruct.scalar_bool('Cmdl'),
			ArgStruct.scalar_bool('Cmst'),
			ArgStruct.scalar_bool('Cmjs'),
			ArgStruct.scalar_bool('B_04_B'),
			ArgStruct.scalar_bool('B_08_B'),
			ArgStruct.scalar_bool('B_12_B'),
			ArgStruct.scalar_bool('B_16_B'),
			ArgStruct.scalar_bool('Sb_4_B'),
			ArgStruct.scalar_bool('Sb_8_B'),
			ArgStruct.scalar_enum('Allocation', enums.AllocMethod),
			ArgStruct.scalar_int('Min_Bit_Pool'),
			ArgStruct.scalar_int('Max_Bit_Pool')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.S_16_K: bool = None
			self.S_32_K: bool = None
			self.S_44_K: bool = None
			self.S_48_K: bool = None
			self.Cmmn: bool = None
			self.Cmdl: bool = None
			self.Cmst: bool = None
			self.Cmjs: bool = None
			self.B_04_B: bool = None
			self.B_08_B: bool = None
			self.B_12_B: bool = None
			self.B_16_B: bool = None
			self.Sb_4_B: bool = None
			self.Sb_8_B: bool = None
			self.Allocation: enums.AllocMethod = None
			self.Min_Bit_Pool: int = None
			self.Max_Bit_Pool: int = None

	def get_sbc(self) -> SbcStruct:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:ADP[:SBC] \n
		Snippet: value: SbcStruct = driver.sense.eut.capability.adp.get_sbc() \n
		No command help available \n
			:return: structure: for return value, see the help for SbcStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:BLUetooth:SIGNaling<Instance>:EUT:CAPability:ADP:SBC?', self.__class__.SbcStruct())
