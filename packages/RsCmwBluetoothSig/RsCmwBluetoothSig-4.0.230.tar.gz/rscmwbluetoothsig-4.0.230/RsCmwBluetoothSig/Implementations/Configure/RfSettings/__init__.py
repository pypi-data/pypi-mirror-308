from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfSettingsCls:
	"""RfSettings commands group definition. 157 total commands, 10 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rfSettings", core, parent)

	@property
	def dtx(self):
		"""dtx commands group. 5 Sub-classes, 1 commands."""
		if not hasattr(self, '_dtx'):
			from .Dtx import DtxCls
			self._dtx = DtxCls(self._core, self._cmd_group)
		return self._dtx

	@property
	def nmode(self):
		"""nmode commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_nmode'):
			from .Nmode import NmodeCls
			self._nmode = NmodeCls(self._core, self._cmd_group)
		return self._nmode

	@property
	def channel(self):
		"""channel commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_channel'):
			from .Channel import ChannelCls
			self._channel = ChannelCls(self._core, self._cmd_group)
		return self._channel

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def aidOverride(self):
		"""aidOverride commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_aidOverride'):
			from .AidOverride import AidOverrideCls
			self._aidOverride = AidOverrideCls(self._core, self._cmd_group)
		return self._aidOverride

	@property
	def goffset(self):
		"""goffset commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_goffset'):
			from .Goffset import GoffsetCls
			self._goffset = GoffsetCls(self._core, self._cmd_group)
		return self._goffset

	@property
	def aoffset(self):
		"""aoffset commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_aoffset'):
			from .Aoffset import AoffsetCls
			self._aoffset = AoffsetCls(self._core, self._cmd_group)
		return self._aoffset

	@property
	def nantenna(self):
		"""nantenna commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_nantenna'):
			from .Nantenna import NantennaCls
			self._nantenna = NantennaCls(self._core, self._cmd_group)
		return self._nantenna

	@property
	def eattenuation(self):
		"""eattenuation commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_eattenuation'):
			from .Eattenuation import EattenuationCls
			self._eattenuation = EattenuationCls(self._core, self._cmd_group)
		return self._eattenuation

	@property
	def afHopping(self):
		"""afHopping commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_afHopping'):
			from .AfHopping import AfHoppingCls
			self._afHopping = AfHoppingCls(self._core, self._cmd_group)
		return self._afHopping

	def get_ar_power(self) -> float:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:ARPower \n
		Snippet: value: float = driver.configure.rfSettings.get_ar_power() \n
		No command help available \n
			:return: inp_level: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:ARPower?')
		return Conversions.str_to_float(response)

	def get_aranging(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<instance>:RFSettings:ARANging \n
		Snippet: value: bool = driver.configure.rfSettings.get_aranging() \n
		Adjusts the input level expected at the R&S CMW antenna automatically, according to the predefined values and measured
		signal amplitude. \n
			:return: auto_ranging: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:ARANging?')
		return Conversions.str_to_bool(response)

	def set_aranging(self, auto_ranging: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<instance>:RFSettings:ARANging \n
		Snippet: driver.configure.rfSettings.set_aranging(auto_ranging = False) \n
		Adjusts the input level expected at the R&S CMW antenna automatically, according to the predefined values and measured
		signal amplitude. \n
			:param auto_ranging: OFF | ON
		"""
		param = Conversions.bool_to_str(auto_ranging)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:ARANging {param}')

	def get_envelope_power(self) -> float:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:ENPower \n
		Snippet: value: float = driver.configure.rfSettings.get_envelope_power() \n
		Sets the expected nominal power of the EUT signal \n
			:return: exp_nominal_power: numeric The range of the expected nominal power can be calculated as follows: Range (Expected Nominal Power) = Range (Input Power) + External Attenuation - User Margin The input power range is stated in the specifications document. Unit: dBm
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:ENPower?')
		return Conversions.str_to_float(response)

	def set_envelope_power(self, exp_nominal_power: float) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:ENPower \n
		Snippet: driver.configure.rfSettings.set_envelope_power(exp_nominal_power = 1.0) \n
		Sets the expected nominal power of the EUT signal \n
			:param exp_nominal_power: numeric The range of the expected nominal power can be calculated as follows: Range (Expected Nominal Power) = Range (Input Power) + External Attenuation - User Margin The input power range is stated in the specifications document. Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(exp_nominal_power)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:ENPower {param}')

	def get_level(self) -> float:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:LEVel \n
		Snippet: value: float = driver.configure.rfSettings.get_level() \n
		Defines the absolute TX level of the R&S CMW signal. The allowed value range can be calculated as follows: Range (Level)
		= Range (Output Power) - External Attenuation Range (Output Power) = -130 dBm to 0 dBm (RFx COM) or -120 dBm to 8 dBm
		(RFx OUT) Please also notice the ranges quoted in the specification document. \n
			:return: level: numeric Range: see above , Unit: dBm
		"""
		response = self._core.io.query_str_with_opc('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, level: float) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:LEVel \n
		Snippet: driver.configure.rfSettings.set_level(level = 1.0) \n
		Defines the absolute TX level of the R&S CMW signal. The allowed value range can be calculated as follows: Range (Level)
		= Range (Output Power) - External Attenuation Range (Output Power) = -130 dBm to 0 dBm (RFx COM) or -120 dBm to 8 dBm
		(RFx OUT) Please also notice the ranges quoted in the specification document. \n
			:param level: numeric Range: see above , Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write_with_opc(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:LEVel {param}')

	def get_umargin(self) -> float:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<instance>:RFSettings:UMARgin \n
		Snippet: value: float = driver.configure.rfSettings.get_umargin() \n
		Sets the margin that the measurement adds to the expected nominal power to determine the reference power. The reference
		power minus the external input attenuation must be within the power range of the selected input connector. Refer to the
		specifications document.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- method RsCmwBluetoothSig.Configure.RfSettings.envelopePower
			- method RsCmwBluetoothSig.Configure.RfSettings.Eattenuation.inputPy \n
			:return: margin: numeric Range: 0 dB to (55 dB + external attenuation - expected nominal power)
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:UMARgin?')
		return Conversions.str_to_float(response)

	def set_umargin(self, margin: float) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<instance>:RFSettings:UMARgin \n
		Snippet: driver.configure.rfSettings.set_umargin(margin = 1.0) \n
		Sets the margin that the measurement adds to the expected nominal power to determine the reference power. The reference
		power minus the external input attenuation must be within the power range of the selected input connector. Refer to the
		specifications document.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- method RsCmwBluetoothSig.Configure.RfSettings.envelopePower
			- method RsCmwBluetoothSig.Configure.RfSettings.Eattenuation.inputPy \n
			:param margin: numeric Range: 0 dB to (55 dB + external attenuation - expected nominal power)
		"""
		param = Conversions.decimal_value_to_str(margin)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:UMARgin {param}')

	def get_easl(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:EASL \n
		Snippet: value: bool = driver.configure.rfSettings.get_easl() \n
		Sets the expected nominal power as the starting level for BR/EDR autoranging. \n
			:return: enp_as_start_level: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:EASL?')
		return Conversions.str_to_bool(response)

	def set_easl(self, enp_as_start_level: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:EASL \n
		Snippet: driver.configure.rfSettings.set_easl(enp_as_start_level = False) \n
		Sets the expected nominal power as the starting level for BR/EDR autoranging. \n
			:param enp_as_start_level: OFF | ON
		"""
		param = Conversions.bool_to_str(enp_as_start_level)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:EASL {param}')

	# noinspection PyTypeChecker
	def get_power_control(self) -> enums.PowerControl:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:PCONtrol \n
		Snippet: value: enums.PowerControl = driver.configure.rfSettings.get_power_control() \n
		No command help available \n
			:return: pcontrol: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:PCONtrol?')
		return Conversions.str_to_scalar_enum(response, enums.PowerControl)

	def set_power_control(self, pcontrol: enums.PowerControl) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:PCONtrol \n
		Snippet: driver.configure.rfSettings.set_power_control(pcontrol = enums.PowerControl.DOWN) \n
		No command help available \n
			:param pcontrol: No help available
		"""
		param = Conversions.enum_scalar_to_str(pcontrol, enums.PowerControl)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:PCONtrol {param}')

	def get_hopping(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:HOPPing \n
		Snippet: value: bool = driver.configure.rfSettings.get_hopping() \n
		Enables/disables frequency hopping. \n
			:return: hopping: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:HOPPing?')
		return Conversions.str_to_bool(response)

	def set_hopping(self, hopping: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:HOPPing \n
		Snippet: driver.configure.rfSettings.set_hopping(hopping = False) \n
		Enables/disables frequency hopping. \n
			:param hopping: OFF | ON
		"""
		param = Conversions.bool_to_str(hopping)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:HOPPing {param}')

	def clone(self) -> 'RfSettingsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RfSettingsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
