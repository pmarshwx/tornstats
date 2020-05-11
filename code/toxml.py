import argparse
import pathlib

import pandas as pd


### Command-Line Argument Parser ###
parser = argparse.ArgumentParser()
parser.add_argument("-y", "--year", required=False, default=None, help="Year to process")
args = parser.parse_args()

if args.year is None:
    import datetime
    year = datetime.datetime.utcnow().year
else:
    year = int(args.year)


print("Processing Year: {:d}".format(year))
fin = pathlib.Path("..", "csv", f"{year:d}-killer-tornadoes.csv")
fout = pathlib.Path("..", "xml", f"{year:d}.xml")

df = pd.read_csv(fin)
columns = df.columns

def df2xml(x):
    cols = []
    cols.append('{:s}="{:d}"'.format(columns[0], x[columns[0]]))         # yrnum
    cols.append('{:s}="{:s}"'.format(columns[1], x[columns[1]]))         # date
    cols.append('{:s}="{:s}"'.format(columns[2], x[columns[2]]))         # dt
    cols.append('{:s}="{:s}"'.format(columns[3], x[columns[3]]))         # time
    cols.append('{:s}="{:s}"'.format(columns[4], x[columns[4]]))         # tz
    cols.append('{:s}="{:s}"'.format(columns[5], x[columns[5]]))         # location
    cols.append('{:s}="{:s}"'.format(columns[6], x[columns[6]]))         # st
    cols.append('{:s}="{:d}"'.format(columns[7], x[columns[7]]))         # deaths
    cols.append('{:s}="{:d}"'.format(columns[8], x[columns[8]]))         # intor
    cols.append('{:s}="{:d}"'.format(columns[9], x[columns[9]]))         # insvr
    cols.append('{:s}="{:d}"'.format(columns[10], x[columns[10]]))       # nrsvr
    cols.append('{:s}="{:d}"'.format(columns[11], x[columns[11]]))       # nowatch
    cols.append('{:s}="{:s}"'.format(columns[12], x[columns[12]]))       # watch
    cols.append('{:s}="{:d}"'.format(columns[13], x[columns[13]]))       # ef
    cols.append('{:s}="{:d}"'.format(columns[14], x[columns[14]]))       # h
    cols.append('{:s}="{:d}"'.format(columns[15], x[columns[15]]))       # m
    cols.append('{:s}="{:d}"'.format(columns[16], x[columns[16]]))       # o
    cols.append('{:s}="{:d}"'.format(columns[17], x[columns[17]]))       # p
    cols.append('{:s}="{:d}"'.format(columns[18], x[columns[18]]))       # v
    cols.append('{:s}="{:d}"'.format(columns[19], x[columns[19]]))       # unk
    cols.append('{:s}="{:.4f}"'.format(columns[20], x[columns[20]]))     # slat
    cols.append('{:s}="{:.4f}"'.format(columns[21], x[columns[21]]))     # slon
    cols.append('{:s}="{:.4f}"'.format(columns[22], x[columns[22]]))     # elat
    cols.append('{:s}="{:.4f}"'.format(columns[23], x[columns[23]]))     # elon
    entry = "<fatalities {:s}/>".format(" ".join(cols))
    return entry


xmlrows = df.apply(df2xml, axis=1)
torns = "\n".join(xmlrows)

summaries = [(d, dd.deaths.sum()) for d,dd in df.groupby("st") if dd.deaths.sum() > 0]
summaries.sort(key=lambda x: x[1], reverse=True)
summary = "\n".join(["<summary STATE=\"{:s}\" FATALITIES=\"{:d}\"/>".format(s[0].upper(), s[1]) for s in summaries])

circumstances = ["h", "m", "o", "p", "v", "unk"]
csummaries = [(d, df[d].sum()) for d in circumstances]
csummaries.sort(key=lambda x: x[1], reverse=True)
csummary = "<csummary {:s}/>".format(" ".join(["{:s}=\"{:d}\"".format(c[0].upper(), c[1]) for c in csummaries]))

total = "<total TOTAL=\"{:d}\"/>".format(df.deaths.sum())

final_xml = "<?xml version=\"1.0\"?>\n<fatalities>\n{:s}\n{:s}\n{:s}\n{:s}\n</fatalities>".format(torns, summary, csummary, total)

with open(fout, "w") as OUT:
    OUT.write(final_xml)
