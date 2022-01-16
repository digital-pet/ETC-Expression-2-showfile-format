# ETC Expression 2 Showfile Format
A WIP parser for the proprietary show file format used with the ETC Expression 2, Insight 2, and Express lighting consoles, among others.

## File header

16 bytes, "ETC EXP II" zero padded

Index follows immediately with the first "entry" having type 0x0 and index 0x0 denoting the size, offset (always 0x20) and checksum of the remaining index.

## Index format

An array of the following struct

```
struct {
short type, // bitfield
short index,  //BCD for cues, hex for submasters
int checksum,
size_t data_size,
fpos_t data_offset
}
```

## Checksum (pseudocode)

```
int xor = 0
int sum16 = 0
int iter = 0
foreach char in data {
xor += (char ^ iter)
sum16 += char
iter++
}
checksum = (xor * 0x10000) | (sum16 & 0xFFFF)
```
