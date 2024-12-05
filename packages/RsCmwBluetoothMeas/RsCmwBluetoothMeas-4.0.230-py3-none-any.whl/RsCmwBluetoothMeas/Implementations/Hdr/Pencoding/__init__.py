from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PencodingCls:
	"""Pencoding commands group definition. 6 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pencoding", core, parent)

	@property
	def ssequence(self):
		"""ssequence commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ssequence'):
			from .Ssequence import SsequenceCls
			self._ssequence = SsequenceCls(self._core, self._cmd_group)
		return self._ssequence

	@property
	def current(self):
		"""current commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_current'):
			from .Current import CurrentCls
			self._current = CurrentCls(self._core, self._cmd_group)
		return self._current

	def clone(self) -> 'PencodingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PencodingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
