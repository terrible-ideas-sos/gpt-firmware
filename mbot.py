from generator import generate_firmware_and_flash, simple_serial_start

if __name__ == "__main__":

  manifest =   """
Use 115200 baud rate. 
Use Makeblock Library SDK.  
Use Makeblock LED matrix on Port 3.
For the main include, use #include <MeMCore.h>, instead of #include <MeOrion.h>
Use MeLEDMatrix class from the #include <MeLEDMatrix.h> for LED matrix.
Use `void drawBitmap(int8_t x, int8_t y, uint8_t Bitmap_Width, uint8_t *Bitmap)` method in MeLEDMatrix.
Use `void clearScreen()` method in MeLEDMatrix.
Left motor attached to `M1`. Going forward is positive value.
Right motor attached to `M2`. Going forward is negative value.
Use 250 as the speed.
"""

  generate_firmware_and_flash(manifest, "Make wheels spin in the same direction. Display eyes on the led matrix.")
  simple_serial_start()