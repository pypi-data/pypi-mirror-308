from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class VolControlCls:
	"""VolControl commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("volControl", core, parent)

	def get_mic_gain(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:VOLControl:MICGain \n
		Snippet: value: int = driver.configure.connection.audio.volControl.get_mic_gain() \n
		Controls microphone gain for audio tests. \n
			:return: microphone_gain: numeric Range: 0 to 15
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:VOLControl:MICGain?')
		return Conversions.str_to_int(response)

	def set_mic_gain(self, microphone_gain: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:VOLControl:MICGain \n
		Snippet: driver.configure.connection.audio.volControl.set_mic_gain(microphone_gain = 1) \n
		Controls microphone gain for audio tests. \n
			:param microphone_gain: numeric Range: 0 to 15
		"""
		param = Conversions.decimal_value_to_str(microphone_gain)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:VOLControl:MICGain {param}')

	def get_speaker(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:VOLControl:SPEaker \n
		Snippet: value: int = driver.configure.connection.audio.volControl.get_speaker() \n
		Controls speaker volume for audio tests. \n
			:return: speaker_volume: numeric Range: 0 to 15
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:VOLControl:SPEaker?')
		return Conversions.str_to_int(response)

	def set_speaker(self, speaker_volume: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:VOLControl:SPEaker \n
		Snippet: driver.configure.connection.audio.volControl.set_speaker(speaker_volume = 1) \n
		Controls speaker volume for audio tests. \n
			:param speaker_volume: numeric Range: 0 to 15
		"""
		param = Conversions.decimal_value_to_str(speaker_volume)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:VOLControl:SPEaker {param}')
