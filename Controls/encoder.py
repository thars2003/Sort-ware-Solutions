#!/usr/bin/env python3
"""
Simple AS5600 Encoder Angle Reader
Just reads and displays the current angle from the encoder

Encoder Pins:
  VCC → 3.3V
  GND → GND
  SDA → GPIO 2
  SCL → GPIO 3
"""

import smbus2
import time

# AS5600 I2C configuration
AS5600_ADDRESS = 0x36
REG_RAW_ANGLE_H = 0x0C
REG_RAW_ANGLE_L = 0x0D

class AS5600Encoder:
    """Simple AS5600 encoder reader"""
    
    def __init__(self, bus=1):
        self.bus = smbus2.SMBus(bus)
        self.address = AS5600_ADDRESS
        
        # Test connection
        try:
            self.bus.read_byte(self.address)
            print("✓ AS5600 encoder connected")
        except:
            raise Exception("AS5600 encoder not found! Check I2C wiring.")
    
    def get_angle_degrees(self):
        """Get current angle in degrees (0-360)"""
        high = self.bus.read_byte_data(self.address, REG_RAW_ANGLE_H)
        low = self.bus.read_byte_data(self.address, REG_RAW_ANGLE_L)
        raw = ((high & 0x0F) << 8) | low
        return (raw / 4096.0) * 360.0
    
    def get_raw_value(self):
        """Get raw 12-bit value (0-4095)"""
        high = self.bus.read_byte_data(self.address, REG_RAW_ANGLE_H)
        low = self.bus.read_byte_data(self.address, REG_RAW_ANGLE_L)
        return ((high & 0x0F) << 8) | low
    
    def close(self):
        self.bus.close()


def main():
    """Read and display encoder angle continuously"""
    
    print("=" * 60)
    print("AS5600 ENCODER ANGLE READER")
    print("=" * 60)
    print()
    print("This will continuously display the encoder angle.")
    print("Rotate the magnet to see the angle change.")
    print()
    print("Press Ctrl+C to stop")
    print()
    
    try:
        # Initialize encoder
        encoder = AS5600Encoder()
        
        time.sleep(0.5)
        
        print("=" * 60)
        print("READING ANGLE...")
        print("=" * 60)
        print()
        
        # Track rotations
        last_angle = encoder.get_angle_degrees()
        total_rotations = 0
        
        while True:
            # Read current angle
            raw = encoder.get_raw_value()
            angle = encoder.get_angle_degrees()
            
            # Detect full rotations
            angle_diff = angle - last_angle
            if angle_diff < -180:  # Crossed 0° going forward
                total_rotations += 1
            elif angle_diff > 180:  # Crossed 0° going backward
                total_rotations -= 1

            last_angle = angle
    
            # Display
            print(f"Raw: {raw:4d} | Angle: {angle:6.2f}° | Total Rotations: {total_rotations:3d}", end='\r')
            
            time.sleep(0.05)  # Update at 20Hz
    
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("STOPPED")
        print("=" * 60)
        print(f"Final angle: {angle:.2f}°")
        print(f"Total rotations: {total_rotations}")
    
    except Exception as e:
        print(f"\n\nError: {e}")
        print("\nTroubleshooting:")
        print("  1. Enable I2C: sudo raspi-config → Interface Options → I2C")
        print("  2. Check wiring:")
        print("     VCC → 3.3V")
        print("     GND → GND")
        print("     SDA → GPIO 2")
        print("     SCL → GPIO 3")
        print("  3. Install library: pip3 install smbus2")
        print("  4. Check connection: i2cdetect -y 1")
        print("     (Should see '36' in the grid)")
    
    finally:
        try:
            encoder.close()
        except:
            pass
        print("\nProgram finished")

if __name__ == "__main__":
    main()