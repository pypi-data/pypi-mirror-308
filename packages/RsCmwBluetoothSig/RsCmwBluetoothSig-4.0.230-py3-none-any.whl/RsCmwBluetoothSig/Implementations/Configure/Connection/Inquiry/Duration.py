from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DurationCls:
	"""Duration commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("duration", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:DURation:LESignaling \n
		Snippet: value: int = driver.configure.connection.inquiry.duration.get_le_signaling() \n
		Specifies the total inquiry duration. \n
			:return: inq_duration: numeric Range: 5 ms to 30E+3 ms
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:DURation:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, inq_duration: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:DURation:LESignaling \n
		Snippet: driver.configure.connection.inquiry.duration.set_le_signaling(inq_duration = 1) \n
		Specifies the total inquiry duration. \n
			:param inq_duration: numeric Range: 5 ms to 30E+3 ms
		"""
		param = Conversions.decimal_value_to_str(inq_duration)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:DURation:LESignaling {param}')
