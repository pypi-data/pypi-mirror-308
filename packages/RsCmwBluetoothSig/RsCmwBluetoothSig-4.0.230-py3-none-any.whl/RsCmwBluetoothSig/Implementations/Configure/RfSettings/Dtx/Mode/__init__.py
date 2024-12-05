from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModeCls:
	"""Mode commands group definition. 11 total commands, 3 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	@property
	def nmode(self):
		"""nmode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_nmode'):
			from .Nmode import NmodeCls
			self._nmode = NmodeCls(self._core, self._cmd_group)
		return self._nmode

	@property
	def tmode(self):
		"""tmode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tmode'):
			from .Tmode import TmodeCls
			self._tmode = TmodeCls(self._core, self._cmd_group)
		return self._tmode

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .LowEnergy import LowEnergyCls
			self._lowEnergy = LowEnergyCls(self._core, self._cmd_group)
		return self._lowEnergy

	# noinspection PyTypeChecker
	def get_edrate(self) -> enums.DtxMode:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:EDRate \n
		Snippet: value: enums.DtxMode = driver.configure.rfSettings.dtx.mode.get_edrate() \n
		Configure the dirty transmitter.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for test mode classic (..:BRATe..) , (..:EDRate..) and for LE direct test mode (..:LE1M..) , (..:LE2M..) , (..
		:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:return: dtx_mode: SINGle values | SPEC table SING: single set of dirty transmitter parameters. No periodic change of the frequency offset, modulation index, and symbol timing error occurs. SPEC: settings according to the test specification for Bluetooth wireless technology, see 'Dirty TX Mode'.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:EDRate?')
		return Conversions.str_to_scalar_enum(response, enums.DtxMode)

	def set_edrate(self, dtx_mode: enums.DtxMode) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:EDRate \n
		Snippet: driver.configure.rfSettings.dtx.mode.set_edrate(dtx_mode = enums.DtxMode.SINGle) \n
		Configure the dirty transmitter.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for test mode classic (..:BRATe..) , (..:EDRate..) and for LE direct test mode (..:LE1M..) , (..:LE2M..) , (..
		:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:param dtx_mode: SINGle values | SPEC table SING: single set of dirty transmitter parameters. No periodic change of the frequency offset, modulation index, and symbol timing error occurs. SPEC: settings according to the test specification for Bluetooth wireless technology, see 'Dirty TX Mode'.
		"""
		param = Conversions.enum_scalar_to_str(dtx_mode, enums.DtxMode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:EDRate {param}')

	# noinspection PyTypeChecker
	def get_brate(self) -> enums.DtxMode:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:BRATe \n
		Snippet: value: enums.DtxMode = driver.configure.rfSettings.dtx.mode.get_brate() \n
		Configure the dirty transmitter.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for test mode classic (..:BRATe..) , (..:EDRate..) and for LE direct test mode (..:LE1M..) , (..:LE2M..) , (..
		:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:return: dtx_mode: SINGle values | SPEC table SING: single set of dirty transmitter parameters. No periodic change of the frequency offset, modulation index, and symbol timing error occurs. SPEC: settings according to the test specification for Bluetooth wireless technology, see 'Dirty TX Mode'.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:BRATe?')
		return Conversions.str_to_scalar_enum(response, enums.DtxMode)

	def set_brate(self, dtx_mode: enums.DtxMode) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:BRATe \n
		Snippet: driver.configure.rfSettings.dtx.mode.set_brate(dtx_mode = enums.DtxMode.SINGle) \n
		Configure the dirty transmitter.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for test mode classic (..:BRATe..) , (..:EDRate..) and for LE direct test mode (..:LE1M..) , (..:LE2M..) , (..
		:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:param dtx_mode: SINGle values | SPEC table SING: single set of dirty transmitter parameters. No periodic change of the frequency offset, modulation index, and symbol timing error occurs. SPEC: settings according to the test specification for Bluetooth wireless technology, see 'Dirty TX Mode'.
		"""
		param = Conversions.enum_scalar_to_str(dtx_mode, enums.DtxMode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MODE:BRATe {param}')

	def clone(self) -> 'ModeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ModeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
