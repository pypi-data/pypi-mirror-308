from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TraceCls:
	"""Trace commands group definition. 28 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("trace", core, parent)

	@property
	def sphase(self):
		"""sphase commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sphase'):
			from .Sphase import SphaseCls
			self._sphase = SphaseCls(self._core, self._cmd_group)
		return self._sphase

	@property
	def mspectrum(self):
		"""mspectrum commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_mspectrum'):
			from .Mspectrum import MspectrumCls
			self._mspectrum = MspectrumCls(self._core, self._cmd_group)
		return self._mspectrum

	@property
	def powerVsTime(self):
		"""powerVsTime commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_powerVsTime'):
			from .PowerVsTime import PowerVsTimeCls
			self._powerVsTime = PowerVsTimeCls(self._core, self._cmd_group)
		return self._powerVsTime

	@property
	def pvaPath(self):
		"""pvaPath commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_pvaPath'):
			from .PvaPath import PvaPathCls
			self._pvaPath = PvaPathCls(self._core, self._cmd_group)
		return self._pvaPath

	def clone(self) -> 'TraceCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TraceCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
