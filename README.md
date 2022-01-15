# ETC Expression 2 Showfile Format
A WIP parser for the ETC Expression 2 showfile format.

## File header

16 bytes, "ETC EXP II" zero padded

## Index format

struct {
char minorType,
char majorType,
short index,
int checksum,
int size,
void* ptr
}

## Checksum (pseudocode)

int xor = 0
int sum16 = 0
foreach char in data {
xor += (char ^ iter)
sum += char
}
checksum = (xor * 0x10000) | (sum & 0xFFFF)
