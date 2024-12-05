from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	def set(self, cmw_rx_frequency: float, cmw_tx_frequency: float) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:FREQuency \n
		Snippet: driver.diagnostic.ucs.frequency.set(cmw_rx_frequency = 1.0, cmw_tx_frequency = 1.0) \n
		No command help available \n
			:param cmw_rx_frequency: No help available
			:param cmw_tx_frequency: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cmw_rx_frequency', cmw_rx_frequency, DataType.Float), ArgSingle('cmw_tx_frequency', cmw_tx_frequency, DataType.Float))
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:FREQuency {param}'.rstrip())

	# noinspection PyTypeChecker
	class FrequencyStruct(StructBase):
		"""Response structure. Fields: \n
			- Cmw_Rx_Frequency: float: No parameter help available
			- Cmw_Tx_Frequency: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Cmw_Rx_Frequency'),
			ArgStruct.scalar_float('Cmw_Tx_Frequency')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Cmw_Rx_Frequency: float = None
			self.Cmw_Tx_Frequency: float = None

	def get(self) -> FrequencyStruct:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:FREQuency \n
		Snippet: value: FrequencyStruct = driver.diagnostic.ucs.frequency.get() \n
		No command help available \n
			:return: structure: for return value, see the help for FrequencyStruct structure arguments."""
		return self._core.io.query_struct(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:FREQuency?', self.__class__.FrequencyStruct())
