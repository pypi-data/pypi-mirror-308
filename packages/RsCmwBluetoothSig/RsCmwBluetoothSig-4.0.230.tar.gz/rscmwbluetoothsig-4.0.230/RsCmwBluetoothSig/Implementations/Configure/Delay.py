from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DelayCls:
	"""Delay commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("delay", core, parent)

	def get_ptimeout(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:DELay:PTIMeout \n
		Snippet: value: int = driver.configure.delay.get_ptimeout() \n
		Sets delay for the processing of HCI commands. If set to 100 ms, maximally one HCI command is processed every 100 ms. \n
			:return: poll_timeout: integer Range: 1 ms to 100 ms , Unit: ms
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:DELay:PTIMeout?')
		return Conversions.str_to_int(response)

	def set_ptimeout(self, poll_timeout: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:DELay:PTIMeout \n
		Snippet: driver.configure.delay.set_ptimeout(poll_timeout = 1) \n
		Sets delay for the processing of HCI commands. If set to 100 ms, maximally one HCI command is processed every 100 ms. \n
			:param poll_timeout: integer Range: 1 ms to 100 ms , Unit: ms
		"""
		param = Conversions.decimal_value_to_str(poll_timeout)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:DELay:PTIMeout {param}')

	def get_tmode(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:DELay:TMODe \n
		Snippet: value: int = driver.configure.delay.get_tmode() \n
		Specifies delay for test mode activation. The delay is applied after acknowledgment from EUT that it has received
		activate test mode command. \n
			:return: act_test_delay: integer Range: 1 ms to 100 ms , Unit: ms
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:DELay:TMODe?')
		return Conversions.str_to_int(response)

	def set_tmode(self, act_test_delay: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:DELay:TMODe \n
		Snippet: driver.configure.delay.set_tmode(act_test_delay = 1) \n
		Specifies delay for test mode activation. The delay is applied after acknowledgment from EUT that it has received
		activate test mode command. \n
			:param act_test_delay: integer Range: 1 ms to 100 ms , Unit: ms
		"""
		param = Conversions.decimal_value_to_str(act_test_delay)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:DELay:TMODe {param}')
