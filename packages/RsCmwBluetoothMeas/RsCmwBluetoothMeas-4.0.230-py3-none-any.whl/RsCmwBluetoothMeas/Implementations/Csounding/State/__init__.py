from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .All import AllCls
			self._all = AllCls(self._core, self._cmd_group)
		return self._all

	# noinspection PyTypeChecker
	def fetch(self, timeout: float = None, target_main_state: enums.TargetMainState = None, target_sync_state: enums.SyncState = None) -> enums.ResourceState:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:CSOunding:STATe \n
		Snippet: value: enums.ResourceState = driver.csounding.state.fetch(timeout = 1.0, target_main_state = enums.TargetMainState.OFF, target_sync_state = enums.SyncState.ADJusted) \n
		Queries the main measurement state. Without query parameters, the state is returned immediately. With query parameters,
		the state is returned when the <TargetMainState> and the <TargetSyncState> are reached or when the <Timeout> expires. \n
			:param timeout: numeric
			:param target_main_state: OFF | RUN | RDY Target MainState for the query Default is RUN.
			:param target_sync_state: PENDing | ADJusted Target SyncState for the query Default is ADJ.
			:return: main_state: OFF | RUN | RDY Current state or target state of ongoing state transition OFF: measurement off RUN: measurement running RDY: measurement completed"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('timeout', timeout, DataType.Float, None, is_optional=True), ArgSingle('target_main_state', target_main_state, DataType.Enum, enums.TargetMainState, is_optional=True), ArgSingle('target_sync_state', target_sync_state, DataType.Enum, enums.SyncState, is_optional=True))
		response = self._core.io.query_str(f'FETCh:BLUetooth:MEASurement<Instance>:CSOunding:STATe? {param}'.rstrip())
		return Conversions.str_to_scalar_enum(response, enums.ResourceState)

	def clone(self) -> 'StateCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = StateCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
