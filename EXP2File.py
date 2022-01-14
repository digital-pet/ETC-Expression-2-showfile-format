from uint import Int as FixedInt
from struct import *
import logging
from binascii import hexlify, unhexlify
from io import BytesIO

class EXP2File:
    """ A Python library that parses ETC Expression II show files

    [extended_summary]
    """
    def __init__(self,strict = True):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.strict = strict

    def decode(self,fileBytes):
        """decode decodes a bytes object containing the contents of an EXP2.SHW file

        Args:
            fileBytes (Bytes): an EXP2.SHW file as a Bytes object

        Returns:
            Dict: A hierarchial representation of an ETC Expression 2 show file
        """
        magic = fileBytes[:16].decode().split('\0', 1)[0]

        self.logger.debug('decode(): Magic string found: {}'.format(magic))

        if magic != "ETC EXP II":
            self.logger.error('decode(): Magic string has lost its magic. Expected "ETC EXP II", got "{}".'.format(magic))
            if self.strict = True:
                return False

        self.logger.debug('decode(): Parsing header')
        recordType, recordIndex, chunk = parseRecord(fileBytes[16:32],fileBytes)

        if int.from_bytes(recordType, "little") != 0:
            self.logger.error('decode(): First record in index table is not of type 0000. (Got {})'.format(recordType.hex()))            
            if self.strict = True:
                return False
        
        elif int.from_bytes(recordIndex, "little") != 0:
            self.logger.error('decode(): First record in index table has non-null index value. (Got {})'.format(recordIndex.hex()))
            if self.strict = True:
                return False
        
        fileIndex = parseIndexChunk(chunk,fileBytes)

        for record in fileIndex:
            pass



        return outputDict

    def encode(self,data):
        """encode [summary]

        [extended_summary]

        Args:
            data ([type]): [description]

        Returns:
            Bytes: a byte representation of an EXP2.SHW file
        """
        SHWfile = BytesIO()
        nextDataOffset = 0x20

        outputBytes = False
        
        SHWfile.seek(0x0)
        
        SHWfile.write(b'ETC EXP II') #magic string
        
        SHWfile.seek(0x10)

        SHWfile.write(b'\x00\x00\x00\x00') #header type and index

        SHWfile.seek(0x1B)

        SHWfile.write(pack('<l',nextDataOffset)) #index offset is always 0x20 in the console, while it's technically relocatable the console may not like it elsewhere

        
        # TODO
        
        outputBytes = SHWfile.getvalue()

        return outputBytes

    def doChecksum(self,chunk):
        """doChecksum calculates data chunk checksums

        Args:
            chunk (bytes): a data chunk

        Returns:
            Bytes: the computed checksum (int32)
        """
        v1 = FixedInt(0,32)
        v2 = FixedInt(0,32)

        for i, b in enumerate(chunk):
            v1 = v1 + (i ^ b)
            v2 = v2 + b

        cs = (v1 * 0x10000) | (v2 & 0xFFFF)

        return pack('<l',cs)

    def parseRecord(self,record,fileBytes):
        """parseRecord parses an individual record

        Parses an individual record from the file index and extracts the data associated with it, also verifies checksums

        Args:
            record (Bytes): The index record to be parsed
            fileBytes (Bytes): an exp2.shw file

        Returns:
            Tuple: 
                Bytes: record type (uint16), 
                Bytes: record index (uint16),
                Bytes: data chunk
        """

        fs = '<2s2sLLL'

        result = unpack(fs,record)

        recordType              = result[0]
        index                   = result[1]
        checksum,size,offset    = result[2:]

        chunk = fileBytes[offset:(offset+size)]

        calculatedChecksum = doChecksum(chunk)

        if calculatedChecksum != checksum:
            self.logger.warning("Record type {}, index {} checksum incorrect. Expected {} got {}.".format(recordType.hex(),checksum.hex(),calculatedChecksum.hex()))    

        return recordType, index, chunk

    def parseIndexChunk(self,chunk,fileBytes):
        """parseIndexChunk parses a chunk with major type 00 minor type 00

        Args:
            chunk (Bytes): the data chunk extracted by parseRecord
            fileBytes (Bytes): an exp2.shw file

        Returns:
            list: a list of parseRecord tuples
        """
        recordList = []
        size = len(chunk)

        # ensure that the index chunk we've extracted is a valid size
        if (size % 16) != 0:
            self.logger.error('parseIndexChunk(): Chunk is not a multiple of 16 bytes. Aborting...')
            return False            

        numRecords = size / 16

        for i in range(numRecords):
            recordBytes = chunk[i*16:(i*16)+16]     # chop out 16 byte sections at a time
            recordList.append(parseRecord(recordBytes,fileBytes))
        
        return recordList

    def parseCueChunk(self,chunk):
        
        return cueStruct

    def parseSubmasterChunk(self,chunk):
        
        return subStruct

    def parseShowNameChunk(self,chunk):
        
        return showName

    def parseMacroChunk(self,chunk):
        
        return macroStruct

    def parsePatchChunk(self,chunk):
        
        return patchStruct

    def parseMLPersonalityChunk(self,chunk):
        
        return MLPersStruct

    def parseDMXOutSettingsChunk(self,chunk):
        
        return DMXOutStruct
    
    def parseChannelSettingsChunk(self,chunk):
        
        return channelSettingStruct

    def parseGroupChunk(self,chunk):

        return groupStruct
