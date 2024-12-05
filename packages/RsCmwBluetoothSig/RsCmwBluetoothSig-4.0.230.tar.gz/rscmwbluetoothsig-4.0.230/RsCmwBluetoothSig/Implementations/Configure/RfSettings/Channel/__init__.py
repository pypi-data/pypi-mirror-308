from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ChannelCls:
	"""Channel commands group definition. 4 total commands, 1 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("channel", core, parent)

	@property
	def loopback(self):
		"""loopback commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_loopback'):
			from .Loopback import LoopbackCls
			self._loopback = LoopbackCls(self._core, self._cmd_group)
		return self._loopback

	def get_tmode(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:TMODe \n
		Snippet: value: int = driver.configure.rfSettings.channel.get_tmode() \n
		Sets the RF channel for LE UTP test mode. This mode supports both data and advertising channels. \n
			:return: rx_tx_chan: numeric Channel number Range: 0 Ch to 39 Ch
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:TMODe?')
		return Conversions.str_to_int(response)

	def set_tmode(self, rx_tx_chan: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:TMODe \n
		Snippet: driver.configure.rfSettings.channel.set_tmode(rx_tx_chan = 1) \n
		Sets the RF channel for LE UTP test mode. This mode supports both data and advertising channels. \n
			:param rx_tx_chan: numeric Channel number Range: 0 Ch to 39 Ch
		"""
		param = Conversions.decimal_value_to_str(rx_tx_chan)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:TMODe {param}')

	def get_dt_mode(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:DTMode \n
		Snippet: value: int = driver.configure.rfSettings.channel.get_dt_mode() \n
		Configures the channel number for direct test mode. \n
			:return: rx_tx_chan: numeric Range: 0 Ch to 39 Ch
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:DTMode?')
		return Conversions.str_to_int(response)

	def set_dt_mode(self, rx_tx_chan: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:DTMode \n
		Snippet: driver.configure.rfSettings.channel.set_dt_mode(rx_tx_chan = 1) \n
		Configures the channel number for direct test mode. \n
			:param rx_tx_chan: numeric Range: 0 Ch to 39 Ch
		"""
		param = Conversions.decimal_value_to_str(rx_tx_chan)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:DTMode {param}')

	def get_tx_test(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:TXTest \n
		Snippet: value: int = driver.configure.rfSettings.channel.get_tx_test() \n
		Defines the channels used by the TX test. \n
			:return: rx_tx_chan: numeric Range: 0 Ch to 78 Ch
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:TXTest?')
		return Conversions.str_to_int(response)

	def set_tx_test(self, rx_tx_chan: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:TXTest \n
		Snippet: driver.configure.rfSettings.channel.set_tx_test(rx_tx_chan = 1) \n
		Defines the channels used by the TX test. \n
			:param rx_tx_chan: numeric Range: 0 Ch to 78 Ch
		"""
		param = Conversions.decimal_value_to_str(rx_tx_chan)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:CHANnel:TXTest {param}')

	def clone(self) -> 'ChannelCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ChannelCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
