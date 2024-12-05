from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ComSettingsCls:
	"""ComSettings commands group definition. 8 total commands, 8 Subgroups, 0 group commands
	Repeated Capability: CommSettings, default value after init: CommSettings.Hw1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("comSettings", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_commSettings_get', 'repcap_commSettings_set', repcap.CommSettings.Hw1)

	def repcap_commSettings_set(self, commSettings: repcap.CommSettings) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to CommSettings.Default
		Default value after init: CommSettings.Hw1"""
		self._cmd_group.set_repcap_enum_value(commSettings)

	def repcap_commSettings_get(self) -> repcap.CommSettings:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def stopBits(self):
		"""stopBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stopBits'):
			from .StopBits import StopBitsCls
			self._stopBits = StopBitsCls(self._core, self._cmd_group)
		return self._stopBits

	@property
	def parity(self):
		"""parity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_parity'):
			from .Parity import ParityCls
			self._parity = ParityCls(self._core, self._cmd_group)
		return self._parity

	@property
	def dbits(self):
		"""dbits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dbits'):
			from .Dbits import DbitsCls
			self._dbits = DbitsCls(self._core, self._cmd_group)
		return self._dbits

	@property
	def comPort(self):
		"""comPort commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_comPort'):
			from .ComPort import ComPortCls
			self._comPort = ComPortCls(self._core, self._cmd_group)
		return self._comPort

	@property
	def baudRate(self):
		"""baudRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_baudRate'):
			from .BaudRate import BaudRateCls
			self._baudRate = BaudRateCls(self._core, self._cmd_group)
		return self._baudRate

	@property
	def protocol(self):
		"""protocol commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_protocol'):
			from .Protocol import ProtocolCls
			self._protocol = ProtocolCls(self._core, self._cmd_group)
		return self._protocol

	@property
	def ereset(self):
		"""ereset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ereset'):
			from .Ereset import EresetCls
			self._ereset = EresetCls(self._core, self._cmd_group)
		return self._ereset

	@property
	def ports(self):
		"""ports commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ports'):
			from .Ports import PortsCls
			self._ports = PortsCls(self._core, self._cmd_group)
		return self._ports

	def clone(self) -> 'ComSettingsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ComSettingsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
