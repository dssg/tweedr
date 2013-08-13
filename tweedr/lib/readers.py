import csv
from StringIO import StringIO


def infer(s):
    if s.isdigit():
        return int(s)
    elif s.isalpha():
        return s
    return float(s)


def read_simple_csv(path):
    rows = []
    with open(path) as csv_fp:
        for line in csv_fp:
            rows.append([infer(cell) for cell in line.strip().split(',')])
    return rows


def read_until(readable, marks):
    '''Could stall if mark never happens before the EOF'''
    stdout_buffer = StringIO()
    while True:
        # read in bytes one-by-one because we have to break as soon as we hit
        #   any `mark` character
        byte = readable.read(1)
        if byte in marks:
            output = stdout_buffer.getvalue()
            stdout_buffer.close()
            return output
        stdout_buffer.write(byte)


class SniffingDictReader(csv.DictReader, object):
    # csv.DictReader(csvfile, fieldnames=None, restkey=None, restval=None, dialect='excel', *args, **kwds)
    def __init__(self, csvfile, restkey=None, restval=None):
        sniffer = csv.Sniffer()
        # sniff the first line
        sample = csvfile.readline()
        dialect = sniffer.sniff(sample)
        # rewind
        csvfile.seek(0)

        super(SniffingDictReader, self).__init__(csvfile, restkey=restkey, restval=restval, dialect=dialect)
