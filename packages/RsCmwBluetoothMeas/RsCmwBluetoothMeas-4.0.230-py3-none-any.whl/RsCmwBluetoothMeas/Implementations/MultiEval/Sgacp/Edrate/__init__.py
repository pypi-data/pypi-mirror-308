from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EdrateCls:
	"""Edrate commands group definition. 3 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("edrate", core, parent)

	@property
	def ptx(self):
		"""ptx commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_ptx'):
			from .Ptx import PtxCls
			self._ptx = PtxCls(self._core, self._cmd_group)
		return self._ptx

	def clone(self) -> 'EdrateCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EdrateCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
