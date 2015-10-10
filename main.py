import numpy as np
import matplotlib.pyplot as plt
import itertools
from mandelmakers import getcounts, getcounts2
import clmandel

cl = clmandel.CL("mandel.cl")


class Settings:
    def __init__(self, depth, scale, dim, center):
        self.depth = depth
        self.scale = scale
        self.dim = dim
        self.center = center
        
        self.methods = itertools.cycle(( cl.getcounts, getcounts, getcounts2))
        self.changemethod()
    def changemethod(self):
        self.method = self.methods.next()

def main():
    #initial settings
    xmin = -2
    xmax = 2
    ymin = -2
    ymax = 2
     
    depth = 60   
    scale = 2
    dim = 600
    settings = Settings(depth, scale, dim, (0, 0))  
                                            # the settings object is used to keep track of
                                            # rendering settings as the click-generated 
                                            # callbacks change the view window
        
    counts = getcounts(xmin, xmax, ymin, ymax, settings)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    picture = ax.imshow(counts, extent = [xmin, xmax, ymax, ymin], interpolation = 'nearest')
    colorbar = fig.colorbar(picture, ax = ax)
    cid = fig.canvas.mpl_connect('button_press_event', lambda e: onclick(e, ax, colorbar, settings))
    cid = fig.canvas.mpl_connect('key_press_event', lambda e: onkey(e, ax, colorbar, settings))
    plt.show()
    
    
def onclick(event, ax, colorbar, settings):
    settings.scale *= .5                  #zoom in by a factor of two with every click
    settings.center = (event.xdata, event.ydata)
    render(ax, colorbar, settings)
    
    
def onkey(event, ax, colorbar, settings):
    key = event.key
    
    if key == "q":
        settings.depth = int(settings.depth * 2)
    elif key == "a":
        settings.depth = int(settings.depth / 2)
    elif key == "e":
        settings.dim = int(settings.dim * 2)
    elif key == "d":
        settings.dim = int(settings.dim / 2)
    elif key == "w":
        settings.scale = settings.scale * 2
    elif key == "r":
        settings.changemethod()
        print settings.method
    else:
        return
    render(ax, colorbar, settings)

def render(ax, colorbar, settings):
    print str(settings.dim), str(settings.depth)
    ax.clear()
    xmin = settings.center[0] - settings.scale
    xmax = settings.center[0] + settings.scale
    ymin = settings.center[1] - settings.scale
    ymax = settings.center[1] + settings.scale
    cax = ax.imshow(settings.method(xmin, xmax, ymin, ymax, settings), extent = [xmin, xmax, ymax, ymin])
    colorbar.on_mappable_changed(cax)
    ax.figure.canvas.draw()
    

if __name__ == "__main__":
    main()
