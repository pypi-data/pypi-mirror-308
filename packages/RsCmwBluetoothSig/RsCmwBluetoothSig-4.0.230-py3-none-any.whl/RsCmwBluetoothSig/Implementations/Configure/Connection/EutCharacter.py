from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EutCharacterCls:
	"""EutCharacter commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("eutCharacter", core, parent)

	def get_opc_mode(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:EUTCharacter:OPCMode \n
		Snippet: value: bool = driver.configure.connection.eutCharacter.get_opc_mode() \n
		No command help available \n
			:return: opc_mode: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:EUTCharacter:OPCMode?')
		return Conversions.str_to_bool(response)

	def set_opc_mode(self, opc_mode: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:EUTCharacter:OPCMode \n
		Snippet: driver.configure.connection.eutCharacter.set_opc_mode(opc_mode = False) \n
		No command help available \n
			:param opc_mode: No help available
		"""
		param = Conversions.bool_to_str(opc_mode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:EUTCharacter:OPCMode {param}')

	# noinspection PyTypeChecker
	def get_sn_behaviour(self) -> enums.SequenceNumbering:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:EUTCharacter:SNBehaviour \n
		Snippet: value: enums.SequenceNumbering = driver.configure.connection.eutCharacter.get_sn_behaviour() \n
		No command help available \n
			:return: seq_numbering: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:EUTCharacter:SNBehaviour?')
		return Conversions.str_to_scalar_enum(response, enums.SequenceNumbering)

	def set_sn_behaviour(self, seq_numbering: enums.SequenceNumbering) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:EUTCharacter:SNBehaviour \n
		Snippet: driver.configure.connection.eutCharacter.set_sn_behaviour(seq_numbering = enums.SequenceNumbering.NORM) \n
		No command help available \n
			:param seq_numbering: No help available
		"""
		param = Conversions.enum_scalar_to_str(seq_numbering, enums.SequenceNumbering)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:EUTCharacter:SNBehaviour {param}')

	def get_tcp_change(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:EUTCharacter:TCPChange \n
		Snippet: value: bool = driver.configure.connection.eutCharacter.get_tcp_change() \n
		No command help available \n
			:return: tcp_change: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:EUTCharacter:TCPChange?')
		return Conversions.str_to_bool(response)

	def set_tcp_change(self, tcp_change: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:EUTCharacter:TCPChange \n
		Snippet: driver.configure.connection.eutCharacter.set_tcp_change(tcp_change = False) \n
		No command help available \n
			:param tcp_change: No help available
		"""
		param = Conversions.bool_to_str(tcp_change)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:EUTCharacter:TCPChange {param}')

	def get_rl_settling(self) -> float:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:EUTCharacter:RLSettling \n
		Snippet: value: float = driver.configure.connection.eutCharacter.get_rl_settling() \n
		No command help available \n
			:return: settling_time: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:EUTCharacter:RLSettling?')
		return Conversions.str_to_float(response)

	def set_rl_settling(self, settling_time: float) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:EUTCharacter:RLSettling \n
		Snippet: driver.configure.connection.eutCharacter.set_rl_settling(settling_time = 1.0) \n
		No command help available \n
			:param settling_time: No help available
		"""
		param = Conversions.decimal_value_to_str(settling_time)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:EUTCharacter:RLSettling {param}')
