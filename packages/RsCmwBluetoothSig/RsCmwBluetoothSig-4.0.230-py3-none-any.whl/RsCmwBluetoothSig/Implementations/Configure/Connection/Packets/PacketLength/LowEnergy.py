from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	def get_le_1_m(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:LENergy[:LE1M] \n
		Snippet: value: int = driver.configure.connection.packets.packetLength.lowEnergy.get_le_1_m() \n
		Specifies the payload length.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Commands for LE direct test mode: For LE 1M PHY (...:LE1M...) , LE 2M PHY (...:LE2M...) , and LE coded PHY (...:LRANge...) .
			- Commands for LE UTP test mode: ..:TCONnection:.. \n
			:return: payload_length: numeric Range: 0 byte(s) to 255 byte(s) , Unit: byte
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:LENergy:LE1M?')
		return Conversions.str_to_int(response)

	def set_le_1_m(self, payload_length: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:LENergy[:LE1M] \n
		Snippet: driver.configure.connection.packets.packetLength.lowEnergy.set_le_1_m(payload_length = 1) \n
		Specifies the payload length.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Commands for LE direct test mode: For LE 1M PHY (...:LE1M...) , LE 2M PHY (...:LE2M...) , and LE coded PHY (...:LRANge...) .
			- Commands for LE UTP test mode: ..:TCONnection:.. \n
			:param payload_length: numeric Range: 0 byte(s) to 255 byte(s) , Unit: byte
		"""
		param = Conversions.decimal_value_to_str(payload_length)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:LENergy:LE1M {param}')

	def get_lrange(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:LENergy:LRANge \n
		Snippet: value: int = driver.configure.connection.packets.packetLength.lowEnergy.get_lrange() \n
		Specifies the payload length.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Commands for LE direct test mode: For LE 1M PHY (...:LE1M...) , LE 2M PHY (...:LE2M...) , and LE coded PHY (...:LRANge...) .
			- Commands for LE UTP test mode: ..:TCONnection:.. \n
			:return: payload_length: numeric Range: 0 byte(s) to 255 byte(s) , Unit: byte
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:LENergy:LRANge?')
		return Conversions.str_to_int(response)

	def set_lrange(self, payload_length: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:LENergy:LRANge \n
		Snippet: driver.configure.connection.packets.packetLength.lowEnergy.set_lrange(payload_length = 1) \n
		Specifies the payload length.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Commands for LE direct test mode: For LE 1M PHY (...:LE1M...) , LE 2M PHY (...:LE2M...) , and LE coded PHY (...:LRANge...) .
			- Commands for LE UTP test mode: ..:TCONnection:.. \n
			:param payload_length: numeric Range: 0 byte(s) to 255 byte(s) , Unit: byte
		"""
		param = Conversions.decimal_value_to_str(payload_length)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:LENergy:LRANge {param}')

	def get_le_2_m(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:LENergy:LE2M \n
		Snippet: value: int = driver.configure.connection.packets.packetLength.lowEnergy.get_le_2_m() \n
		Specifies the payload length.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Commands for LE direct test mode: For LE 1M PHY (...:LE1M...) , LE 2M PHY (...:LE2M...) , and LE coded PHY (...:LRANge...) .
			- Commands for LE UTP test mode: ..:TCONnection:.. \n
			:return: payload_length: numeric Range: 0 byte(s) to 255 byte(s) , Unit: byte
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:LENergy:LE2M?')
		return Conversions.str_to_int(response)

	def set_le_2_m(self, payload_length: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:LENergy:LE2M \n
		Snippet: driver.configure.connection.packets.packetLength.lowEnergy.set_le_2_m(payload_length = 1) \n
		Specifies the payload length.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Commands for LE direct test mode: For LE 1M PHY (...:LE1M...) , LE 2M PHY (...:LE2M...) , and LE coded PHY (...:LRANge...) .
			- Commands for LE UTP test mode: ..:TCONnection:.. \n
			:param payload_length: numeric Range: 0 byte(s) to 255 byte(s) , Unit: byte
		"""
		param = Conversions.decimal_value_to_str(payload_length)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PLENgth:LENergy:LE2M {param}')
