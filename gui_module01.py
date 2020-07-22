import tkinter as tk
from tkinter import ttk 
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from pymongo import MongoClient
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import folium
from folium import plugins

class UserInterface:
    def __init__(self):
        self.client = MongoClient() #OR client = MongoClient('mongodb://localhost:27017')

    def insert_documents_to_db(self):
        db = self.client.pymongo_test    #OR db = self.client['pymongo_test'] //test DB
        #Drop collections to avoid repeating documents/entries when re-run
        db.traffic_v16.drop()
        db.traffic_v17.drop()
        db.traffic_v18.drop()
        db.traffic_i16.drop()
        db.traffic_i17.drop()
        db.traffic_i18.drop()
        
        #Traffic Volumes-collections
        traffic_v16 = db.traffic_v16                 #traffic_v16 collection
        df_traffic_v16 = pd.read_csv("TrafficFlow2016_OpenData.csv")
        traffic_v16.insert_many(df_traffic_v16.to_dict('records')) 

        traffic_v17 = db.traffic_v17                 #traffic_v17 collection
        df_traffic_v17 = pd.read_csv("2017_Traffic_Volume_Flow.csv")
        traffic_v17.insert_many(df_traffic_v17.to_dict('records'))
        #print some entries/documents
        cursor = traffic_v17.find()
        print(cursor.count()) 
        for i in range(1):
            print(cursor[i])

        traffic_v18 = db.traffic_v18                 #traffic_v18 collection
        df_traffic_v18 = pd.read_csv("Traffic_Volumes_for_2018.csv")
        traffic_v18.insert_many(df_traffic_v18.to_dict('records'))  
        
        #Traffic Incidents-Collections
        traffic_i16 = db.traffic_i16                 #traffic_i16 collection
        df_traffic_i16 = pd.read_csv("Traffic_Incidents_Archive_2016.csv")
        traffic_i16.insert_many(df_traffic_i16.to_dict('records'))

        traffic_i17 = db.traffic_i17                 #traffic_i17 collection
        df_traffic_i17 = pd.read_csv("Traffic_Incidents_Archive_2017.csv")
        traffic_i17.insert_many(df_traffic_i17.to_dict('records'))  

        traffic_i18 = db.traffic_i18                 #traffic_i18 collection
        df_traffic_iall = pd.read_csv("Traffic_Incidents.csv")
        filt_18 = df_traffic_iall.START_DT.str.contains(pat = '2018')
        df_traffic_i18 = df_traffic_iall[filt_18]
        print(df_traffic_i18['START_DT'].head(10))  # print head to confirm if all are 2018
        traffic_i18.insert_many(df_traffic_i18.to_dict('records'))  
        #print some entries/documents
        cursor = traffic_i18.find() 
        #print(cursor.count())
        #for i in range(2):
            #print(cursor[i]) 
        
      
    def analyze_and_plot(self):# chart is ok
        for widget in  self.lbl_frame.winfo_children():
            widget.destroy()
        db = "pymongo_test"
        if self.n1.get()=='Traffic flow':
            df_traffic_v16 = self.read_mongo(db, "traffic_v16")
            volume16 = df_traffic_v16['volume']
            max_volume16 = volume16.max()

            df_traffic_v17 = self.read_mongo(db, "traffic_v17")
            volume17 = df_traffic_v17['volume']
            max_volume17 = volume17.max()

            df_traffic_v18 = self.read_mongo(db, "traffic_v18")
            volume18 = df_traffic_v18['volume']
            max_volume18 = volume18.max()
            x=[2016, 2017, 2018]
            y=[max_volume16, max_volume17, max_volume18]

    
    def show_map(self):#working ok
        #added scale controll
        map1 =folium.Map(location=(51.049999, -114.066666), zoom_start=10, width=500, height=600,controll_scale=True)
        # largest number is the call from the argument
        #folium.Marker(location=[largest number ], popup=" this is the largest point", icon=folium.Icon(color='red', icon='info-sign')).add_to(map_of_calgary)
        map1.save(outfile='map_of_calgary.html')
        myLablel1=tk.Label(self.fr_buttons,text="map file created")
        myLablel1.grid(row=10,column=0) 

    # set connection with mongodb
    def _connect_mongo(self, host, port, username, password, db):
        """ A util for making a connection to mongo """
        if username and password:
            mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
            conn = MongoClient(mongo_uri)
        else:
            conn = MongoClient(host, port)

        return conn[db]

    # read mongodb collection and move to pandas dataframe
    def read_mongo(self, db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
        """ Read from Mongo and Store into DataFrame """
        # Connect to MongoDB
        db = self._connect_mongo(host=host, port=port, username=username, password=password, db=db)
        cursor = db[collection].find(query)

        df =  pd.DataFrame(list(cursor))

        # Delete the _id
        if no_id:
            del df['_id']

        return df

    def read_and_print(self):
        for widget in  self.lbl_frame.winfo_children():
            widget.destroy()
        lbl_message = tk.Label(self.fr_buttons)
        lbl_message.configure(text= "Type selected:"+self.n1.get()+"\n Year Selected: "+self.n2.get())
        lbl_message.grid(row=9,column=0,sticky="ew",padx=5,pady=20)

        db = "pymongo_test"
        #Adapt for 2016 volume conditions from GUI
        if ((self.n1.get()=='Traffic flow')and(self.n2.get()=='2016')):      
            df = self.read_mongo(db, "traffic_v16")
            print("\n\n", df.head(5))
            
            records = df.to_records(index=False)
            result_to_print = list(records)   #Returns a list of tuples
            textc= tk.Text(self.lbl_frame,width=130)
            #textc.insert(tk.INSERT,str(df.head(1)))
            for i in range(4):
                Tree= ttk.Treeview(self.fr_buttons, height=10,show="headings")
                Tree["columns"]=("secname","the_geom","year_vol","shape_leng","volume")
                #Tree.grid(row=1,column=2)

                '''textc.insert(tk.INSERT,str(result_to_print[i]))
                textc.insert(tk.INSERT,"\n")
            textc.grid(row=1,column=2)''' 
               
        
            #TO DO// print to right frame\\check and done
            #Adapt for 2017 volume selection from GUI
        if ((self.n1.get()=='Traffic flow')and(self.n2.get()=='2017')):
            df = self.read_mongo(db, "traffic_v17")
            records = df.to_records(index=False)
            result_to_print = list(records)
            myLabel1=tk.Label(self.lbl_frame,text=df.head(5))
            myLabel1.config(width=85)
            myLabel1.grid(row=1,column=2)
            #print('\n',result_to_print[i])
            #TO DO// print to right frame

        #Adapt for 2018 volume selection from GUI
        if ((self.n1.get()=='Traffic flow')and(self.n2.get()=='2018')):
            df = self.read_mongo(db, "traffic_v18")
            records = df.to_records(index=False)
            result_to_print = list(records)
            myLabel1=tk.Label(self.lbl_frame,text=df.head(5))
            myLabel1.config(width=85)
            myLabel1.grid(row=1,column=2)
            #print('\n',result_to_print[i])
            #TO DO// print to right frame            


        #Adapt for 2016 incidents selection from GUI
        if ((self.n1.get()=='Trafic Accidents')and(self.n2.get()=='2016')):
            df = self.read_mongo(db, "traffic_i16")
            # df = df.assign(freq=df.groupby('INCIDENT INFO')['INCIDENT INFO'].transform('count'))\
            #     .sort_values(by=['freq','INCIDENT INFO'],ascending=[False,True])
            print(df.columns)
            if sort_it:
                df = df.assign(freq=df.groupby('INCIDENT INFO')['INCIDENT INFO'].transform('count'))\
                    .sort_values(by=['freq','INCIDENT INFO'],ascending=[False,True])
            print(df.head(5))
            print(df.columns)
            print("yes", df.iloc[0]['location'])   
            records = df.to_records(index=False)
            result_to_print = list(records)
            myLabel1=tk.Label(self.lbl_frame,text=df.head(5))
            myLabel1.config(width=85)
            myLabel1.grid(row=1,column=2)

        #Adapt for 2017 incidents selection from GUI
        if ((self.n1.get()=='Trafic Accidents')and(self.n2.get()=='2017')):
            df = self.read_mongo(db, "traffic_i17")
            records = df.to_records(index=False)
            result_to_print = list(records)
            myLabel1=tk.Label(self.lbl_frame,text=df.head(5))
            myLabel1.config(width=85)
            myLabel1.grid(row=1,column=2)
            #print('\n',result_to_print[i])
            #TO DO// print to right frame

        #Adapt for 2018 incident selection from GUI
        if ((self.n1.get()=='Trafic Accidents')and(self.n2.get()=='2018')):
            df = self.read_mongo(db, "traffic_i18")
            records = df.to_records(index=False)
            result_to_print = list(records)
            myLabel1=tk.Label(self.lbl_frame,text=df.head(5))
            myLabel1.config(width=85)
            myLabel1.grid(row=1,column=2)
            #print('\n',result_to_print[i])
            #TO DO// print to right frame    
       
                

        
    def design_gui(self):
        window = tk.Tk()

        window.title("Data Analyzer")

        window.geometry("1200x750")

        self.lbl_frame = tk.LabelFrame(window)#right frame
        self.fr_buttons = tk.Frame(window)#left frame

        #Two ComboBoxes to select type of data and year to analyze respectively
        self.n1 = tk.StringVar()
        self.n2 = tk.StringVar()
        labelT=ttk.Label(self.fr_buttons,text="Select a Type")
        combo_type = ttk.Combobox(self.fr_buttons, textvariable = self.n1)
        combo_type['values'] = ('Traffic flow', 'Trafic Accidents')
        labelY=ttk.Label(self.fr_buttons,text="Select a Year")    
        combo_year = ttk.Combobox(self.fr_buttons, textvariable = self.n2)
        combo_year['values'] = ('2016', '2017', '2018')
              
       
        #Buttons to perform actions on selected data type's year
        btn_read = tk.Button(self.fr_buttons, text="Read", command=self.read_and_print)
        btn_sort = tk.Button(self.fr_buttons, text="Sort")
        btn_analysis = tk.Button(self.fr_buttons, text="Analysis", command=self.analyze_and_plot)
        btn_map = tk.Button(self.fr_buttons, text="Map", command=self.show_map)
        
       
        #StatusBar
        lbl_status = tk.Label(self.fr_buttons,text="Status:")
        
        

        #Set left frame widgets positions and padding
        labelT.grid(row=0,column=0,sticky="ew",padx=5,pady=10)
        combo_type.grid(row=1, column=0, sticky="ew")
        labelY.grid(row=2,column=0,sticky="ew",padx=5,pady=10)
        combo_year.grid(row=3, column=0, sticky="ew")
        btn_read.grid(row=4, column=0, sticky="ew", padx=5, pady=20)
        btn_sort.grid(row=5, column=0, sticky="ew", padx=5, pady=20)
        btn_analysis.grid(row=6, column=0, sticky="ew", padx=5, pady=20)
        btn_map.grid(row=7, column=0, sticky="ew", padx=5, pady=20)
        lbl_status.grid(row=8, column=0, sticky="ew", padx=5, pady=20)#text plot ready, remaining all other messages

        
        

        self.fr_buttons.grid(row=0, column=0, sticky="ns", padx=5)
        self.lbl_frame.grid(row=0, column=1,sticky="ns",padx=5)
        
        