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
import logging
import os.path
from datetime import datetime

from profiler.prof_common.constant import Constant
from profiler.prof_common.file_reader import FileReader
from profiler.prof_common.path_manager import PathManager
from profiler.module_visualization.graph_build.prof_graph_builder import ProfGraphBuilder


class ProfGraphExport:
    @classmethod
    def export_to_json(cls, prof_data_path: str, output_path: str):
        logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")
        output_path = os.path.abspath(output_path)
        prof_data_path = os.path.abspath(prof_data_path)
        try:
            PathManager.input_path_common_check(prof_data_path)
            PathManager.check_input_directory_path(output_path)
            PathManager.make_dir_safety(output_path)
            PathManager.check_path_writeable(output_path)
        except RuntimeError as err:
            logging.error(err)
        try:
            cls.generate_graph_data(prof_data_path, output_path)
        except RuntimeError as err:
            logging.error(err)

    @classmethod
    def generate_graph_data(cls, prof_data_path: str, output_path: str):
        all_nodes = ProfGraphBuilder(prof_data_path).build_graph()
        result_data = {"root": Constant.NPU_ROOT_ID, "node": {}}
        for node in all_nodes:
            result_data["node"][node.node_id] = node.info
        step_list = list(set([node.step_id for node in all_nodes[0].child_nodes if node.step_id is not None]))
        if step_list:
            result_data["StepList"] = step_list
        micro_steps = len(
            set([node.micro_step_id for node in all_nodes[0].child_nodes if node.micro_step_id is not None]))
        result_data["MicroSteps"] = micro_steps
        file_name = "prof_graph_json_{}.vis".format(datetime.utcnow().strftime("%Y%m%d%H%M%S%f")[:-3])
        FileReader.write_json_file(output_path, result_data, file_name)
        logging.info("Performance data has been converted into a graph-structured file: %s",
                     os.path.join(output_path, file_name))
