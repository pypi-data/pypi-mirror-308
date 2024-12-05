from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.RepeatedCapability import RepeatedCapability
from ... import enums
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HwInterfaceCls:
	"""HwInterface commands group definition. 1 total commands, 0 Subgroups, 1 group commands
	Repeated Capability: HardwareIntf, default value after init: HardwareIntf.Intf1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hwInterface", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_hardwareIntf_get', 'repcap_hardwareIntf_set', repcap.HardwareIntf.Intf1)

	def repcap_hardwareIntf_set(self, hardwareIntf: repcap.HardwareIntf) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to HardwareIntf.Default
		Default value after init: HardwareIntf.Intf1"""
		self._cmd_group.set_repcap_enum_value(hardwareIntf)

	def repcap_hardwareIntf_get(self) -> repcap.HardwareIntf:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	def set(self, hw_interface: enums.HwInterface, hardwareIntf=repcap.HardwareIntf.Default) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:HWINterface<nr> \n
		Snippet: driver.configure.hwInterface.set(hw_interface = enums.HwInterface.NONE, hardwareIntf = repcap.HardwareIntf.Default) \n
		Defines interface used for tests. \n
			:param hw_interface: NONE | RS232 | USB RS232: USB connection with USB to RS232 adapter NONE: no control via USB to be used USB: direct USB connection
			:param hardwareIntf: optional repeated capability selector. Default value: Intf1 (settable in the interface 'HwInterface')
		"""
		param = Conversions.enum_scalar_to_str(hw_interface, enums.HwInterface)
		hardwareIntf_cmd_val = self._cmd_group.get_repcap_cmd_value(hardwareIntf, repcap.HardwareIntf)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:HWINterface{hardwareIntf_cmd_val} {param}')

	# noinspection PyTypeChecker
	def get(self, hardwareIntf=repcap.HardwareIntf.Default) -> enums.HwInterface:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:HWINterface<nr> \n
		Snippet: value: enums.HwInterface = driver.configure.hwInterface.get(hardwareIntf = repcap.HardwareIntf.Default) \n
		Defines interface used for tests. \n
			:param hardwareIntf: optional repeated capability selector. Default value: Intf1 (settable in the interface 'HwInterface')
			:return: hw_interface: NONE | RS232 | USB RS232: USB connection with USB to RS232 adapter NONE: no control via USB to be used USB: direct USB connection"""
		hardwareIntf_cmd_val = self._cmd_group.get_repcap_cmd_value(hardwareIntf, repcap.HardwareIntf)
		response = self._core.io.query_str(f'CONFigure:BLUetooth:SIGNaling<Instance>:HWINterface{hardwareIntf_cmd_val}?')
		return Conversions.str_to_scalar_enum(response, enums.HwInterface)

	def clone(self) -> 'HwInterfaceCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HwInterfaceCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
