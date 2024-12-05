from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ResetCls:
	"""Reset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("reset", core, parent)

	def get_delay(self) -> float:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:LENergy:RESet:DELay \n
		Snippet: value: float = driver.configure.lowEnergy.reset.get_delay() \n
		Specifies a delay after EUT reset. \n
			:return: delay_after_reset: numeric Range: 0 s to 0.2 s
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:LENergy:RESet:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay_after_reset: float) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:LENergy:RESet:DELay \n
		Snippet: driver.configure.lowEnergy.reset.set_delay(delay_after_reset = 1.0) \n
		Specifies a delay after EUT reset. \n
			:param delay_after_reset: numeric Range: 0 s to 0.2 s
		"""
		param = Conversions.decimal_value_to_str(delay_after_reset)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:LENergy:RESet:DELay {param}')
