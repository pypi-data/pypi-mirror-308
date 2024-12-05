from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsoundingCls:
	"""Csounding commands group definition. 3 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("csounding", core, parent)

	@property
	def dtMode(self):
		"""dtMode commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_dtMode'):
			from .DtMode import DtModeCls
			self._dtMode = DtModeCls(self._core, self._cmd_group)
		return self._dtMode

	def clone(self) -> 'CsoundingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CsoundingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
