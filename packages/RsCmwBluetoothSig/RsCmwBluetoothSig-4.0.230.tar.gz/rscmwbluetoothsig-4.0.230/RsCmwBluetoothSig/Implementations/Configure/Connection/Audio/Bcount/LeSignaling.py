from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LeSignalingCls:
	"""LeSignaling commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("leSignaling", core, parent)

	# noinspection PyTypeChecker
	def get_b_16_k(self) -> enums.ByteCountB16k:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:BCOunt:LESignaling:B16K \n
		Snippet: value: enums.ByteCountB16k = driver.configure.connection.audio.bcount.leSignaling.get_b_16_k() \n
		Sets the byte count for 16 kHz sampling rate. \n
			:return: byte_count: B40 40 bytes
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:BCOunt:LESignaling:B16K?')
		return Conversions.str_to_scalar_enum(response, enums.ByteCountB16k)

	def set_b_16_k(self, byte_count: enums.ByteCountB16k) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:BCOunt:LESignaling:B16K \n
		Snippet: driver.configure.connection.audio.bcount.leSignaling.set_b_16_k(byte_count = enums.ByteCountB16k.B40) \n
		Sets the byte count for 16 kHz sampling rate. \n
			:param byte_count: B40 40 bytes
		"""
		param = Conversions.enum_scalar_to_str(byte_count, enums.ByteCountB16k)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:BCOunt:LESignaling:B16K {param}')

	# noinspection PyTypeChecker
	def get_b_32_k(self) -> enums.ByteCountB32K:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:BCOunt:LESignaling:B32K \n
		Snippet: value: enums.ByteCountB32K = driver.configure.connection.audio.bcount.leSignaling.get_b_32_k() \n
		Sets the byte count for 32 kHz sampling rate. \n
			:return: byte_count: B80 80 bytes
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:BCOunt:LESignaling:B32K?')
		return Conversions.str_to_scalar_enum(response, enums.ByteCountB32K)

	def set_b_32_k(self, byte_count: enums.ByteCountB32K) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:BCOunt:LESignaling:B32K \n
		Snippet: driver.configure.connection.audio.bcount.leSignaling.set_b_32_k(byte_count = enums.ByteCountB32K.B80) \n
		Sets the byte count for 32 kHz sampling rate. \n
			:param byte_count: B80 80 bytes
		"""
		param = Conversions.enum_scalar_to_str(byte_count, enums.ByteCountB32K)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:BCOunt:LESignaling:B32K {param}')

	# noinspection PyTypeChecker
	def get_b_48_k(self) -> enums.ByteCountB48K:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:BCOunt:LESignaling:B48K \n
		Snippet: value: enums.ByteCountB48K = driver.configure.connection.audio.bcount.leSignaling.get_b_48_k() \n
		Sets the byte count for 48 kHz sampling rate. \n
			:return: byte_count: B100 | B120 | B155 100 bytes, 120 bytes, 155 bytes
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:BCOunt:LESignaling:B48K?')
		return Conversions.str_to_scalar_enum(response, enums.ByteCountB48K)

	def set_b_48_k(self, byte_count: enums.ByteCountB48K) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:BCOunt:LESignaling:B48K \n
		Snippet: driver.configure.connection.audio.bcount.leSignaling.set_b_48_k(byte_count = enums.ByteCountB48K.B100) \n
		Sets the byte count for 48 kHz sampling rate. \n
			:param byte_count: B100 | B120 | B155 100 bytes, 120 bytes, 155 bytes
		"""
		param = Conversions.enum_scalar_to_str(byte_count, enums.ByteCountB48K)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:BCOunt:LESignaling:B48K {param}')
