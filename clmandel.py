import pyopencl as cl
import numpy as np
import mpmath
mpmath.mp.prec = 290
import random

class CL:
    def __init__(self, filename):
        self.ctx = cl.create_some_context()
        self.queue = cl.CommandQueue(self.ctx)
        self.loadProgram(filename)

    def loadProgram(self, filename):
        #read in the OpenCL source file as a string
        f = open(filename, 'r')
        fstr = "".join(f.readlines())
        print(fstr)
        #create the program
        self.program = cl.Program(self.ctx, fstr).build()

    def popCorn(self, xmin, xmax, ymin, ymax, settings):

        bestdepth = 0
    
        bestz = []
        for __ in range(2):
            print(".", end="")
            if __ == 0:
                c1 =.5
                c2 = .5
            else:
                c1 = random.random()
                c2 = random.random()
            centerx, centery = (c1 * xmax + (1 - c1) * xmin), (c2 * ymax + (1 - c2) * ymin)


            z_real_array = [0]
            z_imag_array = [0]
            z_real = 0
            z_complex = 0
            i = 0
            while i < settings.depth and z_real**2 + z_complex**2 < 1000:
                z_real, z_complex = z_real**2 - z_complex**2 + centery, 2 * z_real * z_complex + centerx
                z_real_array.append(float(z_real))
                z_imag_array.append(float(z_complex))
                i += 1
            if i > bestdepth:
                bestdepth = i
                bestz = z_real_array, z_imag_array
                bestcx, bestcy = centerx, centery
            if i == settings.depth:
                break
        print("found c")
        x, y = np.mgrid[float(ymin - bestcy):float(ymax - bestcy):settings.dim * 1j, 
                        float(xmin-bestcx):float(xmax-bestcx):settings.dim * 1j]
        print("Step", x[0, 0] - x[1, 1])
        print(x.dtype)
        self.x = x.flatten()
        self.y = y.flatten()
        ref_real_array = np.array(bestz[0])
        ref_imag_array = np.array(bestz[1])
        

        mf = cl.mem_flags

  
        
        self.depth = np.array([settings.depth, settings.dim], dtype = np.int32)

        #create OpenCL buffers
        self.ref_real_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=ref_real_array)
        self.ref_imag_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=ref_imag_array)

        self.real_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.x)
        self.imag_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.y)
        self.x[:] = 0
        self.depth_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = self.depth)
        self.dest_buf = cl.Buffer(self.ctx, mf.WRITE_ONLY, self.x.nbytes)

    def execute(self, settings):
        self.program.mandel(self.queue, (self.x.shape[0],), None, self.ref_real_buf, self.ref_imag_buf,
         self.real_buf, self.imag_buf, self.depth_buf, self.dest_buf)
        counts = np.zeros(settings.dim**2, dtype = np.int32)
        cl._enqueue_read_buffer(self.queue, self.dest_buf, counts).wait()
        return counts.reshape([settings.dim, settings.dim])
        
    def getcounts(self, xmin, xmax, ymin, ymax, settings):
        self.popCorn(xmin, xmax, ymin, ymax, settings)
        return self.execute(settings)
        



if __name__ == "__main__":
    example.popCorn()
    example.execute()
