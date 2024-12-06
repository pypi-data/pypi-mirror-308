
import time, logging
from GSOF_ArduBridge.ArduSPI import csLow, csHigh

# Display resolution
EPD_WIDTH       = 176
EPD_HEIGHT      = 264

GRAY1  = 0xff #white
GRAY2  = 0xC0
GRAY3  = 0x80 #gray
GRAY4  = 0x00 #Blackest

logger = logging.getLogger(__name__)

def delay_ms(ms):
    time.sleep(ms/1000)

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]

class EPD():
    def __init__(self, rst, dc, busy, cs, out, landscape=False):
        self.rst  = rst
        self.dc   = dc
        self.busy = busy
        self.cs   = cs
        self.out  = out
        self.width     = EPD_WIDTH
        self.height    = EPD_HEIGHT
        self.pages     = int(self.width/8 +0.5)
        self.landscape = landscape
        self.GRAY1  = GRAY1 #white
        self.GRAY2  = GRAY2
        self.GRAY3  = GRAY3 #gray
        self.GRAY4  = GRAY4 #Blackest


        self.bwr_lut_vcom_dc = [0x00,0x00,
            0x00,0x08,0x00,0x00,0x00,0x02,
            0x60,0x28,0x28,0x00,0x00,0x01,
            0x00,0x14,0x00,0x00,0x00,0x01,
            0x00,0x12,0x12,0x00,0x00,0x01,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,]
        
        self.bwr_lut_ww = [
            0x40,0x08,0x00,0x00,0x00,0x02,
            0x90,0x28,0x28,0x00,0x00,0x01,
            0x40,0x14,0x00,0x00,0x00,0x01,
            0xA0,0x12,0x12,0x00,0x00,0x01,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,]
        
        self.bwr_lut_bw = [
            0x40,0x08,0x00,0x00,0x00,0x02,
            0x90,0x28,0x28,0x00,0x00,0x01,
            0x40,0x14,0x00,0x00,0x00,0x01,
            0xA0,0x12,0x12,0x00,0x00,0x01,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,]

        self.bwr_lut_bb = [
            0x80,0x08,0x00,0x00,0x00,0x02,
            0x90,0x28,0x28,0x00,0x00,0x01,
            0x80,0x14,0x00,0x00,0x00,0x01,
            0x50,0x12,0x12,0x00,0x00,0x01,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,]
        
        self.bwr_lut_wb = [
            0x80,0x08,0x00,0x00,0x00,0x02,
            0x90,0x28,0x28,0x00,0x00,0x01,
            0x80,0x14,0x00,0x00,0x00,0x01,
            0x50,0x12,0x12,0x00,0x00,0x01,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,]

        #******************partial screen update LUT**************
        self.partial_lut_vcom1 =[
            0x00,0x19,0x01,0x00,0x00,0x01,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,]

        self.partial_lut_ww1 =[
            0x00,0x19,0x01,0x00,0x00,0x01,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,]

        self.partial_lut_bw1 =[
            0x80,0x19,0x01,0x00,0x00,0x01,	
            0x00,0x00,0x00,0x00,0x00,0x00,	
            0x00,0x00,0x00,0x00,0x00,0x00,	
            0x00,0x00,0x00,0x00,0x00,0x00,	
            0x00,0x00,0x00,0x00,0x00,0x00,	
            0x00,0x00,0x00,0x00,0x00,0x00,	
            0x00,0x00,0x00,0x00,0x00,0x00,]

        self.partial_lut_wb1 =[
            0x40,0x19,0x01,0x00,0x00,0x01,	
            0x00,0x00,0x00,0x00,0x00,0x00,	
            0x00,0x00,0x00,0x00,0x00,0x00,	
            0x00,0x00,0x00,0x00,0x00,0x00,	
            0x00,0x00,0x00,0x00,0x00,0x00,	
            0x00,0x00,0x00,0x00,0x00,0x00,	
            0x00,0x00,0x00,0x00,0x00,0x00,]

        self.partial_lut_bb1 =[
            0x00,0x19,0x01,0x00,0x00,0x01,	
            0x00,0x00,0x00,0x00,0x00,0x00,	
            0x00,0x00,0x00,0x00,0x00,0x00,	
            0x00,0x00,0x00,0x00,0x00,0x00,	
            0x00,0x00,0x00,0x00,0x00,0x00,	
            0x00,0x00,0x00,0x00,0x00,0x00,	
            0x00,0x00,0x00,0x00,0x00,0x00,]
        
        ###################full screen update LUT######################
        #0~3 gray
        self.gray_lut_vcom = [0x00,0x00,
            0x00,0x0A,0x00,0x00,0x00,0x01,
            0x60,0x14,0x14,0x00,0x00,0x01,
            0x00,0x14,0x00,0x00,0x00,0x01,
            0x00,0x13,0x0A,0x01,0x00,0x01,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,]
        #R21
        self.gray_lut_ww =[
            0x40,0x0A,0x00,0x00,0x00,0x01,
            0x90,0x14,0x14,0x00,0x00,0x01,
            0x10,0x14,0x0A,0x00,0x00,0x01,
            0xA0,0x13,0x01,0x00,0x00,0x01,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,]
        #R22H	r
        self.gray_lut_bw =[
            0x40,0x0A,0x00,0x00,0x00,0x01,
            0x90,0x14,0x14,0x00,0x00,0x01,
            0x00,0x14,0x0A,0x00,0x00,0x01,
            0x99,0x0C,0x01,0x03,0x04,0x01,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,]
        #R23H	w
        self.gray_lut_wb =[
            0x40,0x0A,0x00,0x00,0x00,0x01,
            0x90,0x14,0x14,0x00,0x00,0x01,
            0x00,0x14,0x0A,0x00,0x00,0x01,
            0x99,0x0B,0x04,0x04,0x01,0x01,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,]
        #R24H	b
        self.gray_lut_bb =[
            0x80,0x0A,0x00,0x00,0x00,0x01,
            0x90,0x14,0x14,0x00,0x00,0x01,
            0x20,0x14,0x0A,0x00,0x00,0x01,
            0x50,0x13,0x01,0x00,0x00,0x01,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,
            0x00,0x00,0x00,0x00,0x00,0x00,]
    
    def reset(self):
        """Hardware reset"""
        self.rst(1)
        delay_ms(200) 
        self.rst(0)
        delay_ms(5)
        self.rst(1)
        delay_ms(200)
        return self

    def command(self, cmd):
        """Send command byte"""
        self.dc(0)
        cs = self.cs.pin
        self.out( cs1=csLow(cs), cs2=csHigh(cs), N=1, vByte=[cmd] )
        return self

    def data(self, vDat):
        """Send single byte or vector of bytes""" 
        if type(vDat) == int:
            vDat = [vDat]
        self.dc(1)
        cs = self.cs.pin
        lists = split_list(vDat, wanted_parts=int(len(vDat)/128 +1))
        for ls in lists:
            self.out( cs1=csLow(cs), cs2=csHigh(cs), N=1, vByte=ls )
        return self
        
    def waitWhileBusy(self):
        logger.debug("e-Paper busy")
        while(self.busy() == 0):      #  0: idle, 1: busy
            delay_ms(100)                
        logger.debug("e-Paper busy release")
        return self

    def clear(self, bw=0xff, red=0xff):
        self.command(0x10).data( [bw]*self.height*self.pages )
        self.command(0x13).data( [red]*self.height*self.pages )
        self.command(0x12).waitWhileBusy()

    def sleep(self):
        self.command(0x50).data(0xf7)
        self.command(0x02).command(0X07).data(0xA5)

    def getResolution(self) -> list:
        if self.landscape == False:
            return (self.width, self.height)
        else:
            return (self.height, self.width)

    def _getResolutionBytes(self) -> list:
        resXLsb = 0xff&(self.width)
        resXMsb = 0xff&(self.width>>8)
        resYLsb = 0xff&(self.height)
        resYMsb = 0xff&(self.height>>8)
        return [resXMsb,resXLsb, resYMsb,resYLsb]

    def initBwr(self):
        self.reset()
        
        self.command(0x01) #< POWER_SETTING
        self.data(0x03)    #< VDS_EN, VDG_EN
        self.data(0x00)    #< VCOM_HV, VGHL_LV[1], VGHL_LV[0]
        self.data(0x2b)    #< VDH
        self.data(0x2b)    #< VDL
        self.data(0x09)    #< VDHR
        
        self.command(0x06).data([0x07, 0x07, 0x17] ) #< BOOSTER_SOFT_START
        
#        self.command(0xF8).data( [0x60,0xA5] ) #< Power optimization
#        self.command(0xF8).data( [0x73,0x23] ) #< Power optimization
#        self.command(0xF8).data( [0x7c,0x00] ) #< Power optimization

        self.command(0xF8).data( [0x60,0xA5] ) #< Power optimization
        self.command(0xF8).data( [0x89,0xA5] ) #< Power optimization
        self.command(0xF8).data( [0x90,0x00] ) #< Power optimization
        self.command(0xF8).data( [0x93,0x2A] ) #< Power optimization
        self.command(0xF8).data( [0xA0,0xA5] ) #< Power optimization
        self.command(0xF8).data( [0xA1,0x00] ) #< Power optimization
        self.command(0xF8).data( [0x73,0x41] ) #< Power optimization
        
        self.command(0x16).data(0x00)      #< PARTIAL_DISPLAY_REFRESH

        self.command(0x01).data([0x03,0x00,0x2b,0x2b,0x09]) #< POWER SETTING SPI

        self.command(0x04).waitWhileBusy() #< POWER_ON
        self.command(0x00).data(0xAF)      #< PANEL_SETTING: KW-BF   KWR-AF    BWROTP 0f
        self.command(0x30).data(0x3A)      #< PLL_CONTROL: 3A 100HZ, 29 150Hz, 39 200HZ, 31 171HZ

        resXLsb = 0xff&(self.width)
        resXMsb = 0xff&(self.width>>8)
        resYLsb = 0xff&(self.height)
        resYMsb = 0xff&(self.height>>8)
        self.command(0x61).data( self._getResolutionBytes() ) #resolution setting (176, 264)

        self.command(0x82).data(0x12)      #< VCM_DC_SETTING_REGISTER
        self.command(0X50).data(0x57)      #< VCOM AND DATA INTERVAL SETTING			
        #self.command(0X50).data(0x87)      #< VCOM AND DATA INTERVAL SETTING
        self.setBwrLut()
        return self

    def setBwrLut(self):
        self.command(0x20).data(self.bwr_lut_vcom_dc)
        self.command(0x21).data(self.bwr_lut_ww)      #< ww --
        self.command(0x22).data(self.bwr_lut_bw)      #< bw r
        self.command(0x23).data(self.bwr_lut_bb)      #< wb w
        self.command(0x24).data(self.bwr_lut_wb)      #< bb b 

    def getBufferBwr(self, image):
        # logger.debug("bufsiz = ",int(self.width/8) * self.height)
        buf = [0xFF]*self.pages*self.height
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        # logger.debug("imwidth = %d, imheight = %d",imwidth,imheight)
        if (imwidth==self.width) and (imheight==self.height) and (self.landscape==False):
            logger.debug("Vertical")
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
                        buf[int((x + y * self.width) / 8)] &= ~(0x80 >> (x % 8))
        elif(imwidth==self.height and imheight==self.width) and (self.landscape==True):
            logger.debug("Horizontal")
            for y in range(imheight):
                for x in range(imwidth):
                    newx = y
                    newy = self.height - x - 1
                    if pixels[x, y] == 0:
                        buf[int((newx + newy*self.width) / 8)] &= ~(0x80 >> (y % 8))
        else:
            print("Incorrect resolution. Got (%d,%d) vs (%d, %d)"%(imwidth, imheight, self.width, self.height))
        return buf

    def displayBwr(self, image):
        bufferSize = self.height*self.pages
        img = image[0:bufferSize +1]
        self.setBwrLut();
        self.command(0x10).data( [0xFF]*bufferSize )
        self.command(0x13).data( img )
        self.command(0x12).waitWhileBusy()

    def init4Gray(self):
        self.reset()
        self.command(0x01).data( [0x03,0x00,0x2b,0x2b] ) #< POWER SETTING
        self.command(0x06).data( [0x07, 0x07, 0x17]) #< booster soft start A,B,C
        self.command(0xF8).data( [0x60,0xA5] )
        self.command(0xF8).data( [0x89,0xA5] )
        self.command(0xF8).data( [0x90,0x00] )
        self.command(0xF8).data( [0x93,0x2A] )
        self.command(0xF8).data( [0xa0,0xa5] )
        self.command(0xF8).data( [0xa1,0x00] )
        self.command(0xF8).data( [0x73,0x41] )
        self.command(0x16).data(0x00)	
        self.command(0x04).waitWhileBusy()

        self.command(0x00).data(0xbf) #panel setting: KW-BF   KWR-AF	BWROTP 0f
        self.command(0x30).data(0x90) #PLL setting 100hz
        resXLsb = 0xff&(self.width)
        resXMsb = 0xff&(self.width>>8)
        resYLsb = 0xff&(self.height)
        resYMsb = 0xff&(self.height>>8)
        self.command(0x61).data( self._getResolutionBytes() ) #resolution setting (176, 264)
        self.command(0x61).data( [resXMsb,resXLsb, resYMsb,resYLsb] ) #resolution setting (176, 264)
        self.command(0x82).data(0x12) #vcom_DC setting
        self.command(0X50).data(0x57)			#VCOM AND DATA INTERVAL SETTING			
        return self

    def set4GrayLut(self):
        self.command(0x20).data(self.gray_lut_vcom)
        self.command(0x21).data(self.gray_lut_ww) #< red not use
        self.command(0x22).data(self.gray_lut_bw) #< bw r
        self.command(0x23).data(self.gray_lut_wb) #< wb w
        self.command(0x24).data(self.gray_lut_bb) #< bb b
        self.command(0x25).data(self.gray_lut_ww) #< vcom
    
    def getBuffer4Gray(self, image):
        # logger.debug("bufsiz = ",int(self.width/8) * self.height)
        buf = [0xFF] * (int(self.width / 4) * self.height)
        image_monocolor = image.convert('L')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        i=0
        # logger.debug("imwidth = %d, imheight = %d",imwidth,imheight)
        if (imwidth==self.width) and (imheight==self.height) and (self.landscape==False):
            logger.debug("Vertical")
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if(pixels[x, y] == 0xC0):
                        pixels[x, y] = 0x80
                    elif (pixels[x, y] == 0x80):
                        pixels[x, y] = 0x40
                    i= i+1
                    if(i%4 == 0):
                        buf[int((x + (y * self.width))/4)] = ((pixels[x-3, y]&0xc0) | (pixels[x-2, y]&0xc0)>>2 | (pixels[x-1, y]&0xc0)>>4 | (pixels[x, y]&0xc0)>>6)      
        elif (imwidth==self.height) and (imheight==self.width) and (self.landscape==True):
            logger.debug("Horizontal")
            for x in range(imwidth):
                for y in range(imheight):
                    newx = y
                    newy = self.height - x - 1
                    if(pixels[x, y] == 0xC0):
                        pixels[x, y] = 0x80
                    elif (pixels[x, y] == 0x80):
                        pixels[x, y] = 0x40
                    i= i+1
                    if(i%4 == 0):
                        buf[int((newx + (newy * self.width))/4)] = ((pixels[x, y-3]&0xc0) | (pixels[x, y-2]&0xc0)>>2 | (pixels[x, y-1]&0xc0)>>4 | (pixels[x, y]&0xc0)>>6) 
        else:
            print("Incorrect resolution. Got (%d,%d) vs (%d, %d)"%(imwidth, imheight, self.width, self.height))
        return buf
    
    def display4Gray(self, image):
        layer1 = [0]*self.height*self.pages #< Bytes in frame
        for i in range(0, len(layer1)):
            temp3=0
            for j in range(0, 2):
                temp1 = image[i*2+j]
                for k in range(0, 2):
                    temp2 = temp1&0xC0 
                    if(temp2 == 0xC0):
                        temp3 |= 0x01#white
                    elif(temp2 == 0x00):
                        temp3 |= 0x00  #black
                    elif(temp2 == 0x80): 
                        temp3 |= 0x01  #gray1
                    else: #0x40
                        temp3 |= 0x00 #gray2
                    temp3 <<= 1	
                    
                    temp1 <<= 2
                    temp2 = temp1&0xC0 
                    if(temp2 == 0xC0):  #white
                        temp3 |= 0x01
                    elif(temp2 == 0x00): #black
                        temp3 |= 0x00
                    elif(temp2 == 0x80):
                        temp3 |= 0x01 #gray1
                    else :   #0x40
                            temp3 |= 0x00 #gray2	
                    if(j!=1 or k!=1):				
                        temp3 <<= 1
                    temp1 <<= 2
            layer1[i] = temp3
            
        layer2 = [0]*self.height*self.pages #< Bytes in frame
        for i in range(0, len(layer2)):
            temp3=0
            for j in range(0, 2):
                temp1 = image[i*2+j]
                for k in range(0, 2):
                    temp2 = temp1&0xC0 
                    if(temp2 == 0xC0):
                        temp3 |= 0x01#white
                    elif(temp2 == 0x00):
                        temp3 |= 0x00  #black
                    elif(temp2 == 0x80):
                        temp3 |= 0x00  #gray1
                    else: #0x40
                        temp3 |= 0x01 #gray2
                    temp3 <<= 1	
                    
                    temp1 <<= 2
                    temp2 = temp1&0xC0 
                    if(temp2 == 0xC0):  #white
                        temp3 |= 0x01
                    elif(temp2 == 0x00): #black
                        temp3 |= 0x00
                    elif(temp2 == 0x80):
                        temp3 |= 0x00 #gray1
                    else:    #0x40
                            temp3 |= 0x01   #gray2
                    if(j!=1 or k!=1):					
                        temp3 <<= 1
                    temp1 <<= 2
            layer2[i] = temp3

        self.set4GrayLut()
        self.command(0x10).data(layer1)
        self.command(0x13).data(layer2)
        self.command(0x12).waitWhileBusy()
