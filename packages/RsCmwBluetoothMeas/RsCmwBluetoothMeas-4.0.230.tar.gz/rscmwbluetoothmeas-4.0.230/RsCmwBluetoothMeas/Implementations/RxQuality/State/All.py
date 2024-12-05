from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AllCls:
	"""All commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("all", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Main_State: enums.ResourceState: OFF | RUN | RDY Current state or target state of ongoing state transition OFF: measurement off RUN: measurement running RDY: measurement completed
			- Sync_State: enums.ResourceState: PEND | ADJ PEND: transition to MainState ongoing ADJ: MainState reached
			- Resource_State: enums.ResourceState: QUE | ACT | INV QUE: waiting for resource allocation ACT: resources allocated INV: no resources allocated"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Main_State', enums.ResourceState),
			ArgStruct.scalar_enum('Sync_State', enums.ResourceState),
			ArgStruct.scalar_enum('Resource_State', enums.ResourceState)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Main_State: enums.ResourceState = None
			self.Sync_State: enums.ResourceState = None
			self.Resource_State: enums.ResourceState = None

	def fetch(self, timeout: float = None, target_main_state: enums.ResourceState = None, target_sync_state: enums.SyncState = None) -> FetchStruct:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:RXQuality:STATe:ALL \n
		Snippet: value: FetchStruct = driver.rxQuality.state.all.fetch(timeout = 1.0, target_main_state = enums.ResourceState.ACTive, target_sync_state = enums.SyncState.ADJusted) \n
		Queries the main measurement state and the measurement substates. Without query parameters, the states are returned
		immediately. With query parameters, the states are returned when the <TargetMainState> and the <TargetSyncState> are
		reached or when the <Timeout> expires. \n
			:param timeout: numeric
			:param target_main_state: OFF | RUN | RDY Target MainState for the query Default is RUN.
			:param target_sync_state: PENDing | ADJusted Target SyncState for the query Default is ADJ.
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('timeout', timeout, DataType.Float, None, is_optional=True), ArgSingle('target_main_state', target_main_state, DataType.Enum, enums.ResourceState, is_optional=True), ArgSingle('target_sync_state', target_sync_state, DataType.Enum, enums.SyncState, is_optional=True))
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:RXQuality:STATe:ALL? {param}'.rstrip(), self.__class__.FetchStruct())
