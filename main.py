import argparse, os, struct

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--Input")
    parser.add_argument("-o", "--Output")

    args = parser.parse_args()

    if args.Input:

        file =  args.Input.split("\\")[-1]
        filename = os.path.splitext(file)[0]

        try:
            with open(args.Input, "rb") as f_in:
                count = struct.unpack("<I", f_in.read(4))[0]
                table_entries = []
                for i in range(count):
                    table_entries.append((struct.unpack("<I", f_in.read(4))[0], struct.unpack("<I", f_in.read(4))[0]))
                
                index = 0
                for table_entry in table_entries:
                    f_in.seek(table_entry[0], 0)
                    compressedData = bytearray(f_in.read(table_entry[1]))
                    uncompressedData = DualExpLz8(compressedData, table_entry[1])
                    if args.Output == None:
                        f_out = open(filename + "_" + "decompressed" + "_" + str(index), "wb")
                    else:
                        f_out = open(args.Output + "//" + filename + "_" + "decompressed" + "_" + str(index), "wb")
                    f_out.write(uncompressedData)
                    f_out.close()
                    index += 1
        except IOError:
            print('Error While Opening the file!')

def DualExpLz8 (compressedData, compressedSize):

    uncompressedData = bytearray()

    dPos = 0
    sPos = 0
    
    while True:

        # 00119dc4
        t0 = ToSignedByte(compressedData[sPos])
        sPos += 1

        if t0 >= 0:
            v0 = compressedData[sPos]

            # 00119de0
            v1 = compressedData[sPos + 1]
            sPos += 2
            v1 = v1 << 8
            v0 = v1 | v0
            v1 = v0 & 0x3FF
            t2 = dPos + v1
            v1 = v0 >> 0xA       

            # 00119DFC
            while True:
                v0 = uncompressedData[t2 - 0x400]
                t2 += 1
                uncompressedData.append(v0)
                dPos += 1
                if v1 == 0:
                    break
                v1 -= 1
            
            # 00119E18
            v0 = uncompressedData[t2 - 0x400]
            uncompressedData.append(v0)
        
        else:
            v0 = compressedData[sPos]

            # 00119DD4
            sPos += 1
            uncompressedData.append(v0)
        
        # 00119E20
        v0 = t0 & 0x40
        if sPos == compressedSize:
            dPos += 1
            return uncompressedData
        else:
            dPos += 1

            # 00119E2C
        if v0 == 0:
            v0 = compressedData[sPos]
            
            # 00119E40
            v1 = compressedData[sPos + 1]
            sPos += 2
            v1 = v1 << 8
            v0 = v1 | v0
            v1 = v0 & 0x3FF
            t2 = dPos + v1
            v1 = v0 >> 0xA       

            # 00119E5C
            while True:
                v0 = uncompressedData[t2 - 0x400]
                t2 += 1
                uncompressedData.append(v0)
                dPos += 1
                if v1 == 0:
                    break
                v1 -= 1
            
            # 00119E78
            v0 = uncompressedData[t2 - 0x400]
            uncompressedData.append(v0)
        else:    
            v0 = compressedData[sPos]
        
            # 00119E34
            sPos += 1
            uncompressedData.append(v0)

        # 00119E80
        v0 = t0 & 0x20
        if sPos == compressedSize:
            dPos += 1
            return uncompressedData
        else:
            dPos += 1
        
            # 00119E8C
        if v0 == 0:
            v0 = compressedData[sPos]
            
            # 00119EA0
            v1 = compressedData[sPos + 1]
            sPos += 2
            v1 = v1 << 8
            v0 = v1 | v0
            v1 = v0 & 0x3FF
            t2 = dPos + v1
            v1 = v0 >> 0xA       

            # 00119EBC
            while True:
                v0 = uncompressedData[t2 - 0x400]
                t2 += 1
                uncompressedData.append(v0)
                dPos += 1
                if v1 == 0:
                    break
                v1 -= 1
            
            # 00119ED8
            v0 = uncompressedData[t2 - 0x400]
            uncompressedData.append(v0)
        else:
            v0 = compressedData[sPos]
        
            # 00119E94
            sPos += 1  
            uncompressedData.append(v0)

        # 00119EE0        
        v0 = t0 & 0x10
        if sPos == compressedSize:
            dPos += 1
            return uncompressedData
        else:
            dPos += 1
        
            # 00119EEC 
        if v0 == 0:
            v0 = compressedData[sPos]

            # 00119F00 
            v1 = compressedData[sPos + 1]
            sPos += 2
            v1 = v1 << 8
            v0 = v1 | v0
            v1 = v0 & 0x3FF
            t2 = dPos + v1
            v1 = v0 >> 0xA

            # 00119F1C
            while True:
                v0 = uncompressedData[t2 - 0x400]
                t2 += 1
                uncompressedData.append(v0)
                dPos += 1
                if v1 == 0:
                    break
                v1 -= 1

            # 00119F38
            v0 = uncompressedData[t2 - 0x400]
            uncompressedData.append(v0)
        else:
            v0 = compressedData[sPos]
        
            # 00119EF4
            sPos += 1  
            uncompressedData.append(v0)

        # 00119F40      
        v0 = t0 & 0x8
        if sPos == compressedSize:
            dPos += 1
            return uncompressedData
        else:
            dPos += 1
        
            # 00119F4C  
        if v0 == 0:
            v0 = compressedData[sPos]

            # 00119F60 
            v1 = compressedData[sPos + 1]
            sPos += 2
            v1 = v1 << 8
            v0 = v1 | v0
            v1 = v0 & 0x3FF
            t2 = dPos + v1
            v1 = v0 >> 0xA

            # 00119F7C
            while True:
                v0 = uncompressedData[t2 - 0x400]
                t2 += 1
                uncompressedData.append(v0)
                dPos += 1
                if v1 == 0:
                    break
                v1 -= 1

            # 00119F98
            v0 = uncompressedData[t2 - 0x400]
            uncompressedData.append(v0)
        else:
            v0 = compressedData[sPos]
        
            # 00119F54
            sPos += 1  
            uncompressedData.append(v0)

        # 00119FA0      
        v0 = t0 & 0x4
        if sPos == compressedSize:
            dPos += 1
            return uncompressedData
        else:
            dPos += 1
        
            # 00119FAC 
        if v0 == 0:
            v0 = compressedData[sPos]
                
            # 00119FC0
            v1 = compressedData[sPos + 1]
            sPos += 2
            v1 = v1 << 8
            v0 = v1 | v0
            v1 = v0 & 0x3FF
            t2 = dPos + v1
            v1 = v0 >> 0xA
            
            # 00119FDC
            while True:
                v0 = uncompressedData[t2 - 0x400]
                t2 += 1
                uncompressedData.append(v0)
                dPos += 1
                if v1 == 0:
                    break
                v1 -= 1
            
            # 00119FF8
            v0 = uncompressedData[t2 - 0x400]
            uncompressedData.append(v0)
        else:
            v0 = compressedData[sPos]

            # 00119FB4
            sPos += 1
            uncompressedData.append(v0)

        # 0011A000
        v0 = t0 & 0x2
        if sPos == compressedSize:
            dPos += 1
            return uncompressedData
        else:
            dPos += 1
        
            # 0011A00C
        if v0 == 0:
            v0 = compressedData[sPos]

            # 0011A020
            v1 = compressedData[sPos + 1]
            sPos += 2
            v1 = v1 << 8
            v0 = v1 | v0
            v1 = v0 & 0x3FF
            t2 = dPos + v1
            v1 = v0 >> 0xA
            
            # 0011A03C
            while True:
                v0 = uncompressedData[t2 - 0x400]
                t2 += 1
                uncompressedData.append(v0)
                dPos += 1
                if v1 == 0:
                    break
                v1 -= 1
            
            # 0011A058
            v0 = uncompressedData[t2 - 0x400]
            uncompressedData.append(v0)
        else:
            v0 = compressedData[sPos]
        
            # 0011A014
            sPos += 1
            uncompressedData.append(v0)

        # 0011A060
        v0 = t0 & 0x1
        if sPos == compressedSize:
            dPos += 1
            return uncompressedData
        else:
            dPos += 1
        
            # 0011A06C
        if v0 == 0:
            v0 = compressedData[sPos]

            # 0011A080
            v1 = compressedData[sPos + 1]
            sPos += 2
            v1 = v1 << 8
            v0 = v1 | v0
            v1 = v0 & 0x3FF
            t2 = dPos + v1
            v1 = v0 >> 0xA
            
            # 0011A09C
            while True:
                v0 = uncompressedData[t2 - 0x400]
                t2 += 1
                uncompressedData.append(v0)
                dPos += 1
                if v1 == 0:
                    break
                v1 -= 1
            
            # 0011A0B8
            v0 = uncompressedData[t2 - 0x400]
            uncompressedData.append(v0)
        else:
            v0 = compressedData[sPos]
        
            # 0011A074
            sPos += 1
            uncompressedData.append(v0)

        # 0011A0C0
        if sPos == compressedSize:
            dPos += 1
            return uncompressedData
        else:
            dPos += 1
                


def ToSignedByte(byte):
    if byte > 127:
        return -(256 - byte) 
    else:
        return byte

if __name__ == "__main__":
    main()