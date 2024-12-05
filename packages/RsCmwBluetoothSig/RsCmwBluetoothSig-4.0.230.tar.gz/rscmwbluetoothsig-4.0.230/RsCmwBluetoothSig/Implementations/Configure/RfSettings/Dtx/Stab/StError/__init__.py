from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StErrorCls:
	"""StError commands group definition. 11 total commands, 3 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("stError", core, parent)

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

	def get_edrate(self) -> List[int]:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:STERror:EDRate \n
		Snippet: value: List[int] = driver.configure.rfSettings.dtx.stab.stError.get_edrate() \n
		Return the symbol timing error under the periodic change according to the test specification for Bluetooth wireless
		technology (10 values for BR and LE, 3 values for EDR) .
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for test mode classic (..:BRATe..) , (..:EDRate..) and for LE direct test mode (..:LE1M..) , (..:LE2M..) , (..
		:LRANge..) are available. For dirty transmitter parameters according to the test specification for Bluetooth wireless
		technology, see also 'Dirty TX Mode'.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:return: symbol_time_err: decimal Range: - 50 ppm to 50 ppm, for BR/EDR: - 20 ppm to 20 ppm , Unit: ppm
		"""
		response = self._core.io.query_bin_or_ascii_int_list('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:STERror:EDRate?')
		return response

	def get_brate(self) -> List[int]:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:STERror:BRATe \n
		Snippet: value: List[int] = driver.configure.rfSettings.dtx.stab.stError.get_brate() \n
		Return the symbol timing error under the periodic change according to the test specification for Bluetooth wireless
		technology (10 values for BR and LE, 3 values for EDR) .
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- RF tests:
		Commands for test mode classic (..:BRATe..) , (..:EDRate..) and for LE direct test mode (..:LE1M..) , (..:LE2M..) , (..
		:LRANge..) are available. For dirty transmitter parameters according to the test specification for Bluetooth wireless
		technology, see also 'Dirty TX Mode'.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE connection tests (normal mode) :
		Commands for uncoded LE 1M PHY (..:NMODe:LENergy:LE1M..) , LE 2M PHY (..:NMODe:LENergy:LE2M..) , and LE coded PHY (..
		:NMODe:LENergy:LRANge..) are available.
			INTRO_CMD_HELP: Refer also to the following commands: \n
			- LE UTP test mode:
		Commands for uncoded LE 1M PHY (..:TMODe:LENergy:LE1M..) , LE 2M PHY (..:TMODe:LENergy:LE2M..) , and LE coded PHY (..
		:TMODe:LENergy:LRANge..) are available. \n
			:return: symbol_time_err: decimal Range: - 50 ppm to 50 ppm, for BR/EDR: - 20 ppm to 20 ppm , Unit: ppm
		"""
		response = self._core.io.query_bin_or_ascii_int_list('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:STERror:BRATe?')
		return response

	def clone(self) -> 'StErrorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = StErrorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
