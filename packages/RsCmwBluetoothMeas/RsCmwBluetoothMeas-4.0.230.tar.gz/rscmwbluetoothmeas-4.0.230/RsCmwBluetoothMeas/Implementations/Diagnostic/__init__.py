from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DiagnosticCls:
	"""Diagnostic commands group definition. 4 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("diagnostic", core, parent)

	@property
	def csounding(self):
		"""csounding commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_csounding'):
			from .Csounding import CsoundingCls
			self._csounding = CsoundingCls(self._core, self._cmd_group)
		return self._csounding

	@property
	def rfControl(self):
		"""rfControl commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rfControl'):
			from .RfControl import RfControlCls
			self._rfControl = RfControlCls(self._core, self._cmd_group)
		return self._rfControl

	@property
	def bluetooth(self):
		"""bluetooth commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_bluetooth'):
			from .Bluetooth import BluetoothCls
			self._bluetooth = BluetoothCls(self._core, self._cmd_group)
		return self._bluetooth

	def clone(self) -> 'DiagnosticCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DiagnosticCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
