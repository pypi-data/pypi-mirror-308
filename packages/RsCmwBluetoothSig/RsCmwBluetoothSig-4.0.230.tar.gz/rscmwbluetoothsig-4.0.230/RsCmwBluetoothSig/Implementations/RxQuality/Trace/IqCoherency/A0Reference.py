from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class A0ReferenceCls:
	"""A0Reference commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("a0Reference", core, parent)

	def read(self) -> List[float]:
		"""SCPI: READ:BLUetooth:SIGNaling<Instance>:RXQuality:TRACe:IQCoherency:A0Reference \n
		Snippet: value: List[float] = driver.rxQuality.trace.iqCoherency.a0Reference.read() \n
		Return the trace results of reference phase deviation RPD for IQ samples coherency measured at antenna 0. \n
		Use RsCmwBluetoothSig.reliability.last_value to read the updated reliability indicator. \n
			:return: mrp: float 720 RPD results, one result per IQ sample slot."""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:BLUetooth:SIGNaling<Instance>:RXQuality:TRACe:IQCoherency:A0Reference?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:TRACe:IQCoherency:A0Reference \n
		Snippet: value: List[float] = driver.rxQuality.trace.iqCoherency.a0Reference.fetch() \n
		Return the trace results of reference phase deviation RPD for IQ samples coherency measured at antenna 0. \n
		Use RsCmwBluetoothSig.reliability.last_value to read the updated reliability indicator. \n
			:return: mrp: float 720 RPD results, one result per IQ sample slot."""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:TRACe:IQCoherency:A0Reference?', suppressed)
		return response
