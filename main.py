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

    comparaison_values = [0x40, 0x20, 0x10, 0x8, 0x4, 0x2, 0x1]
    
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
        
        for value in comparaison_values:

            # 00119E20
            v0 = t0 & value
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