from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class A2DpCls:
	"""A2Dp commands group definition. 10 total commands, 0 Subgroups, 10 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("a2Dp", core, parent)

	def get_acc_slave(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:ACCSlave \n
		Snippet: value: bool = driver.configure.connection.audio.a2Dp.get_acc_slave() \n
		Allows the EUT to take control of the establishment of the A2DP connection when the R&S CMW acts as the slave. \n
			:return: assume_acceptor_role_in_slave_mode: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:ACCSlave?')
		return Conversions.str_to_bool(response)

	def set_acc_slave(self, assume_acceptor_role_in_slave_mode: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:ACCSlave \n
		Snippet: driver.configure.connection.audio.a2Dp.set_acc_slave(assume_acceptor_role_in_slave_mode = False) \n
		Allows the EUT to take control of the establishment of the A2DP connection when the R&S CMW acts as the slave. \n
			:param assume_acceptor_role_in_slave_mode: OFF | ON
		"""
		param = Conversions.bool_to_str(assume_acceptor_role_in_slave_mode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:ACCSlave {param}')

	def get_bitrate(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:BITRate \n
		Snippet: value: int = driver.configure.connection.audio.a2Dp.get_bitrate() \n
		Queries the bit rate calculated from the A2DP audio link parameters. \n
			:return: bitrate: decimal Unit: bit/s
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:BITRate?')
		return Conversions.str_to_int(response)

	def get_max_bit_pool(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:MAXBitpool \n
		Snippet: value: int = driver.configure.connection.audio.a2Dp.get_max_bit_pool() \n
		Specifies maximum bitpool value. \n
			:return: maximum_bitpool: numeric Range: 8 to 250
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:MAXBitpool?')
		return Conversions.str_to_int(response)

	def set_max_bit_pool(self, maximum_bitpool: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:MAXBitpool \n
		Snippet: driver.configure.connection.audio.a2Dp.set_max_bit_pool(maximum_bitpool = 1) \n
		Specifies maximum bitpool value. \n
			:param maximum_bitpool: numeric Range: 8 to 250
		"""
		param = Conversions.decimal_value_to_str(maximum_bitpool)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:MAXBitpool {param}')

	def get_min_bit_pool(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:MINBitpool \n
		Snippet: value: int = driver.configure.connection.audio.a2Dp.get_min_bit_pool() \n
		Specifies minimum bitpool value. \n
			:return: minimum_bitpool: numeric Range: 2 to 18
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:MINBitpool?')
		return Conversions.str_to_int(response)

	def set_min_bit_pool(self, minimum_bitpool: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:MINBitpool \n
		Snippet: driver.configure.connection.audio.a2Dp.set_min_bit_pool(minimum_bitpool = 1) \n
		Specifies minimum bitpool value. \n
			:param minimum_bitpool: numeric Range: 2 to 18
		"""
		param = Conversions.decimal_value_to_str(minimum_bitpool)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:MINBitpool {param}')

	# noinspection PyTypeChecker
	def get_alc_method(self) -> enums.AllocMethod:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:ALCMethod \n
		Snippet: value: enums.AllocMethod = driver.configure.connection.audio.a2Dp.get_alc_method() \n
		Defines the algorithm used to calculate the no. of allocated bits to represent each subband sample. \n
			:return: allocation_method: LOUDness | SNR
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:ALCMethod?')
		return Conversions.str_to_scalar_enum(response, enums.AllocMethod)

	def set_alc_method(self, allocation_method: enums.AllocMethod) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:ALCMethod \n
		Snippet: driver.configure.connection.audio.a2Dp.set_alc_method(allocation_method = enums.AllocMethod.LOUDness) \n
		Defines the algorithm used to calculate the no. of allocated bits to represent each subband sample. \n
			:param allocation_method: LOUDness | SNR
		"""
		param = Conversions.enum_scalar_to_str(allocation_method, enums.AllocMethod)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:ALCMethod {param}')

	# noinspection PyTypeChecker
	def get_sub_bands(self) -> enums.SubBands:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:SUBBands \n
		Snippet: value: enums.SubBands = driver.configure.connection.audio.a2Dp.get_sub_bands() \n
		Specifies the number of subbands used by generated signal. \n
			:return: sub_bands: SB4 | SB8 Subband 4 or 8
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:SUBBands?')
		return Conversions.str_to_scalar_enum(response, enums.SubBands)

	def set_sub_bands(self, sub_bands: enums.SubBands) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:SUBBands \n
		Snippet: driver.configure.connection.audio.a2Dp.set_sub_bands(sub_bands = enums.SubBands.SB4) \n
		Specifies the number of subbands used by generated signal. \n
			:param sub_bands: SB4 | SB8 Subband 4 or 8
		"""
		param = Conversions.enum_scalar_to_str(sub_bands, enums.SubBands)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:SUBBands {param}')

	# noinspection PyTypeChecker
	def get_blk_length(self) -> enums.BlockLength:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:BLKLength \n
		Snippet: value: enums.BlockLength = driver.configure.connection.audio.a2Dp.get_blk_length() \n
		Specifies the number of blocks of audio samples that are encoded in a single SBC frame. \n
			:return: block_length: BL4 | BL8 | BL12 | BL16 4, 8, 12, 16 blocks
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:BLKLength?')
		return Conversions.str_to_scalar_enum(response, enums.BlockLength)

	def set_blk_length(self, block_length: enums.BlockLength) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:BLKLength \n
		Snippet: driver.configure.connection.audio.a2Dp.set_blk_length(block_length = enums.BlockLength.BL12) \n
		Specifies the number of blocks of audio samples that are encoded in a single SBC frame. \n
			:param block_length: BL4 | BL8 | BL12 | BL16 4, 8, 12, 16 blocks
		"""
		param = Conversions.enum_scalar_to_str(block_length, enums.BlockLength)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:BLKLength {param}')

	# noinspection PyTypeChecker
	def get_chmode(self) -> enums.AudioChannelMode:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:CHMode \n
		Snippet: value: enums.AudioChannelMode = driver.configure.connection.audio.a2Dp.get_chmode() \n
		Specifies channel mode. \n
			:return: channel_mode: MONO | DUAL | STEReo | JSTereo Mono, dual, stereo, joint stereo
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:CHMode?')
		return Conversions.str_to_scalar_enum(response, enums.AudioChannelMode)

	def set_chmode(self, channel_mode: enums.AudioChannelMode) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:CHMode \n
		Snippet: driver.configure.connection.audio.a2Dp.set_chmode(channel_mode = enums.AudioChannelMode.DUAL) \n
		Specifies channel mode. \n
			:param channel_mode: MONO | DUAL | STEReo | JSTereo Mono, dual, stereo, joint stereo
		"""
		param = Conversions.enum_scalar_to_str(channel_mode, enums.AudioChannelMode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:CHMode {param}')

	# noinspection PyTypeChecker
	def get_smp_frequency(self) -> enums.SamplingFrequency:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:SMPFrequency \n
		Snippet: value: enums.SamplingFrequency = driver.configure.connection.audio.a2Dp.get_smp_frequency() \n
		Specifies the sampling frequency. \n
			:return: sampling_frequency: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:SMPFrequency?')
		return Conversions.str_to_scalar_enum(response, enums.SamplingFrequency)

	def set_smp_frequency(self, sampling_frequency: enums.SamplingFrequency) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:SMPFrequency \n
		Snippet: driver.configure.connection.audio.a2Dp.set_smp_frequency(sampling_frequency = enums.SamplingFrequency.SF16) \n
		Specifies the sampling frequency. \n
			:param sampling_frequency: SF16 | SF32 | SF441 | SF48 16 kHz, 32 kHz, 44.1 kHz, 48 kHz
		"""
		param = Conversions.enum_scalar_to_str(sampling_frequency, enums.SamplingFrequency)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:SMPFrequency {param}')

	# noinspection PyTypeChecker
	def get_codec(self) -> enums.AudioCodec:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:CODec \n
		Snippet: value: enums.AudioCodec = driver.configure.connection.audio.a2Dp.get_codec() \n
		Specifies A2DP codec. \n
			:return: codec: SBC Only subband coding is supported
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:CODec?')
		return Conversions.str_to_scalar_enum(response, enums.AudioCodec)

	def set_codec(self, codec: enums.AudioCodec) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:CODec \n
		Snippet: driver.configure.connection.audio.a2Dp.set_codec(codec = enums.AudioCodec.SBC) \n
		Specifies A2DP codec. \n
			:param codec: SBC Only subband coding is supported
		"""
		param = Conversions.enum_scalar_to_str(codec, enums.AudioCodec)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:A2DP:CODec {param}')
