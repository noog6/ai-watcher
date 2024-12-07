import time
import smbus
from .interfaces import SensorInterface

#i2c address
LPS22HB_I2C_ADDRESS	  =  0x5C
#Register 
LPS_ID                =  0xB1
#Register 
LPS_INT_CFG           =  0x0B        #Interrupt register
LPS_THS_P_L           =  0x0C        #Pressure threshold registers 
LPS_THS_P_H           =  0x0D        
LPS_WHO_AM_I          =  0x0F        #Who am I        
LPS_CTRL_REG1         =  0x10        #Control registers
LPS_CTRL_REG2         =  0x11
LPS_CTRL_REG3         =  0x12
LPS_FIFO_CTRL         =  0x14        #FIFO configuration register 
LPS_REF_P_XL          =  0x15        #Reference pressure registers
LPS_REF_P_L           =  0x16
LPS_REF_P_H           =  0x17
LPS_RPDS_L            =  0x18        #Pressure offset registers
LPS_RPDS_H            =  0x19        
LPS_RES_CONF          =  0x1A        #Resolution register
LPS_INT_SOURCE        =  0x25        #Interrupt register
LPS_FIFO_STATUS       =  0x26        #FIFO status register
LPS_STATUS            =  0x27        #Status register
LPS_PRESS_OUT_XL      =  0x28        #Pressure output registers
LPS_PRESS_OUT_L       =  0x29
LPS_PRESS_OUT_H       =  0x2A
LPS_TEMP_OUT_L        =  0x2B        #Temperature output registers
LPS_TEMP_OUT_H        =  0x2C
LPS_RES               =  0x33        #Filter reset register

class LPS22HBSensor(SensorInterface):
    _instance = None

    def __init__(self, address=LPS22HB_I2C_ADDRESS):
        self._address = address
        self._bus = smbus.SMBus(1)
        self.air_pressure = 0.0
        self.air_temperature = 0.0
        self.reset()                                 #Wait for reset to complete
        self._write_byte(LPS_CTRL_REG1 ,0x02)        #Low-pass filter disabled , output registers not updated until MSB and LSB have been read , Enable Block Data Update , Set Output Data Rate to 0 

        LPS22HBSensor._instance = self

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = LPS22HBSensor()
        return cls._instance

    def reset(self):
        Buf=self._read_u16(LPS_CTRL_REG2)
        Buf|=0x04                                         
        self._write_byte(LPS_CTRL_REG2,Buf)               #SWRESET Set 1
        while Buf:
            Buf=self._read_u16(LPS_CTRL_REG2)
            Buf&=0x04

    def read_value(self):
        self.start_oneshot()
        air_pressure    = self.get_pressure()
        air_temperature = self.get_temperature()
        return air_pressure, air_temperature

    def initialize(self):
        self.reset()

#########################################

    def start_oneshot(self):
        Buf=self._read_u16(LPS_CTRL_REG2)
        Buf|=0x01                                         #ONE_SHOT Set 1
        self._write_byte(LPS_CTRL_REG2,Buf)

    def _read_byte(self,cmd):
        return self._bus.read_byte_data(self._address,cmd)

    def _read_u16(self,cmd):
        LSB = self._bus.read_byte_data(self._address,cmd)
        MSB = self._bus.read_byte_data(self._address,cmd+1)
        return (MSB	<< 8) + LSB

    def _write_byte(self,cmd,val):
        self._bus.write_byte_data(self._address,cmd,val)

    def get_pressure(self):
        u8Buf=[0,0,0]
        if (self._read_byte(LPS_STATUS)&0x01)==0x01:
            u8Buf[0]=self._read_byte(LPS_PRESS_OUT_XL)
            u8Buf[1]=self._read_byte(LPS_PRESS_OUT_L)
            u8Buf[2]=self._read_byte(LPS_PRESS_OUT_H)
            self.air_pressure = ((u8Buf[2]<<16) + (u8Buf[1]<<8) + u8Buf[0])/4096.0
        return self.air_pressure

    def convert_hpa_to_altitude(self, pressure):
        altitude = 44307.692 * (1 - (pressure / 1013.25)**0.190284)
        return altitude

    def get_temperature(self):
        u8Buf=[0,0]
        if (self._read_byte(LPS_STATUS)&0x02)==0x02:
            u8Buf[0]=self._read_byte(LPS_TEMP_OUT_L)
            u8Buf[1]=self._read_byte(LPS_TEMP_OUT_H)
            self.air_temperature = ((u8Buf[1]<<8) + u8Buf[0])/100.0
        return self.air_temperature

if __name__ == '__main__':
    PRESS_DATA = 0.0
    TEMP_DATA = 0.0
    print("\nPressure Sensor Test Program ...\n")
    lps22hb=LPS22HBSensor()
    while True:
        time.sleep(0.1)
        PRESS_DATA, TEMP_DATA = lps22hb.read_value()
        print('Pressure = %6.2f hPa , Temperature = %6.2f °C\r\n'%(PRESS_DATA,TEMP_DATA))
