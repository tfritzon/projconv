#!/usr/bin/python
# -*- coding: utf-8 -*-
import pyproj
import sys
import csv
import argparse
import codecs

#
# Projections
#
projs = {
    # RT90 2.5 gon V 0:-15
    'R' : { 'name' : "RT90",
            'EPSG' : '3021',
            'Y'    : 'Y',
            'X'    : 'X',
            'type' : int,
            'desc' : "Rikets koordinatsystem 1990, Sweden's old standard"
    },

    # SWEREF99 TM
    'S' : { 'name' : "SWEREF99",
            'EPSG' : '3006',
            'Y'    : 'N',
            'X'    : 'E',
            'type' : int,
            'desc' : "Swedish Reference Frame 1999, Lantmäteriverket, ETRS89"
    },

    # WGS84, projected koordinates
    'W' : { 'name' : "WGS84",
            'EPSG' : '4326',
            'Y'    : 'LAT',
            'X'    : 'LONG',
            'type' : float,
            'desc' : "World Geodetic System, GPS, Google Maps"
    },
}

for p in projs:
    projs[p]['proj'] = pyproj.Proj("+init=EPSG:%s" % projs[p]['EPSG'])

prjmap = { 'rt90' : projs['R'], 'sweref99' : projs['S'], 'wgs84' : projs['W'] }

def list_projs():
    for i in projs:
        p = projs[i]
        print("%s  %-10s%s (EPSG:%s)" % (i, p['name'], p['desc'], p['EPSG']))

#
# Arguments
#
parser = argparse.ArgumentParser(description="Convert between RT90, SWEREF99 and WGS84")
parser.add_argument('infile', type=str, nargs='?',
                    help="input file name")
parser.add_argument('-ip', type=str, choices=['R', 'S', 'W'], default='R',
                    help="input coordinate projection, [R]T90, [S]WEREF99, [W]GS84")
parser.add_argument('-iy', metavar='<lat>', type=int, default=2,
                    help="input latitude column number")
parser.add_argument('-ix', metavar='<long>', type=int, default=1,
                    help="input longitude column number")
parser.add_argument('-id', metavar='<char>', type=str, default=';',
                    help="input column delimiter")
parser.add_argument('-il', metavar='<col>', type=int,
                    help="input label column number, if not given first output column will be label")
parser.add_argument('-ie', metavar='<enc>', type=str, default='utf-8',
                    help="input encoding, ex. 'iso8859-1' or 'utf-8'")

parser.add_argument('outfile', type=str, nargs='?',
                    help="output file name")
parser.add_argument('-op', type=str, choices=['R', 'S', 'W'], default='S',
                    help="output coordinate projection, [R]T90, [S]WEREF99, [W]GS84")
parser.add_argument('-od', metavar='<char>', type=str, default=';',
                    help="output column delimiter")
parser.add_argument('-oe', metavar='<enc>', type=str, default='utf-8',
                    help="output encoding")

parser.add_argument('-append', action='store_true',
                    help="copy input to output and add tranformed columns")
parser.add_argument('-l', action='store_true',
                    help="list supported projections / coordinate systems")

args = parser.parse_args()

if args.l:
    list_projs()
    sys.exit(0)

progprojs = (sys.argv[0].split('.')[0]).split('_')

if len(progprojs) > 1:
    iproj = prjmap[progprojs[0]]
else:
    iproj = projs[args.ip]

if len(progprojs) > 1:
    oproj = prjmap[progprojs[1]]
else:
    oproj = projs[args.op]

cfin = csv.reader(sys.stdin, delimiter=args.id)
if args.infile is not None:
    cfin = csv.reader(open(args.infile, encoding=args.ie), delimiter=args.id)

headers = cfin.__next__()

cfout = csv.writer(sys.stdout, delimiter=args.od)
if args.outfile is not None:
    cfout = csv.writer(codecs.open(args.outfile, 'w', args.oe), delimiter=args.od)

if args.append:
    cfout.writerow(headers + [oproj['Y'], oproj['X']])
elif args.il is not None:
    cfout.writerow(['LABEL', oproj['Y'], oproj['X']])
else:
    cfout.writerow([oproj['Y'], oproj['X']])

f = oproj['type']

for row in cfin:
    x = float(row[args.ix-1])
    y = float(row[args.iy-1])
    e,n = pyproj.transform(iproj['proj'], oproj['proj'], y, x)

    if args.append:
        cfout.writerow(row + [f(n), f(e)])
    else:
        if args.il is None:
            cfout.writerow([f(n), f(e)])
        else:
            cfout.writerow([row[args.il-1], f(n), f(e)])
