from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SvTimeoutCls:
	"""SvTimeout commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("svTimeout", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SVTimeout:LESignaling \n
		Snippet: value: int = driver.configure.connection.svTimeout.get_le_signaling() \n
		Specifies the duration of tolerated connection breaks down. \n
			:return: supervision_timeout: numeric Range: 100 ms to 32E+3 ms, Unit: ms
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SVTimeout:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, supervision_timeout: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SVTimeout:LESignaling \n
		Snippet: driver.configure.connection.svTimeout.set_le_signaling(supervision_timeout = 1) \n
		Specifies the duration of tolerated connection breaks down. \n
			:param supervision_timeout: numeric Range: 100 ms to 32E+3 ms, Unit: ms
		"""
		param = Conversions.decimal_value_to_str(supervision_timeout)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SVTimeout:LESignaling {param}')

	def get_value(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SVTimeout \n
		Snippet: value: int = driver.configure.connection.svTimeout.get_value() \n
		Sets/gets the LMP supervision timeout. \n
			:return: supervision_timeout: numeric Range: 400 slots to 65535 slots, Unit: slots
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SVTimeout?')
		return Conversions.str_to_int(response)

	def set_value(self, supervision_timeout: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SVTimeout \n
		Snippet: driver.configure.connection.svTimeout.set_value(supervision_timeout = 1) \n
		Sets/gets the LMP supervision timeout. \n
			:param supervision_timeout: numeric Range: 400 slots to 65535 slots, Unit: slots
		"""
		param = Conversions.decimal_value_to_str(supervision_timeout)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SVTimeout {param}')
