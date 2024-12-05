from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LoopbackCls:
	"""Loopback commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("loopback", core, parent)

	def set(self, rx_chan: int, tx_chan: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:LOOPback \n
		Snippet: driver.configure.rfSettings.channel.loopback.set(rx_chan = 1, tx_chan = 1) \n
		Defines the channels used by the loopback test. \n
			:param rx_chan: numeric Range: 0 Ch to 78 Ch
			:param tx_chan: numeric Range: 0 Ch to 78 Ch
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('rx_chan', rx_chan, DataType.Integer), ArgSingle('tx_chan', tx_chan, DataType.Integer))
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:LOOPback {param}'.rstrip())

	# noinspection PyTypeChecker
	class LoopbackStruct(StructBase):
		"""Response structure. Fields: \n
			- Rx_Chan: int: numeric Range: 0 Ch to 78 Ch
			- Tx_Chan: int: numeric Range: 0 Ch to 78 Ch"""
		__meta_args_list = [
			ArgStruct.scalar_int('Rx_Chan'),
			ArgStruct.scalar_int('Tx_Chan')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rx_Chan: int = None
			self.Tx_Chan: int = None

	def get(self) -> LoopbackStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:LOOPback \n
		Snippet: value: LoopbackStruct = driver.configure.rfSettings.channel.loopback.get() \n
		Defines the channels used by the loopback test. \n
			:return: structure: for return value, see the help for LoopbackStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:LOOPback?', self.__class__.LoopbackStruct())
