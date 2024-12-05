from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SphaseCls:
	"""Sphase commands group definition. 6 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sphase", core, parent)

	@property
	def zmdeTrend(self):
		"""zmdeTrend commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_zmdeTrend'):
			from .ZmdeTrend import ZmdeTrendCls
			self._zmdeTrend = ZmdeTrendCls(self._core, self._cmd_group)
		return self._zmdeTrend

	def clone(self) -> 'SphaseCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SphaseCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
