from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CodecCls:
	"""Codec commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("codec", core, parent)

	# noinspection PyTypeChecker
	def get_le_signaling(self) -> enums.LeSigCodec:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CODec:LESignaling \n
		Snippet: value: enums.LeSigCodec = driver.configure.connection.audio.codec.get_le_signaling() \n
		Specifies the codec for LE audio. \n
			:return: codec: LC3 LC3 is default for LE audio.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CODec:LESignaling?')
		return Conversions.str_to_scalar_enum(response, enums.LeSigCodec)

	def set_le_signaling(self, codec: enums.LeSigCodec) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CODec:LESignaling \n
		Snippet: driver.configure.connection.audio.codec.set_le_signaling(codec = enums.LeSigCodec.LC3) \n
		Specifies the codec for LE audio. \n
			:param codec: LC3 LC3 is default for LE audio.
		"""
		param = Conversions.enum_scalar_to_str(codec, enums.LeSigCodec)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CODec:LESignaling {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.SpeechCode:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CODec \n
		Snippet: value: enums.SpeechCode = driver.configure.connection.audio.codec.get_value() \n
		Specifies the codec to be used for synchronous connection-oriented audio connections. \n
			:return: codec: CVSD | ALAW | ULAW | MSBC CVSD: continuously variable slope delta codec (8 kHz - SCO link) ALAW: A-law coding (8 kHz - SCO link) ULAW: u-law coding (8 kHz - SCO link) mSBC: modified subband coding (16 kHz - eSCO link)
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CODec?')
		return Conversions.str_to_scalar_enum(response, enums.SpeechCode)

	def set_value(self, codec: enums.SpeechCode) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CODec \n
		Snippet: driver.configure.connection.audio.codec.set_value(codec = enums.SpeechCode.ALAW) \n
		Specifies the codec to be used for synchronous connection-oriented audio connections. \n
			:param codec: CVSD | ALAW | ULAW | MSBC CVSD: continuously variable slope delta codec (8 kHz - SCO link) ALAW: A-law coding (8 kHz - SCO link) ULAW: u-law coding (8 kHz - SCO link) mSBC: modified subband coding (16 kHz - eSCO link)
		"""
		param = Conversions.enum_scalar_to_str(codec, enums.SpeechCode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CODec {param}')
