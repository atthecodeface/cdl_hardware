/** Copyright (C) 2020,  Gavin J Stark.  All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * @file   analyzer.h
 * @brief  Types for the analyzer data/control buses
 *
 * Header file for the types for the analyzer data/control buses
 *
 */

/*a Types */
/*t t_analyzer_mst - Master interface towards target */
typedef struct {
    bit    valid  "If asserted, shift in the data to the control registers";
    bit[4] data   "Data for control - N bits shifted in from low to high, with data out of 0 until valid is deasserted";
    bit    enable "If high and selected then node is enabled - chained through bus joiners and targets; if seen as low, then do not drive data bus";
    bit    select "If high when enable is seen to go high at a node then that node is selected and enabled";
} t_analyzer_mst;

/*t t_analyzer_data - Analyzer data */
typedef struct {
    bit     data_valid    "High if the data is valid from the target";
    bit[64] data          "Analyzer data";
} t_analyzer_data;

/*t t_analyzer_tgt - Target interface back towards master */
typedef struct {
    bit     enable_return "If high and selected then node is enabled - chained through bus joiners and targets; if seen as low, then do not drive data bus";
    bit     selected      "Asserted if node is selected - for status only";
    t_analyzer_data data  "Data from node; all zeros if not selected";
} t_analyzer_tgt;

/*t t_analyzer_ctl - Control information to a target */
typedef struct {
    bit     enable;
    bit[32] mux_control "Shifted in from valid/data - cleared when a node becomes selected";
} t_analyzer_ctl;

