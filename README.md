# projconv
Convert between projections used by different map systems.

## Currently supported projections
* RT90 -- Old Swedish standard "Rikets referenssystem 1990".
* SWEREF -- Swedish Reference Frame 1990. Used by Lantmäteriverket. Based on ETRS89.
* WGS84 -- World Geodetic System. Used by GPS and Google Maps.

## Usage
```
usage: projconv.py [-h] [-ip {R,S,W}] [-iy <lat>] [-ix <long>] [-id <char>]
                   [-il <col>] [-ie <enc>] [-op {R,S,W}] [-od <char>]
                   [-oe <enc>] [-append] [-l]
                   [infile] [outfile]

Convert between RT90, SWEREF99 and WGS84

positional arguments:
  infile       input file name
  outfile      output file name

optional arguments:
  -h, --help   show this help message and exit
  -ip {R,S,W}  input coordinate projection, [R]T90, [S]WEREF99, [W]GS84
  -iy <lat>    input latitude column number
  -ix <long>   input longitude column number
  -id <char>   input column delimiter
  -il <col>    input label column number, if not given first output column
               will be label
  -ie <enc>    input encoding, ex. 'iso8859-1' or 'utf-8'
  -op {R,S,W}  output coordinate projection, [R]T90, [S]WEREF99, [W]GS84
  -od <char>   output column delimiter
  -oe <enc>    output encoding
  -append      copy input to output and add tranformed columns
  -l           list supported projections / coordinate systems
```

If an outfile is not given, projconv will print to standard out. If an infile is not
given, it will read from standard in.

## Examples

### 1. RT90 to Google Maps
Read a CSV file exported from Excel with RT90 and output WGS84. Column
delimiter is ';' and column order is X, Y. Something like this:

```
RT90 X;RT90 Y
1233368;5313112
2236118;4406072
3231600;3472700
4214876;2400189
```

To convert this to WGS84:

```
$ python projconv.py -ip R -op W -ix 1 -iy 2 -od , rt90.csv wgs84.csv
```

Given these switches:

| switch | descr                                |
|--------|--------------------------------------|
| -ip R  | Input format is RT90                 |
| -op W  | Output format is WGS84               |
| -ix 1  | Coordinate X is in the first column  |
| -iy 2  | Coordinate Y is in the second column |
| -od ,  | Output column delimiter is comma     |

It will render this output:

```
LAT,LONG
9.396777375768838,48.662851512707356
18.2068508594007,42.471193083202664
27.73900463330521,35.5889660602486
37.6295572304569,25.98982771143085
```

This format can be directly imported into a layer on Google Maps.

### 2. WGS84 With Labels to SWEREF99
Read a CSV file exported from Excel with SWEREF99 coordinates and output RT90. Column
delimiter is ',' for input and ';' for output files. Column order is LAT,LONG and the
label is in column 1.

```
LABEL;LAT,LONG
PLATS 1;9.396777375768838,48.662851512707356
PLATS 2;18.2068508594007,42.471193083202664
PLATS 3;27.73900463330521,35.5889660602486
PLATS 4;37.6295572304569,25.98982771143085
PLATS 4;4214876;2400189
```

To convert:

```
$ python3 projconv.py -ip W -op S -il 1 -iy 2 -ix 3 -id , wgs84.csv sweref99.csv
```

Given these switches:

| switch | descr                                |
|--------|--------------------------------------|
| -ip W  | Input format is WGS84                | 
| -op S  | Output format is SWEREF99            |
| -il 1  | Label is in first column             |
| -ix 1  | Lattitude is is in the second column |
| -iy 2  | Longitude is in the third column     |
| -id ,  | Input column delimiter is comma      |

It will render this output:

```
LABEL;N;E
PLATS 1;5405145;87491
PLATS 2;4707078;763627
PLATS 3;4013952;1657117
PLATS 4;3080894;2801626
```
