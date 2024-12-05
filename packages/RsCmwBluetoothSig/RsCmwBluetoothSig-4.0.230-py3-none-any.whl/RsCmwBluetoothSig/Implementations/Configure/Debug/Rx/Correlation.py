from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CorrelationCls:
	"""Correlation commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("correlation", core, parent)

	def get_threshold(self) -> str:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:DEBug:RX:CORRelation:THReshold \n
		Snippet: value: str = driver.configure.debug.rx.correlation.get_threshold() \n
		No command help available \n
			:return: threshold: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:DEBug:RX:CORRelation:THReshold?')
		return trim_str_response(response)

	def set_threshold(self, threshold: str) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:DEBug:RX:CORRelation:THReshold \n
		Snippet: driver.configure.debug.rx.correlation.set_threshold(threshold = rawAbc) \n
		No command help available \n
			:param threshold: No help available
		"""
		param = Conversions.value_to_str(threshold)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:DEBug:RX:CORRelation:THReshold {param}')

	def get_timeout(self) -> str:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:DEBug:RX:CORRelation:TIMeout \n
		Snippet: value: str = driver.configure.debug.rx.correlation.get_timeout() \n
		No command help available \n
			:return: timeout: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:DEBug:RX:CORRelation:TIMeout?')
		return trim_str_response(response)

	def set_timeout(self, timeout: str) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:DEBug:RX:CORRelation:TIMeout \n
		Snippet: driver.configure.debug.rx.correlation.set_timeout(timeout = rawAbc) \n
		No command help available \n
			:param timeout: No help available
		"""
		param = Conversions.value_to_str(timeout)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:DEBug:RX:CORRelation:TIMeout {param}')
