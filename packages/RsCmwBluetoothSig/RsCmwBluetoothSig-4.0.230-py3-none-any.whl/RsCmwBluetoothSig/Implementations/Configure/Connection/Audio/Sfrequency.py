from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SfrequencyCls:
	"""Sfrequency commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sfrequency", core, parent)

	# noinspection PyTypeChecker
	def get_le_signaling(self) -> enums.SamplingFrequencyLe:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SFRequency:LESignaling \n
		Snippet: value: enums.SamplingFrequencyLe = driver.configure.connection.audio.sfrequency.get_le_signaling() \n
		Specifies the sampling frequency for LE audio. \n
			:return: sampling_frequency: S8F | S16F | S24F | S32F | SF441 | S48F 8 kHz, 16 kHz, 24 kHz, 32 kHz, 44.1 kHz, 48 kHz
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SFRequency:LESignaling?')
		return Conversions.str_to_scalar_enum(response, enums.SamplingFrequencyLe)

	def set_le_signaling(self, sampling_frequency: enums.SamplingFrequencyLe) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SFRequency:LESignaling \n
		Snippet: driver.configure.connection.audio.sfrequency.set_le_signaling(sampling_frequency = enums.SamplingFrequencyLe.S16F) \n
		Specifies the sampling frequency for LE audio. \n
			:param sampling_frequency: S8F | S16F | S24F | S32F | SF441 | S48F 8 kHz, 16 kHz, 24 kHz, 32 kHz, 44.1 kHz, 48 kHz
		"""
		param = Conversions.enum_scalar_to_str(sampling_frequency, enums.SamplingFrequencyLe)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SFRequency:LESignaling {param}')
