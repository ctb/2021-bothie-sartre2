"""
Parse various 'sar' output files
"""
import pandas

def parse_cpu(fp):
    line = fp.readline()
    assert line.startswith('Linux ')

    line = fp.readline()
    assert not line.strip()

    header = fp.readline()
    assert ' CPU ' in header

    x = []
    while 1:
        line = fp.readline()
        if line.startswith('Average:'): # end line
            break
        if not line:
            assert 0, "unexpected end of file"

        tup = line.strip().split()
        timestr, cpu, puser, pnice, psystem, piowait, psteal, pidle = tup

        timestr = list(map(int, timestr.split(':')))
        timesec = timestr[0]*3600 + timestr[1]*60 + timestr[2]

        puser, pnice, psystem, piowait, psteal, pidle = map(float, tup[2:])
        d = {}
        d['timesec'] = timesec
        d['cpu'] = cpu
        d['puser'] = puser
        d['pnice'] = pnice
        d['psystem'] = psystem
        d['piowait'] = piowait
        d['psteal'] = psteal
        d['pidle'] = pidle

        x.append(d)

    return pandas.DataFrame(x)


def parse_disk(fp, target_device='nvme1n1'):
    line = fp.readline()
    assert line.startswith('Linux ')

    line = fp.readline()
    assert not line.strip()

    header = fp.readline()
    assert ' DEV ' in header

    x = []
    while 1:
        line = fp.readline()
        if line.startswith('Average:'): # end line
            break
        if not line:
            assert 0, "unexpected end of file"

        tup = line.strip().split()
        device = tup[1]
        if device != target_device: # skip reporting on other stuff
            continue

        timestr = tup[0]

        timestr = list(map(int, timestr.split(':')))
        timesec = timestr[0]*3600 + timestr[1]*60 + timestr[2]

        tps, read_kbps, write_kbps, d_kbps, areq_sz, aqu_sz, aawait, putil = map(float, tup[2:])
        
        d = {}
        d['timesec'] = timesec
        for key in 'tps, read_kbps, write_kbps, d_kbps, areq_sz, aqu_sz, aawait, putil'.split(', '):
            d[key] = locals()[key]

        x.append(d)

    return pandas.DataFrame(x)

def parse_ram(fp):
    line = fp.readline()
    assert line.startswith('Linux ')

    line = fp.readline()
    assert not line.strip()

    header = fp.readline()
    assert ' kbmemfree ' in header

    x = []
    while 1:
        line = fp.readline()
        if line.startswith('Average:'): # end line
            break
        if not line:
            assert 0, "unexpected end of file"

        tup = line.strip().split()
        timestr, kbmemfree, kbavail, kbmemused, pmemused, kbbuffers, kbcached, kbcommit, pcommit, kbactive, kbinact, kbdirty = tup

        timestr = list(map(int, timestr.split(':')))
        timesec = timestr[0]*3600 + timestr[1]*60 + timestr[2]

        kbmemfree, kbavail, kbmemused, pmemused, kbbuffers, kbcached, kbcommit, pcommit, kbactive, kbinact, kbdirty = map(float, tup[1:])
        d = {}
        d['timesec'] = timesec
        for key in 'kbmemfree, kbavail, kbmemused, pmemused, kbbuffers, kbcached, kbcommit, pcommit, kbactive, kbinact, kbdirty'.split(', '):
            d[key] = locals()[key]

        x.append(d)

    return pandas.DataFrame(x)
