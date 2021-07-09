import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
import json, urllib
import math
from PIL import ImageTk, Image

# ******************************************* BLEList tab ***********************************

def BLElist_tab():
    BLElist_tab = Toplevel(app)
    BLElist_tab.geometry('1500x1200')
    BLElist_tab.title('BLElist')
    text = tk.Text(BLElist_tab)
    text.pack()
    
    # ************************************** Tags Names **************************************
    BLEsList=["BLE1", "BLE2", "BLE3"]
    
    #********************************************** Tables Definition ************************
    BLETreeview = ttk.Treeview(text, show="headings", columns=("1", "2", "3", "4", "5", "6"))
    BLETreeview.heading("#1", text="Name")
    BLETreeview.column("#1",minwidth=0,width=70)
    BLETreeview.heading("#2", text="MAC Address")
    BLETreeview.column("#2",minwidth=0,width=150)
    BLETreeview.heading("#3", text="RSSI")
    BLETreeview.column("#3",minwidth=0,width=70)
    BLETreeview.heading("#4", text="Distance")
    BLETreeview.column("#4",minwidth=0,width=80)
    BLETreeview.heading("#5", text="Temperature")
    BLETreeview.column("#5",minwidth=0,width=120)
    BLETreeview.heading("#6", text="Sensitivity")
    BLETreeview.column("#6",minwidth=0,width=100)
    BLETreeview.grid()
    
    # ******************************************* Scan Real Tags *********************
    
    from bluepy.btle import Scanner, DefaultDelegate

    class ScanDelegate(DefaultDelegate):
        def __init__(self):
            DefaultDelegate.__init__(self)

        def handleDiscovery(self, dev, isNewDev, isNewData):
            if isNewDev:
                print ("Discovered device", dev.addr)
            elif isNewData:
                print ("Received new data from", dev.addr)

    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(10.0)
    
    for dev in devices:
        # *********************************** A BLE Data Example *****************************
    #     dev={
    #         addr: "33-C9-5C-F4-87-73",
    #         rssi: "-65dB",
    #         data: {
    #             1: '\x08',
    #             22: 'j\xfe\x03\t\x02\x10\x00\x00?\xff\xff\xff\xff\x06\x01`\x1b\xd5`d\x03\x05\xff\x11',
    #             9: 'BLE1'
    #         }
    #    }
    
        #**************************************** Real Time Tag Readings ************************
        macAddress = dev.addr
        rssi = dev.rssi
        data = dev.scanData
        stringData = str(data)
        #***************************************** Initializations ***************************
        telemetryMode = False
        temperature = 0
        sensitivity = 0 
        movementNo = 0 
        lastMovement = 0
        clickNo = 0
        lastClick = 0
        #************************************** Distance calculations **************************
        txpower = -77
        n = 2
        delta = float(txpower-rssi)/(10*n)
        distance = round(math.pow(10, delta),2)
        # ************************************ Check Type of Tag **********************
        try:
            name = data[9]
            lastL = stringData.find(', 9:')
            truncData=stringData[17:lastL-1]
            print(name, truncData)
            telemetryMode=(int(truncData[7:9]) == 3)
        except Exception as e:
            name ='Unknown device'
        # *************************************** Assign Table parameters ***********************    
        if (name in BLEsList):
            if telemetryMode:
                temperature = int(truncData[-2])*16 + int(truncData[-1])
                startField = truncData[9:].find('x02')
                sensitivity = int(truncData[14+startField])*16 + int(truncData[15+startField])
            BLETreeview.insert("", "end", values=(name,macAddress,rssi,distance,temperature,sensitivity))
        text.config(state = tk.DISABLED)


# ******************************************* Assetlist tab ***********************************

def ASSETlist_tab():
    ASSETlist_tab = Toplevel(app)
    ASSETlist_tab.geometry('1500x1200')
    ASSETlist_tab.title('ASSETlist')
    text = tk.Text(ASSETlist_tab)
    text.pack()
    
    # ************************************** Tags Names **************************************
    AssetsList=["Asset1", "Asset2", "Asset3"]
    
    #********************************************** Tables Definition ************************
    AssetTreeview = ttk.Treeview(text, show="headings", columns=("1","2","3","4","5","6","7","8","9"))
    AssetTreeview.heading("#1", text="Name")
    AssetTreeview.column("#1",minwidth=0,width=70)
    AssetTreeview.heading("#2", text="MAC Address")
    AssetTreeview.column("#2",minwidth=0,width=150)
    AssetTreeview.heading("#3", text="RSSI")
    AssetTreeview.column("#3",minwidth=0,width=70)
    AssetTreeview.heading("#4", text="Distance")
    AssetTreeview.column("#4",minwidth=0,width=80)
    AssetTreeview.heading("#5", text="Temperature")
    AssetTreeview.column("#5",minwidth=0,width=120)
    AssetTreeview.heading("#6", text="Sensitivity")
    AssetTreeview.column("#6",minwidth=0,width=100)
    AssetTreeview.heading("#7", text="Click No")
    AssetTreeview.column("#7",minwidth=0,width=100)
    AssetTreeview.heading("#8", text="Last Click")
    AssetTreeview.column("#8",minwidth=0,width=100)
    AssetTreeview.heading("#9", text="Move No")
    AssetTreeview.column("#9",minwidth=0,width=100)
    AssetTreeview.grid()

    # ******************************************* Scan Real Tags *********************
    from bluepy.btle import Scanner, DefaultDelegate

    class ScanDelegate(DefaultDelegate):
        def __init__(self):
            DefaultDelegate.__init__(self)

        def handleDiscovery(self, dev, isNewDev, isNewData):
            if isNewDev:
                print ("Discovered device", dev.addr)
            elif isNewData:
                print ("Received new data from", dev.addr)

    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(10.0)

    # ****************************************** Analysing All BLE Devices *********************
    for dev in devices:
       
    # ******************************** An Asset Data Example *****************************
    #     dev={
    #         addr  : "33-C9-5C-F4-87-75",
    #         rssi: "-65dB",
    #         data: {
    #             1: '\x06',
    #             22: 'j\xfe\x03\x05\x06\x10\xfe\xff<\x04\x11\x00\xff\xff\x04\x16\x02\xff\xff\x03\x13P\x15
    #             9: 'Asset1'
    #         }
    #    }
    #
        #**************************************** Real Time Tag Readings ************************
        macAddress = dev.addr
        rssi = dev.rssi
        data = dev.scanData
        stringData = str(data)
        #***************************************** Initializations ***************************
        telemetryMode = False
        temperature = 0
        sensitivity = 0 
        movementNo = 0 
        lastMovement = 0
        clickNo = 0
        lastClick = 0
        #************************************** Distance calculations **************************
        txpower = -77
        n = 2
        delta = float(txpower-rssi)/(10*n)
        distance = round(math.pow(10, delta),2)
        # ************************************ Check Type of Tag **********************
        try:
            name = data[9]
            lastL = stringData.find(', 9:')
            truncData=stringData[17:lastL-1]
            print(name, truncData)
            telemetryMode=(int(truncData[7:9]) == 3)
        except Exception as e:
            name ='Unknown device'
        # *************************************** Assign Table parameters ***********************    
        if (name in AssetsList):
            if telemetryMode:
                temperature = int(truncData[-2])*16 + int(truncData[-1])
                startField = truncData[9:].find('x05\\x06')
                sensitivity = int(truncData[18+startField])*16 + int(truncData[19+startField])
                startField = truncData[32:].find('x11')
                clickNo = int(truncData[37+startField])*16 + int(truncData[38+startField])
                if (truncData[41+startField:43+startField] == 'ff') & (truncData[45+startField:47+startField] == 'ff'):
                    print('button not clicked yet')           
                    lastClick = 0
                else:
                    lastClick = int(truncData[42+startField]) + int(truncData[41+startField])*16 + int(truncData[46+startField])*256 + int(truncData[45+startField])*4096
                startField = truncData[47:].find('x04\\x16')
                movementNo = int(truncData[56+startField])*16 + int(truncData[57+startField])
            AssetTreeview.insert("", "end", values=(name,macAddress,rssi,distance,temperature,sensitivity,clickNo,lastClick,movementNo))
        text.config(state = tk.DISABLED)

# ******************************************* Visitorlist tab ***********************************
        
def VISITORlist_tab():
    VISITORlist_tab = Toplevel(app)
    VISITORlist_tab.geometry('1500x1200')
    VISITORlist_tab.title('VISITORlist')
    text = tk.Text(VISITORlist_tab)
    text.pack()
    
    #********************************************** Tables Definition ************************
    
    VisitorTreeview = ttk.Treeview(text, show="headings", columns=("1", "2", "3", "4"))
    VisitorTreeview.heading("#1", text="Name")
    VisitorTreeview.column("#1",minwidth=0,width=70)
    VisitorTreeview.heading("#2", text="MAC Address")
    VisitorTreeview.column("#2",minwidth=0,width=150)
    VisitorTreeview.heading("#3", text="RSSI")
    VisitorTreeview.column("#3",minwidth=0,width=70)
    VisitorTreeview.heading("#4", text="Distance")
    VisitorTreeview.column("#4",minwidth=0,width=80)
    VisitorTreeview.grid()
    # ******************************************* Scan Real Tags *********************
    from bluepy.btle import Scanner, DefaultDelegate

    class ScanDelegate(DefaultDelegate):
        def __init__(self):
            DefaultDelegate.__init__(self)

        def handleDiscovery(self, dev, isNewDev, isNewData):
            if isNewDev:
                print ("Discovered device", dev.addr)
            elif isNewData:
                print ("Received new data from", dev.addr)

    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(10.0)
    
    # ****************************************** Analysing All BLE Devices *********************
    for dev in devices:
        
    # *********************************** An Unkonwn Device Data Example *****************************
    #     dev={
    #         addr  : "D2-C9-5C-F4-87-75",
    #         rssi: "-78dB",
    #         data: {
    #             1: '\x06',
    #             255: 'L\x00\x02\x15\xf7\x82m\xa6O\xa2N\x98\x80$\xbc[q\xe0\x89>\xf6}\xdc_\xb3'
    #         }
    #    }
        #**************************************** Real Time Tag Readings ************************
        macAddress = dev.addr
        rssi = dev.rssi
        data = dev.scanData
        stringData = str(data)
        #***************************************** Initializations ***************************
        telemetryMode = False
        temperature = 0
        sensitivity = 0 
        movementNo = 0 
        lastMovement = 0
        clickNo = 0
        lastClick = 0
        #************************************** Distance calculations **************************
        txpower = -77
        n = 2
        delta = float(txpower-rssi)/(10*n)
        distance = round(math.pow(10, delta),2)
        # ************************************ Check Type of Tag **********************
        try:
            name = data[9]
            lastL = stringData.find(', 9:')
            truncData=stringData[17:lastL-1]
            print(name, truncData)
            telemetryMode=(int(truncData[7:9]) == 3)
        except Exception as e:
            name ='Unknown device'
        # *************************************** Assign Table parameters ***********************    
        
        VisitorTreeview.insert("", "end", values=(name, macAddress, rssi, distance))
        
        # ***************************************************************************************        
        text.config(state = tk.DISABLED)

# **************************************** GUI Configuration ****************************
app = tk.Tk()
#img2 = Image.open("Circuit.jpeg")
#resized2 = img2.resize((300,94), Image.ANTIALIAS)
#new_pic2 = ImageTk.PhotoImage(resized2)
#img_label2 = Label(app, image=new_pic2, borderwidth=0, highlightthickness=0, padx=0, pady=0)
#img_label2.pack(pady=2,side=LEFT, padx=10)

img = Image.open("logomerged.png")
resized = img.resize((650,250), Image.ANTIALIAS)
new_pic = ImageTk.PhotoImage(resized)
img_label = Label(app, image=new_pic, borderwidth=0, highlightthickness=0, padx=0, pady=0)
#img_label.grid(row=0, column=0, padx=50, pady=50)
img_label.pack(pady=2,side=TOP, padx=10)
# app.iconbitmap('bluetooth_icon.ico')
p1 = PhotoImage(file = 'bluetooth_icon.png') # Setting icon of master window
app.iconphoto(False, p1)


# **************************************** BLElist button ****************************
btn = Button(app, text="BLE List",command=BLElist_tab, bg="#f0f0f0", fg="#08245c", font=("Century Gothic",20), borderwidth=0)
# **************************************** Assetlist button ****************************
btn1 = Button(app, text="Asset List",command=ASSETlist_tab, bg="#f0f0f0", fg="#08245c", font=("Century Gothic",20), borderwidth=0)
# **************************************** Visitorlist button ****************************
btn2 = Button(app, text="Visitor List",command=VISITORlist_tab, bg="#f0f0f0", fg="#08245c", font=("Century Gothic",20), borderwidth=0)
btn.place(anchor = CENTER, relx = 0.3, rely = 0.5)
btn1.place(anchor = CENTER, relx = 0.5, rely = 0.5)
btn2.place(anchor = CENTER, relx = 0.7, rely = 0.5)
app.title('Indoor navigation')
app.geometry('1500x1200')
app['bg']='#fff'
app.mainloop()