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
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DELay:PTIMeout \n
		Snippet: value: int = driver.diagnostic.delay.get_ptimeout() \n
		No command help available \n
			:return: poll_timeout: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:DELay:PTIMeout?')
		return Conversions.str_to_int(response)

	def set_ptimeout(self, poll_timeout: int) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DELay:PTIMeout \n
		Snippet: driver.diagnostic.delay.set_ptimeout(poll_timeout = 1) \n
		No command help available \n
			:param poll_timeout: No help available
		"""
		param = Conversions.decimal_value_to_str(poll_timeout)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:DELay:PTIMeout {param}')

	def get_tmode(self) -> int:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DELay:TMODe \n
		Snippet: value: int = driver.diagnostic.delay.get_tmode() \n
		No command help available \n
			:return: act_test_delay: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:DELay:TMODe?')
		return Conversions.str_to_int(response)

	def set_tmode(self, act_test_delay: int) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DELay:TMODe \n
		Snippet: driver.diagnostic.delay.set_tmode(act_test_delay = 1) \n
		No command help available \n
			:param act_test_delay: No help available
		"""
		param = Conversions.decimal_value_to_str(act_test_delay)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:DELay:TMODe {param}')
