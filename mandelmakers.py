import numpy as np
from subprocess import Popen
import subprocess

def getcounts(xmin, xmax, ymin, ymax, settings):
    """render a view of the mandelbrot set on the given rectangle of the
    complex plane, by calling a C script and interpreting stdout as a series of integers
    output is a numpy array reshaped into a dim*dim square"""
     
    p = Popen(["./a.out", repr(xmin), 
        repr(xmax), repr(ymin),repr(ymax), str(settings.dim), str(settings.depth)], stdout=subprocess.PIPE)
        
    print repr(xmin), repr(xmax), repr(ymin),repr(ymax), str(settings.dim), str(settings.depth)

    counts = np.fromstring(p.stdout.readline()[:-1], dtype = np.int, sep = ' ')
   
    return counts.reshape([settings.dim, settings.dim]).transpose()

def getcounts2(xmin, xmax, ymin, ymax, settings):
    XDIM = settings.dim
    YDIM = settings.dim

    xmin = settings.center[0] - settings.scale
    xmax = settings.center[0] + settings.scale
    ymin = settings.center[1] - settings.scale
    ymax = settings.center[1] + settings.scale
    
    re = np.linspace(xmin, xmax, XDIM)
    im = np.linspace(ymin, ymax, YDIM)
    
    cre, cim = np.meshgrid(re, im)
    
    cre = cre.flatten()
    cim = cim.flatten()
    crestatic = cre
    cimstatic = cim
    zrestatic = np.zeros(cre.shape).flatten()
    zimstatic = np.zeros(cim.shape).flatten()
    
    counts = np.zeros(cre.shape)
    countsstatic = counts
    
    zre = zrestatic
    zim = zimstatic
    positionstatic = np.array(range(len(zre)))
    position = positionstatic
    for j in xrange(0, settings.depth / 10):
        
        for i in xrange(0, 10):
            zre, zim = zre**2 - zim**2 + cre, 2 * zre * zim + cim
            norms = (zim**2 + zre**2)
            mask = norms > 4
            counts[np.invert(mask)] += 1
        countsstatic[position] = counts
        zrestatic[position] = zre
        zimstatic[position] = zim
        norms = (zimstatic**2 + zrestatic**2)
        
        mask = norms < 4
        zre = zrestatic[mask]
        zim = zimstatic[mask]
        cre = crestatic[mask]
        cim = cimstatic[mask]
        position = positionstatic[mask]
        counts = countsstatic[mask]
        
        
    return countsstatic.reshape([YDIM, XDIM])
