"""
 ReSpeaker Python Library
 Copyright (c) 2016 Seeed Technology Limited.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import re
import respeaker.usb_hid
from respeaker.spi import spi
try: # Python 2
    import Queue
except: # Python 3
    import queue as Queue


class Sensor:
    _cmd_queue = Queue.Queue()
    _air_value=0
    devTbl={}
    cfgTbl={}

    def __init__(self):
        def led_ctrl(code, value):
            val = [code, 0, 0, int(value)]
            return val

        def led_rgb(code, value):
            r = value[0:4] 
            g = value[4:8] 
            b = value[8:12] 
            return [code, int(r, 16), int(g, 16), int (b, 16)]

        self.devTbl["R"]={"vol":[5, led_ctrl],
                          "speak":[4, led_ctrl], 
                          "listen":[7, led_ctrl],
                          "wait":[3, led_ctrl],
                          "rgb":[1, led_rgb]
                         }
        self.cfgTbl["R1"]={"addr":"00"}


        #  self.devTblRev["00"]={"G1":{"status":[0, 1]},#Gesture
                              #  "K80":{"status":[1, 2]},#human detector  
                              #  "Y1":{"ugm":[2, 4]},#PM2.5 
                              #  "X1":{"accel":[4, 16],"gyro":[16, 32]},
                             #  }
        #  self.devTblRev["01"]={"D80":{"hum":[0, 1], "rtp":[1, 2]},
                              #  "A80":{"hum":[0, 1], "rtp":[1, 2]},
                             #  }



    def loop(self):
        if Sensor._cmd_queue.qsize() != 0:
            spi_data = Sensor._cmd_queue.get(False)
        else:
            spi_data = bytearray([0xff])

        rsp = spi.write(spi_data)

        def _gesture(value)
           tmp=("right", "left", "up", "down") 
           if value == 0 or value > len(tmp) + 1:
               return None
           return "G1" + ";" + "status" + ";" + tmp[value + 1]

       def _human_detector(value)
           if value == 0:
               return None

           return "K80" + ";" + "status" + ";" + str(value)

       def _air_quality(value)
           if abs(Sensor._air_value - value) > 10:
               Sensor._air_value = value
               return "Y1" + ";" + "ugm" + ";" + str(value)
           else
               Sensor._air_value = value
               return None

       ret = []
       data = _gesture(rsp[0]) 
       if data is not None
           ret.append(data)
       data = _human_detector(rsp[1])    
       if data is not None
           ret.append(data)
       data = _air_quality(rsp[2] | rsp[3] << 8)
       if data is not None
           ret.append(data)

       return ret

    def cmd(self, cmd):
        match = re.match('(.*);(.*);(.*)', cmd)
        dev = match.group(1)
        key = match.group(2)
        value = match.group(3)

        address = int(_cfgTbl[dev], 16)

        data = cfgTbl[dev][key](value)
        self._write(address + data)
            
    @staticmethod
    def to_bytearray(data):
        if type(data) is int:
            array = bytearray([data & 0xFF])
        elif type(data) is bytearray:
            array = data
        elif type(data) is str:
            array = bytearray(data)
        elif type(data) is list:
            array = bytearray(data)
        else:
            raise TypeError('%s is not supported' % type(data))

        return array

    def _write(self, data):
        data = self.to_bytearray(data)
        Sensor._cmd_queue.put(data)


if __name__ == '__main__':
    while True:
        try:
        except KeyboardInterrupt:
            break

