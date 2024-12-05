from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HfpCls:
	"""Hfp commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hfp", core, parent)

	def get_castartup(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:HFP:CASTartup \n
		Snippet: value: bool = driver.configure.connection.audio.hfp.get_castartup() \n
		Enables the indication of the active call to the EUT for the audio profile role hands free. \n
			:return: call_activeat_startup: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:HFP:CASTartup?')
		return Conversions.str_to_bool(response)

	def set_castartup(self, call_activeat_startup: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:HFP:CASTartup \n
		Snippet: driver.configure.connection.audio.hfp.set_castartup(call_activeat_startup = False) \n
		Enables the indication of the active call to the EUT for the audio profile role hands free. \n
			:param call_activeat_startup: OFF | ON
		"""
		param = Conversions.bool_to_str(call_activeat_startup)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:HFP:CASTartup {param}')
