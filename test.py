import luminance_meter.CS200 as cs200
import pylab
from tkinter import *
from tkinter import ttk
from colour.plotting import CIE_1931_chromaticity_diagram_plot
import time
import serial
import serial.tools.list_ports

#import matplotlib as plt
#matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt




def EN12966_chromaticity_diagramplot():
    fig = pylab.figure(1)
    CIE_1931_chromaticity_diagram_plot(title='', figure_size=(8,10), standalone=False)
    pylab.xlim([0,0.8])
    pylab.ylim([0,0.9])
    
	# RED C2
    pylab.plot([0.68, 0.66, 0.69, 0.71], [0.32, 0.32, 0.29, 0.29],'k-',color='#880000')
    # GREEN C2
    pylab.plot([0.009, 0.284, 0.209, 0.028], [0.72, 0.52, 0.4, 0.4],'k-',color='#008800')
    # BLUE C2
    pylab.plot([0.109, 0.173, 0.208, 0.149], [0.087, 0.16, 0.125, 0.025],'k-',color='#000088')
    # WHITE C2
    pylab.plot([0.3, 0.44, 0.44, 0.3, 0.3], [0.342, 0.432, 0.382, 0.276, 0.342],'k-',color='#BBBBBB')
    # YELLOW C2
    pylab.plot([0.547, 0.536, 0.593, 0.613], [0.452, 0.444, 0.387, 0.387],'k-',color='#CCCC00')
    # WITE/YELOW C2
    pylab.plot([0.479, 0.3, 0.3, 0.44, 0.618], [0.52, 0.342, 0.276, 0.382, 0.382],'k-',color='#CCCC88')

    # RED C1
    pylab.plot([0.68, 0.66, 0.721, 0.735], [0.32, 0.32, 0.256, 0.265],'k-',color='#CC0000')
    # GREEN C1
    pylab.plot([0.31, 0.31, 0.209, 0.028], [0.684, 0.562, 0.4, 0.4],'k-',color='#00CC00')
    # BLUE C1
    pylab.plot([0.109, 0.204, 0.233, 0.149], [0.087, 0.196, 0.167, 0.025],'k-',color='#0000FF')
    # WHITE C1
    pylab.plot([0.3, 0.44, 0.50, 0.5, 0.44, 0.3], [0.342, 0.432, 0.440, 0.382, 0.382, 0.276],'k-',color='#EEEEEE')
    # YELLOW C1
    pylab.plot([0.547, 0.536, 0.593, 0.613], [0.452, 0.444, 0.387, 0.387],'k-',color='#FFFF00')
    # WITE/YELOW C1
    pylab.plot([0.479, 0.3, 0.3, 0.44, 0.618], [0.52, 0.342, 0.276, 0.382, 0.382],'k-',color='#DDDD88')

    #pylab.plot(x, y, 'x', color='black')
    #pylab.plot(x, y, 'bs')
	#'ro' puntos rojos
	#'bs' cuadrado azul
	#'g^' triangulo verde
	   
	
    return fig

def beamPlot():
    r = np.arange(-35.0, 40.0, 5)
    figAngle = pylab.figure(2)
    hor = pylab.subplot(211)
    pylab.title('Horizontal º')
    ver = pylab.subplot(212)
    pylab.title('Vertical º')
    hor.set_xlim([-35,35])  
    ver.set_xlim([-35,35])  
    hor.set_xticks(r)
    ver.set_xticks(r)
    hor.grid(True)
    ver.grid(True)
    return figAngle
    

def addPointToCIE(x, y, c):
    fig = pylab.figure(1)
    pylab.plot(x, y, c)
    fig.canvas.draw()
	
def addPointToBeamH(l, d, c, m):
    fig = pylab.figure(2)
    hor = pylab.subplot(211)
    hor.plot(d, float(l)/float(m), c)
    hor.set_xlim([-35,35])
    hor.set_yticks([0, 0.5, 1])  
    fig.canvas.draw()
	
def addPointToBeamV(l, d, c, m):
    fig = pylab.figure(2)
    ver = pylab.subplot(212)
    ver.plot(d, float(l)/float(m), c)
    ver.set_xlim([-35,35])
    ver.set_yticks([0, 0.5, 1])  
    fig.canvas.draw()

def sendH(port):
    #arduino = serial.Serial(listPorts.get(),listSpeeds.get(),timeout=1)
    #time.sleep(1)
    port.write(b"O")
    #arduino.close()
    	
def sendV(port):
    #arduino = serial.Serial(listPorts.get(),listSpeeds.get(),timeout=1)
    #time.sleep(1)
    port.write(b'S')
    #arduino.close()

def getAllPorts(): ##OJO COMO PASAR ARGUMENTOS
    listSpeeds['values'] = ["9600", "19200", "38400", "57600", "115200", "250000"]
    listSpeeds.current(4)
    puertosCom = []
    for n1,n2,n3 in list(serial.tools.list_ports.comports()):
        puertosCom.append(n1)
    listPorts['values']=puertosCom
    if len(puertosCom) > 0:
        listPorts.current(0)
        
def enablePorts():		
    arduino = serial.Serial(listPorts.get(),listSpeeds.get(),timeout=1)
    time.sleep(1)
	
def readOne():
    color = ['rx', 'gx', 'bx', 'wx', 'yx', 'cx']
    select = color[int(colorEntry.get())]
    aux, lux, x, y = cs200.read_instrument(0)
    addPointToCIE(x,y,select)
    addPointToBeamH(lux,hEntry.get(),select,20)
    addPointToBeamV(lux,vEntry.get(),select,20)
   
	
def clearGraphics():
    fig1 = pylab.figure(1)
    fig1.clear()
    EN12966_chromaticity_diagramplot()
    fig1.canvas.draw()
    fig2 = pylab.figure(2)
    fig2.clear()
    beamPlot()
    fig2.canvas.draw()
    
    	
    
	
cs200.open_instrument(0)
#print(cs200.read_instrument(0))
	

master = Tk()
master.title("Lacroix Laboratory")
#master.geometry('1200x600')
master.wm_state('zoomed')


# Generate Controls
dataTree = ttk.Treeview(master)
groupMM039A = LabelFrame(master,text="MM039A",padx=10, pady=10)
groupLuminanceMeter = LabelFrame(master,text="Luminance Meter",padx=10, pady=10)
listPorts = ttk.Combobox(groupMM039A, width=8, state='readonly')
listSpeeds = ttk.Combobox(groupMM039A, width=8, state='readonly')
getAllPorts()
scanPorts = Button(groupMM039A, text="Scan", command=getAllPorts)
openPorts = Button(groupMM039A, text="ON/OFF", command=enablePorts)

hButton = Button(groupMM039A, text="H->", command=sendH)
vButton = Button(groupMM039A, text="V->", command=sendV)
hEntry = Entry(groupMM039A, width=5)
vEntry = Entry(groupMM039A, width=5)
hLabel = Label(groupMM039A, text="deg.")
vLabel = Label(groupMM039A, text="deg.")
setHButton = Button(groupMM039A, text="Set H")
setVButton = Button(groupMM039A, text="Set V")
goHButton = Button(groupMM039A, text="Go H")
goVButton = Button(groupMM039A, text="Go V")

scanPorts.grid(row=0, column=0)
listPorts.grid(row=0, column=1)
listSpeeds.grid(row=0, column=2)
openPorts.grid(row=0, column=3)
hButton.grid(row=1, column=0)
hEntry.grid(row=1, column=1)
hLabel.grid(row=1, column=2)
vButton.grid(row=2, column=0)
vEntry.grid(row=2, column=1)
vLabel.grid(row=2, column=2)
setHButton.grid(row=3, column=0)
setVButton.grid(row=3, column=1)
goHButton.grid(row=4, column=0)
goVButton.grid(row=4, column=1)

readOneButton = Button(groupLuminanceMeter, text="Read One", command=readOne)
clearButton = Button(groupLuminanceMeter, text="Clear", command=clearGraphics)
colorEntry = Entry(groupLuminanceMeter, width=5)
readOneButton.grid(row=0, column=0)
clearButton.grid(row=0, column=1)
colorEntry.grid(row=0, column=2)

dataTree["columns"]=("lum","x","y","Hor", "Ver")
dataTree.heading("lum", text="cd/m2")
dataTree.heading("x", text="x")
dataTree.heading("y", text="y")
dataTree.heading("Hor", text="Hor.")
dataTree.heading("Ver", text="Ver.")
dataTree.column("lum", width=100 )
dataTree.column("x", width=100 )
dataTree.column("y", width=100 )
dataTree.column("Hor", width=100 )
dataTree.column("Ver", width=100 )
dataTree.tag_configure('red', font=('Helvetica', 12),foreground='red')
dataTree.tag_configure('green', font=('Helvetica', 12),foreground='green')
dataTree.tag_configure('blue', font=('Helvetica', 12),foreground='blue')
dataTree.tag_configure('white', font=('Helvetica', 12),foreground='black')
dataTree.tag_configure('yellow', font=('Helvetica', 12),foreground='orange')
dataTree.tag_configure('greenC2', font=('Helvetica', 12),foreground='violet')
redData = dataTree.insert("", 1, "red", text="Red", tags=('red',))
greenData = dataTree.insert("", 2, "green", text="Green", tags=('green',))
blueData = dataTree.insert("", 3, "blue", text="Blue", tags=('blue',))
whiteData = dataTree.insert("", 4, "white", text="White", tags=('white',))
yellowData = dataTree.insert("", 5, "yellow", text="Yellow", tags=('yellow',))
greenC2Data = dataTree.insert("", 6, "greenC2", text="Green C2", tags=('greenC2',))

redData4 = dataTree.insert(redData, 1, "red4", text="40000lux 3100 - 15500", tags=('red',))
redData3 = dataTree.insert(redData, 2, "red3", text="4000lux  550 - 2750", tags=('red',))
redData2 = dataTree.insert(redData, 3, "red2", text="400lux   150 - 750", tags=('red',))
redData1 = dataTree.insert(redData, 4, "red1", text="40lux    63 - 315", tags=('red',))
redData0 = dataTree.insert(redData, 5, "red0", text="4lux     19 - 95", tags=('red',))

greenData4 = dataTree.insert(greenData, 1, "green4", text="40000lux 3720 - 18600", tags=('green',))
greenData3 = dataTree.insert(greenData, 2, "green3", text="4000lux  660 - 3300", tags=('green',))
greenData2 = dataTree.insert(greenData, 3, "green2", text="400lux   180 - 900", tags=('green',))
greenData1 = dataTree.insert(greenData, 4, "green1", text="40lux    75 - 375", tags=('green',))
greenData0 = dataTree.insert(greenData, 5, "green0", text="4lux     23 - 115", tags=('green',))

blueData4 = dataTree.insert(blueData, 1, "blue4", text="40000lux 1240 - 6200", tags=('blue',))
blueData3 = dataTree.insert(blueData, 2, "blue3", text="4000lux  220 - 1100 ", tags=('blue',))
blueData2 = dataTree.insert(blueData, 3, "blue2", text="400lux   60 - 300", tags=('blue',))
blueData1 = dataTree.insert(blueData, 4, "blue1", text="40lux    25 - 125", tags=('blue',))
blueData0 = dataTree.insert(blueData, 5, "blue0", text="4lux     7,5 - 37,5", tags=('blue',))

whiteData4 = dataTree.insert(whiteData, 1, "white4", text="40000lux 12400 - 62000", tags=('white',))
whiteData3 = dataTree.insert(whiteData, 2, "white3", text="4000lux  2200 - 11000", tags=('white',))
whiteData2 = dataTree.insert(whiteData, 3, "white2", text="400lux   600 - 3000", tags=('white',))
whiteData1 = dataTree.insert(whiteData, 4, "white1", text="40lux    250 - 1250", tags=('white',))
whiteData0 = dataTree.insert(whiteData, 5, "white0", text="4lux     75 - 375", tags=('white',))

yellowData4 = dataTree.insert(yellowData, 1, "yellow4", text="40000lux 7440 - 37200", tags=('yellow',))
yellowData3 = dataTree.insert(yellowData, 2, "yellow3", text="4000lux  1320 - 6600", tags=('yellow',))
yellowData2 = dataTree.insert(yellowData, 3, "yellow2", text="400lux   360 - 1800", tags=('yellow',))
yellowData1 = dataTree.insert(yellowData, 4, "yellow1", text="40lux    150 - 750", tags=('yellow',))
yellowData0 = dataTree.insert(yellowData, 5, "yellow0", text="4lux     45 - 225", tags=('yellow',))

greenC2Data4 = dataTree.insert(greenC2Data, 1, "greenC24", text="40000lux 3720 - 18600", tags=('greenC2',))
greenC2Data3 = dataTree.insert(greenC2Data, 2, "greenC23", text="4000lux  660 - 3300", tags=('greenC2',))
greenC2Data2 = dataTree.insert(greenC2Data, 3, "greenC22", text="4400lux  180 - 900", tags=('greenC2',))
greenC2Data1 = dataTree.insert(greenC2Data, 4, "greenC21", text="40lux    75 - 375", tags=('greenC2',))
greenC2Data0 = dataTree.insert(greenC2Data, 5, "greenC20", text="4lux     23 - 115", tags=('greenC2',))


dataTree.insert(redData4, "end", "", text="measure", tags=('red',),values=("","","","2A","2B"))
#redDataH0V0L4 = dataTree.insert(redData, "end", "redDataH0V0L4", text="40000lux", values=("","","","2A","2B"))



Grid.rowconfigure(master, 0, weight=1)
Grid.rowconfigure(master, 1, weight=1)
Grid.rowconfigure(master, 2, weight=1)
#Grid.rowconfigure(master, 2, weight=1)
#Grid.rowconfigure(master, 3, weight=1)
Grid.columnconfigure(master, 1, weight=1)
Grid.columnconfigure(master, 2, weight=1)
#Grid.columnconfigure(master, 0, weight=1)
#Grid.columnconfigure(master, 3, weight=1)


figAngle = beamPlot()
fig=EN12966_chromaticity_diagramplot()

canvas = FigureCanvasTkAgg(fig, master=master)
canvas2 = FigureCanvasTkAgg(figAngle, master=master)
#canvas3 = FigureCanvasTkAgg(fig, master=master)




canvas.get_tk_widget().grid(row=0,column=1,rowspan=3)
canvas2.get_tk_widget().grid(row=0,column=2,rowspan=1)
#canvas3.get_tk_widget().grid(row=1,column=1, columnspan=2)
groupMM039A.grid(row=0,column=0,rowspan=1,padx=5)
groupLuminanceMeter.grid(row=1,column=0,rowspan=1,padx=5)
dataTree.grid(row=1,column=2,rowspan=2)
#scanPorts.grid(row=0,column=0,rowspan=2)
#listPorts.grid(row=0,column=0, rowspan=2)




#etiqueta = Label(ventana,text="Etiqueta.")
#etiqueta.pack()
mainloop()
arduino = serial.Serial('COM10',57600)
arduino.write(b'HOLA')

arduino.close()

cs200.close_instrument(0)
"""
EJEMPLO PARA METER COORDENADAS DENTRO DE LA GRAFICA
import pylab

# Plotting the *CIE 1931 Chromaticity Diagram*.
# The argument *standalone=False* is passed so that the plot doesn't get displayed
# and can be used as a basis for other plots.
CIE_1931_chromaticity_diagram_plot(standalone=False)

# Plotting the *xy* chromaticity coordinates.
x, y = xy
pylab.plot(x, y, 'o-', color='white')

# Annotating the plot.
pylab.annotate(patch_spd.name.title(),
               xy=xy,
               xytext=(-50, 30),
               textcoords='offset points',
               arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=-0.2'))

# Displaying the plot.
display(standalone=True)
"""
