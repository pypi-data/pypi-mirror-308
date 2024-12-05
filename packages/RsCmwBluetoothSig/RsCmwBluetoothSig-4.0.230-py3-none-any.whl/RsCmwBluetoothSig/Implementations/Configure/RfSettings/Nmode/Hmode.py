from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HmodeCls:
	"""Hmode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hmode", core, parent)

	# noinspection PyTypeChecker
	def get_low_energy(self) -> enums.LeHoppingMode:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:NMODe:HMODe:LENergy \n
		Snippet: value: enums.LeHoppingMode = driver.configure.rfSettings.nmode.hmode.get_low_energy() \n
		Specifies hopping for LE connection tests. Channels used in hopping mode 'CH2' depend on the specified measured channel.
		The first hopping channel is identical with the measured channel (method RsCmwBluetoothSig.Configure.RfSettings.Nmode.
		Mchannel.lowEnergy) . The second hopping channel is offset from the first one. \n
			:return: hopping_mode: CH2 | ALL 'CH2': 2 data channels offset by 10 or 9 channels are used for hopping. 'ALL': 37 data channels are used for hopping.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:NMODe:HMODe:LENergy?')
		return Conversions.str_to_scalar_enum(response, enums.LeHoppingMode)

	def set_low_energy(self, hopping_mode: enums.LeHoppingMode) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:NMODe:HMODe:LENergy \n
		Snippet: driver.configure.rfSettings.nmode.hmode.set_low_energy(hopping_mode = enums.LeHoppingMode.ALL) \n
		Specifies hopping for LE connection tests. Channels used in hopping mode 'CH2' depend on the specified measured channel.
		The first hopping channel is identical with the measured channel (method RsCmwBluetoothSig.Configure.RfSettings.Nmode.
		Mchannel.lowEnergy) . The second hopping channel is offset from the first one. \n
			:param hopping_mode: CH2 | ALL 'CH2': 2 data channels offset by 10 or 9 channels are used for hopping. 'ALL': 37 data channels are used for hopping.
		"""
		param = Conversions.enum_scalar_to_str(hopping_mode, enums.LeHoppingMode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:NMODe:HMODe:LENergy {param}')
