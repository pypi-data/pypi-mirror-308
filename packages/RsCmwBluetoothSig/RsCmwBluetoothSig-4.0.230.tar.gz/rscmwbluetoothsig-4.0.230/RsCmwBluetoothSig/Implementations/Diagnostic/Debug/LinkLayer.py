from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LinkLayerCls:
	"""LinkLayer commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("linkLayer", core, parent)

	def get_ip_address(self) -> str:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:LINKlayer:IPADdress \n
		Snippet: value: str = driver.diagnostic.debug.linkLayer.get_ip_address() \n
		No command help available \n
			:return: window: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:LINKlayer:IPADdress?')
		return trim_str_response(response)

	def set_ip_address(self, window: str) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:LINKlayer:IPADdress \n
		Snippet: driver.diagnostic.debug.linkLayer.set_ip_address(window = 'abc') \n
		No command help available \n
			:param window: No help available
		"""
		param = Conversions.value_to_quoted_str(window)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:LINKlayer:IPADdress {param}')

	def get_port_address(self) -> str:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:LINKlayer:PORTaddress \n
		Snippet: value: str = driver.diagnostic.debug.linkLayer.get_port_address() \n
		No command help available \n
			:return: window: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:LINKlayer:PORTaddress?')
		return trim_str_response(response)

	def set_port_address(self, window: str) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:LINKlayer:PORTaddress \n
		Snippet: driver.diagnostic.debug.linkLayer.set_port_address(window = 'abc') \n
		No command help available \n
			:param window: No help available
		"""
		param = Conversions.value_to_quoted_str(window)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:DEBug:LINKlayer:PORTaddress {param}')
