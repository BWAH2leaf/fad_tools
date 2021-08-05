import io
import os
from struct import *

def fad_unpack():
    print('fad_unpack')
    with open('anm0.fad', 'rb') as F:
        F.seek( int('30', 16) )
        FileNameListOffset = unpack('<l', F.read( 4 ) )[0]
        F.seek( int('24', 16) )
        DataStartOffset = unpack('<l', F.read( 4 ) )[0]

        F.seek( FileNameListOffset )
        FileNameData = io.BytesIO( F.read( DataStartOffset - FileNameListOffset ) )

        NextPos = int('40', 16)
        while True:
            F.seek( NextPos )
            DataName = F.read(8)
            DataSize = F.read(4)
            DataType = F.read(4)
            DataOffset = F.read(4)
            NoneData = F.read( int('c', 16 ) )
            NextPos = F.tell()

            print( NextPos, DataName.hex() )

            F.seek( unpack('<l', DataOffset )[0] )
            tempData = F.read( unpack('<l', DataSize )[0] )

            FileNameOffset = unpack('<l',tempData[ int('10',16):int('10',16)+4 ])[0]

            FileNameData.seek( FileNameOffset )
            FullName = b''
            while True:
                tempBytes = FileNameData.read(1)
                if tempBytes.hex() == '00' or tempBytes.hex() == '':
                    break
                else:
                    FullName+= tempBytes

            with open( '.\\fad_ex\\'+FullName.decode('utf8'), 'wb' ) as NF:
                NF.write( tempData )

            print(FullName.decode('utf8'))

            if NextPos == int('1880',16):
                break

if __name__=='__main__':
    fad_unpack()
