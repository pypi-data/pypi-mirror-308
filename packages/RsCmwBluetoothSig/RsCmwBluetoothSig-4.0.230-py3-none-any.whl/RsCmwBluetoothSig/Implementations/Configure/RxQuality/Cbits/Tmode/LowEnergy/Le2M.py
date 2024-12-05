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

	def set(self, no_bits_to_corrupt: int, byte_start_err: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:CBITs:TMODe:LENergy:LE2M \n
		Snippet: driver.configure.rxQuality.cbits.tmode.lowEnergy.le2M.set(no_bits_to_corrupt = 1, byte_start_err = 1) \n
		No command help available \n
			:param no_bits_to_corrupt: No help available
			:param byte_start_err: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('no_bits_to_corrupt', no_bits_to_corrupt, DataType.Integer), ArgSingle('byte_start_err', byte_start_err, DataType.Integer))
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:CBITs:TMODe:LENergy:LE2M {param}'.rstrip())

	# noinspection PyTypeChecker
	class Le2MStruct(StructBase):
		"""Response structure. Fields: \n
			- No_Bits_To_Corrupt: int: No parameter help available
			- Byte_Start_Err: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('No_Bits_To_Corrupt'),
			ArgStruct.scalar_int('Byte_Start_Err')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.No_Bits_To_Corrupt: int = None
			self.Byte_Start_Err: int = None

	def get(self) -> Le2MStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:CBITs:TMODe:LENergy:LE2M \n
		Snippet: value: Le2MStruct = driver.configure.rxQuality.cbits.tmode.lowEnergy.le2M.get() \n
		No command help available \n
			:return: structure: for return value, see the help for Le2MStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:CBITs:TMODe:LENergy:LE2M?', self.__class__.Le2MStruct())
