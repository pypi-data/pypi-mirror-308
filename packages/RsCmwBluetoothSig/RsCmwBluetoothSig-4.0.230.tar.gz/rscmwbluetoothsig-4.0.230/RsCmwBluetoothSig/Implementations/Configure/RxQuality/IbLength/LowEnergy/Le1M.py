from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Le1MCls:
	"""Le1M commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("le1M", core, parent)

	def set(self, enable: bool, inter_burst_len: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IBLength:LENergy:LE1M \n
		Snippet: driver.configure.rxQuality.ibLength.lowEnergy.le1M.set(enable = False, inter_burst_len = 1) \n
		Enables and sets the number of slots to wait between transmissions for direction finding tests. \n
			:param enable: OFF | ON
			:param inter_burst_len: integer Range: 0 slot(s) to 255 slot(s)
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('inter_burst_len', inter_burst_len, DataType.Integer))
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IBLength:LENergy:LE1M {param}'.rstrip())

	# noinspection PyTypeChecker
	class Le1MStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON
			- Inter_Burst_Len: int: integer Range: 0 slot(s) to 255 slot(s)"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_int('Inter_Burst_Len')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Inter_Burst_Len: int = None

	def get(self) -> Le1MStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IBLength:LENergy:LE1M \n
		Snippet: value: Le1MStruct = driver.configure.rxQuality.ibLength.lowEnergy.le1M.get() \n
		Enables and sets the number of slots to wait between transmissions for direction finding tests. \n
			:return: structure: for return value, see the help for Le1MStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IBLength:LENergy:LE1M?', self.__class__.Le1MStruct())
