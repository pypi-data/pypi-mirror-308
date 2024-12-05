from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MchannelCls:
	"""Mchannel commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mchannel", core, parent)

	def get_low_energy(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:NMODe:MCHannel:LENergy \n
		Snippet: value: int = driver.configure.rfSettings.nmode.mchannel.get_low_energy() \n
		Set the single measured channel for RX measurements with LE connection tests. Channels for hopping mode 'CH2' also depend
		on this setting. See also method RsCmwBluetoothSig.Configure.RfSettings.Nmode.Hmode.lowEnergy. \n
			:return: measured_channel: numeric Channel number Range: 1 to 11, 13 to 38
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:NMODe:MCHannel:LENergy?')
		return Conversions.str_to_int(response)

	def set_low_energy(self, measured_channel: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:NMODe:MCHannel:LENergy \n
		Snippet: driver.configure.rfSettings.nmode.mchannel.set_low_energy(measured_channel = 1) \n
		Set the single measured channel for RX measurements with LE connection tests. Channels for hopping mode 'CH2' also depend
		on this setting. See also method RsCmwBluetoothSig.Configure.RfSettings.Nmode.Hmode.lowEnergy. \n
			:param measured_channel: numeric Channel number Range: 1 to 11, 13 to 38
		"""
		param = Conversions.decimal_value_to_str(measured_channel)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:NMODe:MCHannel:LENergy {param}')
