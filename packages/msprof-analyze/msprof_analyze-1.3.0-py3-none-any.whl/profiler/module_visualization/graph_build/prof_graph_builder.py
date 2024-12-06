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
from decimal import Decimal

from profiler.module_visualization.graph.prof_node import ProfNode
from profiler.module_visualization.graph_build.fwd_module_node import FwdModuleNode
from profiler.prof_common.tree_builder import TreeBuilder
from profiler.prof_common.trace_event_bean import TraceEventBean
from profiler.prof_common.constant import Constant
from profiler.module_visualization.prof_parse.prof_data_pre_process import ProfDataPreProcess


class ProfGraphBuilder:

    def __init__(self, prof_data_path: str):
        self._prof_data_path = prof_data_path
        self._prof_data = {}
        self._fwd_bwd_id = 1

    @classmethod
    def _create_event_bean_from_ops(cls, op_list: list, name: str) -> TraceEventBean:
        min_start = min((op.start_time for op in iter(op_list)))
        max_end = max((op.end_time for op in iter(op_list)))
        # 以反向算子的区间作为反向module的区间范围，为了module包含算子，做了-0.0001 +0.0001处理
        event = TraceEventBean(
            {"ts": min_start - Decimal("0.0001"), "dur": float(max_end - min_start + Decimal("0.0001")), "name": name})
        event.event_type = Constant.MODULE_TYPE
        return event

    @classmethod
    def _trans_flow_to_dict(cls, flow_events: dict, end_events: list) -> dict:
        end_event_dict = {}
        for event in end_events:
            end_event_dict[event.start_time] = event
        result_data = {}
        for flow in flow_events.values():
            start_point = flow.get("start")
            end_point = flow.get("end")
            if not start_point or not end_point:
                continue
            end_event = end_event_dict.get(end_point.start_time)
            if end_event:
                result_data.setdefault(start_point.start_time, []).append(end_event)
        return result_data

    @classmethod
    def _create_virtual_node(cls, all_nodes: list):
        root_node = all_nodes[0]
        virtual_nodes = []
        first_level_nodes = root_node.child_nodes
        root_node.reset_child_nodes([])
        merged_nodes = []
        order_id = 1
        for node in first_level_nodes:
            if node.node_type == Constant.OPERATOR_TYPE:
                merged_nodes.append(node)
                continue
            if len(merged_nodes) >= 2:
                virtual_node = ProfNode(TraceEventBean({"ts": min((node.start_time for node in merged_nodes))},
                                                       f"Operators_Between_Modules_{order_id}"), root_node)
                root_node.update_child_nodes(virtual_node)
                order_id += 1
                for op_node in merged_nodes:
                    op_node.parent_node = virtual_node
                    virtual_node.update_child_nodes(op_node)
                virtual_nodes.append(virtual_node)
            elif len(merged_nodes) == 1:
                root_node.update_child_nodes(merged_nodes[0])
            root_node.update_child_nodes(node)
            merged_nodes = []
        if len(merged_nodes) >= 2:
            virtual_node = ProfNode(TraceEventBean({"ts": min((node.start_time for node in merged_nodes))},
                                                   f"Operators_Between_Modules_{order_id}"), root_node)
            root_node.update_child_nodes(virtual_node)
            for op_node in merged_nodes:
                op_node.parent_node = virtual_node
                virtual_node.update_child_nodes(op_node)
            virtual_nodes.append(virtual_node)
        elif len(merged_nodes) == 1:
            root_node.update_child_nodes(merged_nodes[0])
        all_nodes.extend(virtual_nodes)

    @classmethod
    def _set_event_order_id(cls, all_events: list):
        name_dict = {}
        for event in all_events:
            order_id = name_dict.get(event.name, 0)
            event.set_id(f"{event.name}_{order_id}")
            name_dict[event.name] = order_id + 1

    def build_graph(self):
        self._prof_data = ProfDataPreProcess(self._prof_data_path).run()
        all_data = [*self._prof_data.get(Constant.MODULE_EVENT, []),
                    *self.find_bwd_module(),
                    *self._prof_data.get(Constant.CPU_OP_EVENT, [])]
        all_data.sort(key=lambda x: x.start_time)
        self._set_event_order_id(all_data)
        all_nodes = TreeBuilder.build_tree(all_data, ProfNode, TraceEventBean({}, Constant.NPU_ROOT_ID))
        if len(all_nodes) < 2:
            msg = "Failed to build graph."
            raise RuntimeError(msg)
        self._update_kernel_details(all_nodes[0])
        self._update_communication_details(all_nodes[0])
        self._create_virtual_node(all_nodes)
        self._update_precision_index_and_overall_metrics(all_nodes)
        self._update_step_info(all_nodes[0])
        return all_nodes

    def find_bwd_module(self) -> list:
        bwd_module_list = []
        fwdbwd_flow = self._prof_data.get(Constant.FWD_BWD_FLOW, {})
        module_list = self._prof_data.get(Constant.MODULE_EVENT, [])
        cpu_op_list = self._prof_data.get(Constant.CPU_OP_EVENT, [])
        if not fwdbwd_flow or not module_list or not cpu_op_list:
            return bwd_module_list
        fwd_tid = module_list[0].tid
        bwd_tid = fwd_tid
        for end_point in (flow.get("end") for flow in fwdbwd_flow.values()):
            if end_point:
                bwd_tid = end_point.tid
                break
        if fwd_tid == bwd_tid:
            return bwd_module_list
        # 将每一个反向包成一个module，名字叫“nn.Module: BACKWARD_0”
        all_module_nodes = TreeBuilder.build_tree(module_list, FwdModuleNode, TraceEventBean({}))
        cpu_op_list.sort(key=lambda x: x.start_time)
        pre_status = Constant.FWD_OR_OPT
        bwd_op_list = []
        for op in cpu_op_list:
            if op.tid == bwd_tid:
                bwd_op_list.append(op)
                pre_status = Constant.BACKWARD
                continue
            elif pre_status == Constant.BACKWARD:
                bwd_module_list.append(self._create_event_bean_from_ops(bwd_op_list, Constant.BACKWARD_MODULE))
                bwd_module_list.extend(self._match_fwd_module(module_list, fwdbwd_flow, bwd_op_list))
                bwd_op_list.clear()
                pre_status = Constant.FWD_OR_OPT
        if bwd_op_list:
            bwd_module_list.append(self._create_event_bean_from_ops(bwd_op_list, Constant.BACKWARD_MODULE))
            bwd_module_list.extend(self._match_fwd_module(module_list, fwdbwd_flow, bwd_op_list))
            bwd_op_list.clear()
        return bwd_module_list

    def _match_fwd_module(self, all_module_nodes, fwdbwd_flow, bwd_op_list):
        # 通过连线匹配正向module，构建出反向的整体module关系
        bwd_module_list = []
        root_node = all_module_nodes[0]
        fwdbwd_flow_dict = self._trans_flow_to_dict(fwdbwd_flow, bwd_op_list)
        for start_time, end_events in fwdbwd_flow_dict.items():
            matched_node = root_node.binary_search(start_time)
            while matched_node != Constant.INVALID_RETURN:
                matched_node.update_bwd_op(end_events)
                matched_node = matched_node.binary_search(start_time)
        for module_node in all_module_nodes:
            if module_node.bwd_op_list:
                module_node.event.fwd_bwd_id = self._fwd_bwd_id
                bwd_module_list.append(
                    self._create_event_bean_from_ops(module_node.bwd_op_list, f"{module_node.name} [BACKWARD]"))
                bwd_module_list[-1].fwd_bwd_id = self._fwd_bwd_id
                self._fwd_bwd_id += 1
        return bwd_module_list

    def _update_kernel_details(self, root_node):
        kernel_flow_dict = self._trans_flow_to_dict(self._prof_data.get(Constant.TORCH_TO_NPU_FLOW, {}),
                                                    self._prof_data.get(Constant.KERNEL_EVENT, []))
        for start_time, kernels in kernel_flow_dict.items():
            matched_node = root_node.binary_search(start_time)
            while matched_node != Constant.INVALID_RETURN:
                matched_node.update_kernel_total_list(kernels)
                matched_node = matched_node.binary_search(start_time)

    def _update_communication_details(self, root_node):
        communication_flow_dict = self._trans_flow_to_dict(self._prof_data.get(Constant.TORCH_TO_NPU_FLOW, {}),
                                                           self._prof_data.get(Constant.HCCL_EVENT, []))
        for start_time, communications in communication_flow_dict.items():
            matched_node = root_node.binary_search(start_time)
            while matched_node != Constant.INVALID_RETURN:
                matched_node.update_communication_total_list(communications)
                matched_node = matched_node.binary_search(start_time)

    def _update_step_info(self, root_node):
        first_level_nodes = root_node.child_nodes
        step_events = self._prof_data.get(Constant.STEP_EVENT, [])
        node_dict = {}
        if not step_events:
            node_dict[None] = first_level_nodes
        else:
            for node in first_level_nodes:
                for step_event in step_events:
                    if step_event.start_time <= node.start_time <= step_event.end_time:
                        node.step_id = step_event.step_id
                        node_dict.setdefault(step_event.step_id, []).append(node)
                        break
        for nodes in node_dict.values():
            micro_step_list = []
            micro_events = []
            for node in nodes:
                micro_events.append(node)
                if node.is_backward:
                    micro_step_list.append(micro_events)
                    micro_events = []
            if micro_step_list:
                micro_step_list[-1].extend(micro_events)
            else:
                micro_step_list.append(micro_events)
            for index, micro_events in enumerate(micro_step_list):
                for node in micro_events:
                    node.micro_step_id = index

    def _update_precision_index_and_overall_metrics(self, all_nodes: list):
        overlap_analysis_event = self._prof_data.get(Constant.OVERLAP_ANALYSIS_EVENT, [])
        overlap_analysis_event.sort(key=lambda x: x.start_time)
        for node in all_nodes:
            node.update_child_precision_index()
            if node.node_type != Constant.OPERATOR_TYPE:
                node.update_overall_metrics(overlap_analysis_event)
                if node.is_bwd and node.fwd_bwd_id:
                    bwd_infos[node.fwd_bwd_id] = node.overall_metrics
        for node in all_nodes:
            if node.node_type != Constant.OPERATOR_TYPE and not node.is_bwd:
                node.update_bwd_overall_metrics(bwd_infos.get(node.fwd_bwd_id, {}))
