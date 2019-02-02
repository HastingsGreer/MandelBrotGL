import pyopencl as cl
import numpy as np

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
        mf = cl.mem_flags

        #initialize client side (CPU) arrays
        self.c_real = np.array(np.linspace(xmin, xmax, settings.dim), dtype = np.float64)
        self.c_imag = np.array(np.linspace(ymin, ymax, settings.dim), dtype = np.float64)
        
        self.c_real, self.c_imag = np.meshgrid(self.c_real, self.c_imag)
        
        self.c_real = np.array(self.c_real.flatten(), dtype = np.float64)
        self.c_imag = np.array(self.c_imag.flatten(), dtype = np.float64)
        
        self.depth = np.array([settings.depth, settings.dim], dtype = np.int32)

        #create OpenCL buffers
        self.real_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.c_real)
        self.imag_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.c_imag)
        self.depth_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = self.depth)
        self.dest_buf = cl.Buffer(self.ctx, mf.WRITE_ONLY, self.c_real.nbytes)

    def execute(self, settings):
        self.program.mandel(self.queue, (self.c_real.shape[0],), None, self.real_buf, self.imag_buf, self.depth_buf, self.dest_buf)
        counts = np.zeros(settings.dim**2, dtype = np.int32)
        cl._enqueue_read_buffer(self.queue, self.dest_buf, counts).wait()
        return counts.reshape([settings.dim, settings.dim])
        
    def getcounts(self, xmin, xmax, ymin, ymax, settings):
        self.popCorn(xmin, xmax, ymin, ymax, settings)
        return self.execute(settings)
        



if __name__ == "__main__":
    example.popCorn()
    example.execute()
