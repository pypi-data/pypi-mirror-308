from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PacketsCls:
	"""Packets commands group definition. 11 total commands, 4 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("packets", core, parent)

	@property
	def audio(self):
		"""audio commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_audio'):
			from .Audio import AudioCls
			self._audio = AudioCls(self._core, self._cmd_group)
		return self._audio

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .LowEnergy import LowEnergyCls
			self._lowEnergy = LowEnergyCls(self._core, self._cmd_group)
		return self._lowEnergy

	@property
	def tmode(self):
		"""tmode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tmode'):
			from .Tmode import TmodeCls
			self._tmode = TmodeCls(self._core, self._cmd_group)
		return self._tmode

	@property
	def nmode(self):
		"""nmode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_nmode'):
			from .Nmode import NmodeCls
			self._nmode = NmodeCls(self._core, self._cmd_group)
		return self._nmode

	def get_bedr(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:PACKets[:BEDR] \n
		Snippet: value: int = driver.configure.rxQuality.packets.get_bedr() \n
		Defines the number of data packets to be measured per measurement cycle (statistics cycle) . \n
			:return: number_packets: numeric Range: 1 to 400E+3
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:PACKets:BEDR?')
		return Conversions.str_to_int(response)

	def set_bedr(self, number_packets: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:PACKets[:BEDR] \n
		Snippet: driver.configure.rxQuality.packets.set_bedr(number_packets = 1) \n
		Defines the number of data packets to be measured per measurement cycle (statistics cycle) . \n
			:param number_packets: numeric Range: 1 to 400E+3
		"""
		param = Conversions.decimal_value_to_str(number_packets)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:PACKets:BEDR {param}')

	def clone(self) -> 'PacketsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PacketsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
