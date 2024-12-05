from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CmodeCls:
	"""Cmode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cmode", core, parent)

	# noinspection PyTypeChecker
	def get_le_signaling(self) -> enums.AudioChannelModeLe:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CMODe:LESignaling \n
		Snippet: value: enums.AudioChannelModeLe = driver.configure.connection.audio.cmode.get_le_signaling() \n
		Specifies channel mode. \n
			:return: channel_mode: MONO | STEReo Mono, stereo
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CMODe:LESignaling?')
		return Conversions.str_to_scalar_enum(response, enums.AudioChannelModeLe)

	def set_le_signaling(self, channel_mode: enums.AudioChannelModeLe) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CMODe:LESignaling \n
		Snippet: driver.configure.connection.audio.cmode.set_le_signaling(channel_mode = enums.AudioChannelModeLe.MONO) \n
		Specifies channel mode. \n
			:param channel_mode: MONO | STEReo Mono, stereo
		"""
		param = Conversions.enum_scalar_to_str(channel_mode, enums.AudioChannelModeLe)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CMODe:LESignaling {param}')
