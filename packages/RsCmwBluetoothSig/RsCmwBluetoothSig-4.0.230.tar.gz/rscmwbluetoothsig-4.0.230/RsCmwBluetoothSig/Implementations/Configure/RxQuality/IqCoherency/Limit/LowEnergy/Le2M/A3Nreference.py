from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class A3NreferenceCls:
	"""A3Nreference commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("a3Nreference", core, parent)

	def set(self, limit: float or bool, enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE2M:A3NReference \n
		Snippet: driver.configure.rxQuality.iqCoherency.limit.lowEnergy.le2M.a3Nreference.set(limit = 1.0, enable = False) \n
		Defines the IQ samples coherency limit for 95% relative phase values RP(m) for non-reference antennas A1NReference to
		A3NReference. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:param limit: (float or boolean) numeric Range: 0 (Rad) to 3.14 (Rad)
			:param enable: OFF | ON Disables/enables the limit check
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('limit', limit, DataType.FloatExt), ArgSingle('enable', enable, DataType.Boolean))
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE2M:A3NReference {param}'.rstrip())

	# noinspection PyTypeChecker
	class A3NreferenceStruct(StructBase):
		"""Response structure. Fields: \n
			- Limit: float or bool: numeric Range: 0 (Rad) to 3.14 (Rad)
			- Enable: bool: OFF | ON Disables/enables the limit check"""
		__meta_args_list = [
			ArgStruct.scalar_float_ext('Limit'),
			ArgStruct.scalar_bool('Enable')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Limit: float or bool = None
			self.Enable: bool = None

	def get(self) -> A3NreferenceStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE2M:A3NReference \n
		Snippet: value: A3NreferenceStruct = driver.configure.rxQuality.iqCoherency.limit.lowEnergy.le2M.a3Nreference.get() \n
		Defines the IQ samples coherency limit for 95% relative phase values RP(m) for non-reference antennas A1NReference to
		A3NReference. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:return: structure: for return value, see the help for A3NreferenceStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:LIMit:LENergy:LE2M:A3NReference?', self.__class__.A3NreferenceStruct())
