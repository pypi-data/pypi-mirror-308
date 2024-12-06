# Copyright (c) 2024 Huawei Technologies Co., Ltd
# All rights reserved.
#
# Licensed under the BSD 3-Clause License  (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://opensource.org/licenses/BSD-3-Clause
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from profiler.prof_common.constant import Constant
from profiler.prof_common.base_node import BaseNode
from profiler.prof_common.trace_event_bean import TraceEventBean


class ProfNode(BaseNode):

    def __init__(self, event: TraceEventBean, parent_node=None):
        super().__init__(event, parent_node)
        self._kernel_total_list = []
        self._communication_total_list = []
        self._precision_index = 1
        self._computing_time = 0
        self._uncovered_comm_time = 0
        self._free_time = 0
        self._step_id = None
        self._micro_step_id = None
        self._bwd_overall_data = {}

    @property
    def node_id(self):
        return self._event.unique_id

    @property
    def node_type(self):
        if self._event.event_type is None:
            return Constant.VIRTUAL_TYPE
        return self._event.event_type

    @property
    def step_id(self):
        return self._step_id

    @property
    def micro_step_id(self):
        return self._micro_step_id

    @property
    def is_backward(self):
        return self.node_id.startswith(Constant.BACKWARD_MODULE)

    @property
    def fwd_bwd_id(self):
        return self._event.fwd_bwd_id

    @property
    def is_bwd(self):
        return "BACKWARD" in self.node_id

    @property
    def total_kernels(self):
        if self.node_type == Constant.VIRTUAL_TYPE:
            return [kernel for node in self.child_nodes for kernel in node.total_kernels]
        return self._kernel_total_list

    @property
    def total_communications(self):
        if self.node_type == Constant.VIRTUAL_TYPE:
            return [comm for node in self.child_nodes for comm in node.total_communications]
        return self._communication_total_list

    @property
    def host_total_dur(self):
        if self.node_type == Constant.VIRTUAL_TYPE:
            return sum((node.host_total_dur for node in self.child_nodes))
        return self._event.dur

    @property
    def host_self_dur(self):
        if self.node_type == Constant.VIRTUAL_TYPE:
            return 0
        return self.host_total_dur - sum((node.host_total_dur for node in self.child_nodes))

    @property
    def device_total_dur(self):
        return sum((kernel.dur for kernel in self.total_kernels))

    @property
    def device_self_dur(self):
        if self.node_type == Constant.VIRTUAL_TYPE:
            return 0
        return self.device_total_dur - sum((node.device_total_dur for node in self.child_nodes))

    @property
    def input_data(self) -> dict:
        data = {}
        input_dim = self._event.args.get("Input Dims")
        if input_dim:
            data["Input Dims"] = input_dim
        input_type = self._event.args.get("Input type")
        if input_type:
            data["Input type"] = input_type
        return data

    @property
    def kernel_data(self) -> list:
        return [kernel.kernel_info for kernel in self.total_kernels]

    @property
    def communication_data(self) -> list:
        return [[comm.name, comm.dur] for comm in self.total_communications]

    @property
    def overall_data(self):
        return {"Computing Time(us)": round(self._computing_time, 3),
                "Uncovered Communication Time(us)": round(self._uncovered_comm_time, 3),
                "Free Time(us)": round(self._free_time, 3)}

    @property
    def data(self):
        data = {
            "Overall Metrics": self.overall_data} if self.node_type != Constant.OPERATOR_TYPE else {}
        if self._bwd_overall_data:
            data.update({"Backward Overall Metrics": self._bwd_overall_data})
        data.update({"Input Data": self.input_data,
                     "precision_index": self.precision_index,
                     "Host Self Duration(us)": round(self.host_self_dur, 3),
                     "Host Total Duration(us)": round(self.host_total_dur, 3),
                     "Device Self Duration(us)": round(self.device_self_dur, 3),
                     "Device Total Duration(us)": round(self.device_total_dur, 3),
                     "kernels": self.kernel_data,
                     "Communications": self.communication_data})
        return data

    @property
    def info(self):
        info = {"id": self.node_id,
                "node_type": self.node_type,
                "data": self.data,
                "upnode": self.parent_node.node_id if self.parent_node else "None",
                "subnodes": [node.node_id for node in iter(self.child_nodes)]}
        if self.step_id is not None:
            info.update({"step_id": self.step_id})
        if self.micro_step_id is not None:
            info.update({"micro_step_id": self.micro_step_id})
        return info

    @property
    def is_root_node(self):
        return self.node_id == Constant.NPU_ROOT_ID

    @property
    def precision_index(self):
        return self._precision_index

    @precision_index.setter
    def precision_index(self, precision_index):
        self._precision_index = precision_index

    @step_id.setter
    def step_id(self, step_id):
        self._step_id = step_id

    @micro_step_id.setter
    def micro_step_id(self, micro_step_id):
        self._micro_step_id = micro_step_id

    def update_child_nodes(self, node):
        self._child_nodes.append(node)

    def reset_child_nodes(self, nodes):
        self._child_nodes = nodes

    def update_kernel_total_list(self, kernel_list: list):
        self._kernel_total_list.extend(kernel_list)

    def update_communication_total_list(self, communication_list: list):
        self._communication_total_list.extend(communication_list)

    def update_child_precision_index(self):
        if not self.child_nodes:
            return
        max_dur = max((node.device_total_dur for node in self.child_nodes))
        min_dur = min((node.device_total_dur for node in self.child_nodes))
        diff_dur = max_dur - min_dur
        for node in self.child_nodes:
            node.precision_index = 1 - (node.device_total_dur - min_dur) / diff_dur if diff_dur else 1

    def update_overall_metrics(self, overlap_analysis_event):
        if not self.total_kernels and not self.total_communications:
            return
        device_events = []
        device_events.extend(self.total_kernels)
        device_events.extend(self.total_communications)
        device_events.sort(key=lambda x: x.start_time)
        device_start = device_events[0].start_time
        device_end = device_events[-1].end_time
        for event in overlap_analysis_event:
            if event.start_time >= device_end:
                break
            if event.end_time <= device_start:
                continue
            duration_us = float(
                min(device_end, event.end_time) - max(device_start, event.start_time))
            if event.name == Constant.COMPUTING_EVENT:
                self._computing_time += duration_us
            elif event.name == Constant.FREE_EVENT:
                self._free_time += duration_us
            elif event.name == Constant.UNCOVERED_COMMUNICATION_EVENT:
                self._uncovered_comm_time += duration_us

    def update_bwd_overall_metrics(self, overall_metrics):
        self._bwd_overall_data = overall_metrics
