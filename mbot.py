from generator import generate_firmware_and_flash, simple_serial_start

if __name__ == "__main__":

  manifest =   """
Use 115200 baud rate. 
Use Makeblock Library SDK.  
For the main include, use #include <MeMCore.h>, instead of #include <MeOrion.h>
Left motor attached to port 1.
Right motor attached to port 2.
"""

  generate_firmware_and_flash(manifest, "Make wheels spin.")
  simple_serial_start()