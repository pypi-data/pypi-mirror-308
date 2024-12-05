from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FdriftCls:
	"""Fdrift commands group definition. 11 total commands, 3 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fdrift", core, parent)

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

	def get_edrate(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:FDRift:EDRate \n
		Snippet: value: bool = driver.configure.rfSettings.dtx.sing.fdrift.get_edrate() \n
		Enable/disable the periodic change of frequency offset.
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
			:return: freq_drift: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:FDRift:EDRate?')
		return Conversions.str_to_bool(response)

	def set_edrate(self, freq_drift: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:FDRift:EDRate \n
		Snippet: driver.configure.rfSettings.dtx.sing.fdrift.set_edrate(freq_drift = False) \n
		Enable/disable the periodic change of frequency offset.
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
			:param freq_drift: OFF | ON
		"""
		param = Conversions.bool_to_str(freq_drift)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:FDRift:EDRate {param}')

	def get_brate(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:FDRift:BRATe \n
		Snippet: value: bool = driver.configure.rfSettings.dtx.sing.fdrift.get_brate() \n
		Enable/disable the periodic change of frequency offset.
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
			:return: freq_drift: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:FDRift:BRATe?')
		return Conversions.str_to_bool(response)

	def set_brate(self, freq_drift: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:FDRift:BRATe \n
		Snippet: driver.configure.rfSettings.dtx.sing.fdrift.set_brate(freq_drift = False) \n
		Enable/disable the periodic change of frequency offset.
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
			:param freq_drift: OFF | ON
		"""
		param = Conversions.bool_to_str(freq_drift)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:FDRift:BRATe {param}')

	def clone(self) -> 'FdriftCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FdriftCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
