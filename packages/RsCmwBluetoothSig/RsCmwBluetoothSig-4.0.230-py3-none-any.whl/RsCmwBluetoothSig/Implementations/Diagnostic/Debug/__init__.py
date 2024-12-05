from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DebugCls:
	"""Debug commands group definition. 8 total commands, 1 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("debug", core, parent)

	@property
	def linkLayer(self):
		"""linkLayer commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_linkLayer'):
			from .LinkLayer import LinkLayerCls
			self._linkLayer = LinkLayerCls(self._core, self._cmd_group)
		return self._linkLayer

	def get_sua_log(self) -> bool:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:SUALog \n
		Snippet: value: bool = driver.diagnostic.debug.get_sua_log() \n
		No command help available \n
			:return: sua_log_win: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:SUALog?')
		return Conversions.str_to_bool(response)

	def set_sua_log(self, sua_log_win: bool) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:SUALog \n
		Snippet: driver.diagnostic.debug.set_sua_log(sua_log_win = False) \n
		No command help available \n
			:param sua_log_win: No help available
		"""
		param = Conversions.bool_to_str(sua_log_win)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:SUALog {param}')

	def get_sua_fsw_log(self) -> bool:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:SUAFswlog \n
		Snippet: value: bool = driver.diagnostic.debug.get_sua_fsw_log() \n
		No command help available \n
			:return: sua_fsw_log: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:SUAFswlog?')
		return Conversions.str_to_bool(response)

	def set_sua_fsw_log(self, sua_fsw_log: bool) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:SUAFswlog \n
		Snippet: driver.diagnostic.debug.set_sua_fsw_log(sua_fsw_log = False) \n
		No command help available \n
			:param sua_fsw_log: No help available
		"""
		param = Conversions.bool_to_str(sua_fsw_log)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:SUAFswlog {param}')

	def get_simulation(self) -> bool:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:SIMulation \n
		Snippet: value: bool = driver.diagnostic.debug.get_simulation() \n
		No command help available \n
			:return: simulation: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:SIMulation?')
		return Conversions.str_to_bool(response)

	def set_simulation(self, simulation: bool) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:SIMulation \n
		Snippet: driver.diagnostic.debug.set_simulation(simulation = False) \n
		No command help available \n
			:param simulation: No help available
		"""
		param = Conversions.bool_to_str(simulation)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:SIMulation {param}')

	def get_hci_window(self) -> bool:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:HCIWindow \n
		Snippet: value: bool = driver.diagnostic.debug.get_hci_window() \n
		No command help available \n
			:return: window: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:HCIWindow?')
		return Conversions.str_to_bool(response)

	def set_hci_window(self, window: bool) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:HCIWindow \n
		Snippet: driver.diagnostic.debug.set_hci_window(window = False) \n
		No command help available \n
			:param window: No help available
		"""
		param = Conversions.bool_to_str(window)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:HCIWindow {param}')

	def get_app_window(self) -> bool:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:APPWindow \n
		Snippet: value: bool = driver.diagnostic.debug.get_app_window() \n
		No command help available \n
			:return: window: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:APPWindow?')
		return Conversions.str_to_bool(response)

	def set_app_window(self, window: bool) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:APPWindow \n
		Snippet: driver.diagnostic.debug.set_app_window(window = False) \n
		No command help available \n
			:param window: No help available
		"""
		param = Conversions.bool_to_str(window)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:APPWindow {param}')

	def get_attr_window(self) -> bool:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:ATTRibwindow \n
		Snippet: value: bool = driver.diagnostic.debug.get_attr_window() \n
		No command help available \n
			:return: window: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:ATTRibwindow?')
		return Conversions.str_to_bool(response)

	def set_attr_window(self, window: bool) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:ATTRibwindow \n
		Snippet: driver.diagnostic.debug.set_attr_window(window = False) \n
		No command help available \n
			:param window: No help available
		"""
		param = Conversions.bool_to_str(window)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:ATTRibwindow {param}')

	def clone(self) -> 'DebugCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DebugCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
