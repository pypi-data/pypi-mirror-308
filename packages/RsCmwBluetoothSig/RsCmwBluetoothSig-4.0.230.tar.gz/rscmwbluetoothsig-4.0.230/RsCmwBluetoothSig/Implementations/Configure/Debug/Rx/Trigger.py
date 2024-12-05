from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TriggerCls:
	"""Trigger commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("trigger", core, parent)

	def get_plevel(self) -> str:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:DEBug:RX:TRIGger:PLEVel \n
		Snippet: value: str = driver.configure.debug.rx.trigger.get_plevel() \n
		No command help available \n
			:return: trigger: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:DEBug:RX:TRIGger:PLEVel?')
		return trim_str_response(response)

	def set_plevel(self, trigger: str) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:DEBug:RX:TRIGger:PLEVel \n
		Snippet: driver.configure.debug.rx.trigger.set_plevel(trigger = rawAbc) \n
		No command help available \n
			:param trigger: No help available
		"""
		param = Conversions.value_to_str(trigger)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:DEBug:RX:TRIGger:PLEVel {param}')
