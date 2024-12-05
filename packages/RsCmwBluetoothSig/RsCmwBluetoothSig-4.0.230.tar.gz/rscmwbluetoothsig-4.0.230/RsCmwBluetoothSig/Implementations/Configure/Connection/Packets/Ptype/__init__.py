from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PtypeCls:
	"""Ptype commands group definition. 7 total commands, 1 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ptype", core, parent)

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .LowEnergy import LowEnergyCls
			self._lowEnergy = LowEnergyCls(self._core, self._cmd_group)
		return self._lowEnergy

	# noinspection PyTypeChecker
	def get_sco(self) -> enums.PacketTypeSco:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:SCO \n
		Snippet: value: enums.PacketTypeSco = driver.configure.connection.packets.ptype.get_sco() \n
		Specifies the packet type for SCO connections. \n
			:return: packet_type: HV1 | HV2 | HV3 HV1: BR packet, 1/3 rate FEC HV2: BR packet, 2/3 rate FEC HV3: BR packet, no FEC
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:SCO?')
		return Conversions.str_to_scalar_enum(response, enums.PacketTypeSco)

	def set_sco(self, packet_type: enums.PacketTypeSco) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:SCO \n
		Snippet: driver.configure.connection.packets.ptype.set_sco(packet_type = enums.PacketTypeSco.HV1) \n
		Specifies the packet type for SCO connections. \n
			:param packet_type: HV1 | HV2 | HV3 HV1: BR packet, 1/3 rate FEC HV2: BR packet, 2/3 rate FEC HV3: BR packet, no FEC
		"""
		param = Conversions.enum_scalar_to_str(packet_type, enums.PacketTypeSco)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:SCO {param}')

	# noinspection PyTypeChecker
	def get_esco(self) -> enums.PacketTypeEsco:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:ESCO \n
		Snippet: value: enums.PacketTypeEsco = driver.configure.connection.packets.ptype.get_esco() \n
		Specifies the packet type for eSCO connections. \n
			:return: packet_type: EV3 | EV4 | EV5 | 2EV3 | 3EV3 | 2EV5 | 3EV5 EV3, EV4, EV5: BR packets 2EV3, 3EV3, 2EV5, 3EV5: EDR packets (2-EV3, 3-EV3, 2-EV5, 3-EV5)
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:ESCO?')
		return Conversions.str_to_scalar_enum(response, enums.PacketTypeEsco)

	def set_esco(self, packet_type: enums.PacketTypeEsco) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:ESCO \n
		Snippet: driver.configure.connection.packets.ptype.set_esco(packet_type = enums.PacketTypeEsco._2EV3) \n
		Specifies the packet type for eSCO connections. \n
			:param packet_type: EV3 | EV4 | EV5 | 2EV3 | 3EV3 | 2EV5 | 3EV5 EV3, EV4, EV5: BR packets 2EV3, 3EV3, 2EV5, 3EV5: EDR packets (2-EV3, 3-EV3, 2-EV5, 3-EV5)
		"""
		param = Conversions.enum_scalar_to_str(packet_type, enums.PacketTypeEsco)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:ESCO {param}')

	# noinspection PyTypeChecker
	def get_brate(self) -> enums.BrPacketType:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:BRATe \n
		Snippet: value: enums.BrPacketType = driver.configure.connection.packets.ptype.get_brate() \n
		Sets the BR packet type. \n
			:return: packet_type: DH1 | DH3 | DH5 Data - high rate packet carrying information bytes plus a 16-bit CRC code, see table below.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:BRATe?')
		return Conversions.str_to_scalar_enum(response, enums.BrPacketType)

	def set_brate(self, packet_type: enums.BrPacketType) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:BRATe \n
		Snippet: driver.configure.connection.packets.ptype.set_brate(packet_type = enums.BrPacketType.DH1) \n
		Sets the BR packet type. \n
			:param packet_type: DH1 | DH3 | DH5 Data - high rate packet carrying information bytes plus a 16-bit CRC code, see table below.
		"""
		param = Conversions.enum_scalar_to_str(packet_type, enums.BrPacketType)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:BRATe {param}')

	# noinspection PyTypeChecker
	def get_edrate(self) -> enums.EdrPacketType:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:EDRate \n
		Snippet: value: enums.EdrPacketType = driver.configure.connection.packets.ptype.get_edrate() \n
		Sets the EDR packet type. \n
			:return: packet_type: E21P | E23P | E25P | E31P | E33P | E35P Data - high rate packet carrying information bytes plus a 16-bit CRC code, see table below.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:EDRate?')
		return Conversions.str_to_scalar_enum(response, enums.EdrPacketType)

	def set_edrate(self, packet_type: enums.EdrPacketType) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:EDRate \n
		Snippet: driver.configure.connection.packets.ptype.set_edrate(packet_type = enums.EdrPacketType.E21P) \n
		Sets the EDR packet type. \n
			:param packet_type: E21P | E23P | E25P | E31P | E33P | E35P Data - high rate packet carrying information bytes plus a 16-bit CRC code, see table below.
		"""
		param = Conversions.enum_scalar_to_str(packet_type, enums.EdrPacketType)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PTYPe:EDRate {param}')

	def clone(self) -> 'PtypeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PtypeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
