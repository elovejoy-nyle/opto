# opto
An updated opto provissioning script.
This script does assume the opto has a direct connection to the opto  though. I was also unable to avoid browser macros, and js injection.<br>
## STATUS:
<br>
currently only installs the e360 version

<br>Improvements:<br>
<ul>
  <li>doesnt expose the system username and password</li>
  <li>finds MAC / hostname on its own</li>
  <li>Runs on Windows</li>
  <li>Fewer dependencies</li>
</ul>

## Improvements TODO:
<ul>
   <li>Detect Ethernet PORT name</li>
   <li>select upload based on model name, for example C-series, E-series, or MCP...<br>
      ( For integration into another automation system) <br></li>

</ul>
Extended TODO:
<br>add a function to upgrade the firmware to version 4, which aledgedly fixes the modbus stagnation issue.<br>
<br>
<bold>Requires firefox</bold> 
<br>
## Usage:

Connect Ethernet to Groov Rio<br>
Run script either standalone or as part of someother script.<br>
allow execution time, may take a litteral minute.<br>
wait for STAT indicator light to START pulsing, then for it to STOP pulsing, and return to SOLID GREEN, before removing Ethernet Cable from OPTO.
The update script will exit before this time, but the RIO is still setting up communications. 
Reconnect the Ethernet Cable of the RIO to the rest of the SYSTEM.

## Troubleshooting: 

