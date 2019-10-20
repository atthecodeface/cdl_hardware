/** Copyright (C) 2019,  Gavin J Stark.  All rights reserved.
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
 * @file   i2c_modules.h
 * @brief  Header file for CDL I2C modules
 *
 * Header file for the types and CDL modules for I2C
 *
 */

/*a Includes */
include "types/i2c.h"

/*a Modules */
/*m i2c_interface */
extern module i2c_interface( clock        clk          "Clock",
                             input bit    reset_n      "Active low reset",
                             input t_i2c  i2c_in   "Pin values from the outside",
                             output t_i2c_action i2c_action "Action to I2C master or slaves",
                             input  t_i2c_conf i2c_conf     "Clock divider input to generate approx 3us from @p clk"
    )
{
    timing to    rising clock clk i2c_in, i2c_conf;
    timing from  rising clock clk i2c_action;
}

/*m i2c_slave */
extern module i2c_slave( clock        clk          "Clock",
                         input bit    reset_n      "Active low reset",
                         input t_i2c_action i2c_action "State from an i2c_interface module",
                         output t_i2c       i2c_out "Pin values to drive - 1 means float high, 0 means pull low",
                         output t_i2c_slave_request slave_request "Request to slave client",
                         input t_i2c_slave_response slave_response "Response from slave client",
                         input t_i2c_slave_select slave_select "Slave select to select this slave on I2C"
    )
{
    timing to    rising clock clk i2c_action, slave_select, slave_response;
    timing from  rising clock clk i2c_out, slave_request;
}

/*m i2c_master */
extern module i2c_master( clock        clk          "Clock",
                          input bit    reset_n      "Active low reset",
                          input t_i2c_action i2c_action "State from an i2c_interface module",
                          output t_i2c       i2c_out "Pin values to drive - 1 means float high, 0 means pull low",
                          input t_i2c_master_request master_request "Request from master client",
                          output t_i2c_master_response master_response "Response to master client",
                          input t_i2c_master_conf master_conf "Configuration of timing of master"
    )
{
    timing to    rising clock clk i2c_action;
    timing from  rising clock clk i2c_out;
    timing to    rising clock clk master_request, master_conf;
    timing from  rising clock clk master_response;
}

/*m i2c_slave_apb_master */
extern module i2c_slave_apb_master( clock        clk          "Clock",
                             input bit    reset_n      "Active low reset",
                             input t_i2c_slave_request slave_request "Request to slave client",
                             output t_i2c_slave_response slave_response "Response from slave client",
                             output t_apb_request apb_request,
                             input t_apb_response apb_response

    )
{
    timing to    rising clock clk apb_response, slave_request;
    timing from  rising clock clk apb_request, slave_response;
}
