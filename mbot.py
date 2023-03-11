from generator import generate_firmware_and_flash, simple_serial_start

if __name__ == "__main__":

  manifest =   """
Use 115200 baud rate. 
Use Makeblock Library SDK.  
For the main include, use #include <MeMCore.h>, instead of #include <MeOrion.h>
Left motor attached to M1. Going forward is positive value.
Right motor attached to M2. Going forward is negative value.
Use 250 as the speed.
"""

  generate_firmware_and_flash(manifest, "Make wheels spin in the same direction")
  simple_serial_start()