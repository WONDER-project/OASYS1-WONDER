import os, numpy
import orangecontrib.wonder.fit.functions.wppm_functions as wf

def run_gsas_ii():
    datadir = "/Users/lrebuffi/Documents/Workspace/Wonder/GSAS-TEST"
    cif_file = os.path.join(datadir,"LaB6_NISTSRM_660a.cif")

    datadir = "/Users/lrebuffi/Documents/Workspace/Wonder/Orange3-WONDER/Use_Cases/FeMoMCX"
    cif_file = os.path.join(datadir,"Fe_bcc.cif")

    reflections = wf.gsasii_load_reflections(cif_file, 0.0826, 5.0, 140.0)

    print(reflections.get_reflection(1, 1, 0))
    print(reflections.get_reflection(4, 1, 1))

    print ("h, k, l, 2th, mult, F2, int")

    reflections = reflections.get_reflections()

    tth = numpy.zeros(len(reflections))
    ints = numpy.zeros(len(reflections))

    i = 0
    for reflection in reflections:
        print(reflection)
        tth[i] = reflection.pos
        ints[i] = reflection.get_intensity_factor()
        i += 1

    from matplotlib import pyplot as plt

    plt.bar(tth,ints)
    plt.show()


def run_gsasii_test_2():
    import os, sys
    sys.path.insert(0, '/Users/lrebuffi/Documents/Workspace/Wonder/GSAS-II-WONDER-OSX/GSAS-II-WONDER')  # needed to "find" GSAS-II modules

    datadir = "/Users/lrebuffi/Documents/Workspace/Wonder/GSAS-TEST"

    import GSASIIscriptable as G2sc

    PathWrap = lambda fil: os.path.join(datadir, fil)
    gpx = G2sc.G2Project(newgpx=PathWrap('pkfit.gpx'))
    hist = gpx.add_powder_histogram(PathWrap('FAP.XRA'), PathWrap('INST_XRY.PRM'),
                                    fmthint='GSAS powder')
    hist.set_refinements({'Limits': [16., 24.],
                          'Background': {"no. coeffs": 2, 'type': 'chebyschev-1', 'refine': True}
                          })
    peak1 = hist.add_peak(1, ttheta=16.8)
    peak2 = hist.add_peak(1, ttheta=18.9)
    peak3 = hist.add_peak(1, ttheta=21.8)
    peak4 = hist.add_peak(1, ttheta=22.9)
    hist.set_peakFlags(area=True)
    hist.refine_peaks()
    hist.set_peakFlags(area=True, pos=True)
    hist.refine_peaks()
    hist.set_peakFlags(area=True, pos=True, sig=True, gam=True)
    hist.refine_peaks()
    print('peak positions: ', [i[0] for i in hist.PeakList])
    for i in range(len(hist.Peaks['peaks'])):
        print('peak', i, 'pos=', hist.Peaks['peaks'][i][0], 'sig=', hist.Peaks['sigDict']['pos' + str(i)])
    hist.Export_peaks('pkfit.txt')

    return hist

if __name__=="__main__":
    hist = run_gsasii_test_2()

    from matplotlib import pyplot as plt

    plt.plot(hist.data['data'][1][0], hist.data['data'][1][1])
    plt.show()
