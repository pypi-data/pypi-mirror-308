from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FlexibleCls:
	"""Flexible commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("flexible", core, parent)

	def set(self, bb_board: enums.BbBoard, rx_connector: enums.RxConnector, rx_converter: enums.RxConverter, tx_connector: enums.TxConnector, tx_converter: enums.TxConverter) -> None:
		"""SCPI: ROUTe:BLUetooth:SIGNaling<Instance>:SCENario:OTRX:FLEXible \n
		Snippet: driver.route.scenario.otRx.flexible.set(bb_board = enums.BbBoard.BBR1, rx_connector = enums.RxConnector.I11I, rx_converter = enums.RxConverter.IRX1, tx_connector = enums.TxConnector.I12O, tx_converter = enums.TxConverter.ITX1) \n
		Activates the scenario with one output and one input signal paths. For possible signaling unit, connector and converter
		values, see 'Values for signal path selection'. \n
			:param bb_board: Signaling unit
			:param rx_connector: RF connector for the input path
			:param rx_converter: RX module for the input path
			:param tx_connector: RF connector for the output path
			:param tx_converter: TX module for the output path
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('bb_board', bb_board, DataType.Enum, enums.BbBoard), ArgSingle('rx_connector', rx_connector, DataType.Enum, enums.RxConnector), ArgSingle('rx_converter', rx_converter, DataType.Enum, enums.RxConverter), ArgSingle('tx_connector', tx_connector, DataType.Enum, enums.TxConnector), ArgSingle('tx_converter', tx_converter, DataType.Enum, enums.TxConverter))
		self._core.io.write(f'ROUTe:BLUetooth:SIGNaling<Instance>:SCENario:OTRX:FLEXible {param}'.rstrip())

	# noinspection PyTypeChecker
	class FlexibleStruct(StructBase):
		"""Response structure. Fields: \n
			- Bb_Board: enums.BbBoard: Signaling unit
			- Rx_Connector: enums.RxConnector: RF connector for the input path
			- Rx_Converter: enums.RxConverter: RX module for the input path
			- Tx_Connector: enums.TxConnector: RF connector for the output path
			- Tx_Converter: enums.TxConverter: TX module for the output path"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Bb_Board', enums.BbBoard),
			ArgStruct.scalar_enum('Rx_Connector', enums.RxConnector),
			ArgStruct.scalar_enum('Rx_Converter', enums.RxConverter),
			ArgStruct.scalar_enum('Tx_Connector', enums.TxConnector),
			ArgStruct.scalar_enum('Tx_Converter', enums.TxConverter)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Bb_Board: enums.BbBoard = None
			self.Rx_Connector: enums.RxConnector = None
			self.Rx_Converter: enums.RxConverter = None
			self.Tx_Connector: enums.TxConnector = None
			self.Tx_Converter: enums.TxConverter = None

	def get(self) -> FlexibleStruct:
		"""SCPI: ROUTe:BLUetooth:SIGNaling<Instance>:SCENario:OTRX:FLEXible \n
		Snippet: value: FlexibleStruct = driver.route.scenario.otRx.flexible.get() \n
		Activates the scenario with one output and one input signal paths. For possible signaling unit, connector and converter
		values, see 'Values for signal path selection'. \n
			:return: structure: for return value, see the help for FlexibleStruct structure arguments."""
		return self._core.io.query_struct(f'ROUTe:BLUetooth:SIGNaling<Instance>:SCENario:OTRX:FLEXible?', self.__class__.FlexibleStruct())
