from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FdurationCls:
	"""Fduration commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fduration", core, parent)

	# noinspection PyTypeChecker
	def get_le_signaling(self) -> enums.LeSigFrameDuration:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:FDURation:LESignaling \n
		Snippet: value: enums.LeSigFrameDuration = driver.configure.connection.audio.fduration.get_le_signaling() \n
		Selects the 7.5 ms or 10 ms frame length mode for encoding of LC3 audio samples. \n
			:return: frame_duration: MS75 | MS10 Frame duration in ms.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:FDURation:LESignaling?')
		return Conversions.str_to_scalar_enum(response, enums.LeSigFrameDuration)

	def set_le_signaling(self, frame_duration: enums.LeSigFrameDuration) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:FDURation:LESignaling \n
		Snippet: driver.configure.connection.audio.fduration.set_le_signaling(frame_duration = enums.LeSigFrameDuration.MS10) \n
		Selects the 7.5 ms or 10 ms frame length mode for encoding of LC3 audio samples. \n
			:param frame_duration: MS75 | MS10 Frame duration in ms.
		"""
		param = Conversions.enum_scalar_to_str(frame_duration, enums.LeSigFrameDuration)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:FDURation:LESignaling {param}')
