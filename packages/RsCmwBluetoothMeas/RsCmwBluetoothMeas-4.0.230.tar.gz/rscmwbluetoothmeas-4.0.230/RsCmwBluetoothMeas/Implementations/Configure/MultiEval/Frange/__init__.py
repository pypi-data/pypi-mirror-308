from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrangeCls:
	"""Frange commands group definition. 1 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frange", core, parent)

	@property
	def brate(self):
		"""brate commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_brate'):
			from .Brate import BrateCls
			self._brate = BrateCls(self._core, self._cmd_group)
		return self._brate

	def clone(self) -> 'FrangeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FrangeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
