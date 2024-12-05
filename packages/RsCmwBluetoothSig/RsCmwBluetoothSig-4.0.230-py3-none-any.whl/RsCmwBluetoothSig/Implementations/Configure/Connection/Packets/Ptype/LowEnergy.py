from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	# noinspection PyTypeChecker
	def get_le_1_m(self) -> enums.LePacketType2:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:LENergy[:LE1M] \n
		Snippet: value: enums.LePacketType2 = driver.configure.connection.packets.ptype.lowEnergy.get_le_1_m() \n
		Specifies the type of the LE test packet. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..
		) are available. \n
			:return: packet_type: RFPHytest | RFCTe 'RFPHytest': test packet according to Bluetooth specification up to version 5.0 'RFCTe': test packet with CTE according to Bluetooth specification version 5.1
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:LENergy:LE1M?')
		return Conversions.str_to_scalar_enum(response, enums.LePacketType2)

	def set_le_1_m(self, packet_type: enums.LePacketType2) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:LENergy[:LE1M] \n
		Snippet: driver.configure.connection.packets.ptype.lowEnergy.set_le_1_m(packet_type = enums.LePacketType2.RFCTe) \n
		Specifies the type of the LE test packet. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..
		) are available. \n
			:param packet_type: RFPHytest | RFCTe 'RFPHytest': test packet according to Bluetooth specification up to version 5.0 'RFCTe': test packet with CTE according to Bluetooth specification version 5.1
		"""
		param = Conversions.enum_scalar_to_str(packet_type, enums.LePacketType2)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:LENergy:LE1M {param}')

	# noinspection PyTypeChecker
	def get_lrange(self) -> enums.LePacketType2:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:LENergy:LRANge \n
		Snippet: value: enums.LePacketType2 = driver.configure.connection.packets.ptype.lowEnergy.get_lrange() \n
		No command help available \n
			:return: packet_type: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:LENergy:LRANge?')
		return Conversions.str_to_scalar_enum(response, enums.LePacketType2)

	def set_lrange(self, packet_type: enums.LePacketType2) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:LENergy:LRANge \n
		Snippet: driver.configure.connection.packets.ptype.lowEnergy.set_lrange(packet_type = enums.LePacketType2.RFCTe) \n
		No command help available \n
			:param packet_type: No help available
		"""
		param = Conversions.enum_scalar_to_str(packet_type, enums.LePacketType2)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:LENergy:LRANge {param}')

	# noinspection PyTypeChecker
	def get_le_2_m(self) -> enums.LePacketType2:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:LENergy:LE2M \n
		Snippet: value: enums.LePacketType2 = driver.configure.connection.packets.ptype.lowEnergy.get_le_2_m() \n
		Specifies the type of the LE test packet. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..
		) are available. \n
			:return: packet_type: RFPHytest | RFCTe 'RFPHytest': test packet according to Bluetooth specification up to version 5.0 'RFCTe': test packet with CTE according to Bluetooth specification version 5.1
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:LENergy:LE2M?')
		return Conversions.str_to_scalar_enum(response, enums.LePacketType2)

	def set_le_2_m(self, packet_type: enums.LePacketType2) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:LENergy:LE2M \n
		Snippet: driver.configure.connection.packets.ptype.lowEnergy.set_le_2_m(packet_type = enums.LePacketType2.RFCTe) \n
		Specifies the type of the LE test packet. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..
		) are available. \n
			:param packet_type: RFPHytest | RFCTe 'RFPHytest': test packet according to Bluetooth specification up to version 5.0 'RFCTe': test packet with CTE according to Bluetooth specification version 5.1
		"""
		param = Conversions.enum_scalar_to_str(packet_type, enums.LePacketType2)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:LENergy:LE2M {param}')
