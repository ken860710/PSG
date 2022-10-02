import numpy as np
from pyedflib import highlevel
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.patches as patches
name = "K:/OSA patient with surgery/pre test/edf/20220121.edf"
name_event = "K:/OSA patient with surgery/pre test/osa_label/20220121.edf.XML"

# edf
#==============================================================================        
signals, signal_headers, header = highlevel.read_edf(name)        
dic = highlevel.read_edf_header(name)
channels = dic['channels']
print(channels)
#讀取並印出所有channels

npress = signals[11]  #讀取PSG中的NPress
therm = signals[12] #讀取PSG中的therm
chest = signals[13] #胸腔變化
abdo = signals[14] #腹腔變化
spo2 = signals[15] #血氧濃度變化


fsamp=25 # 資料點/每秒


sleep_lengh= len(npress) #設定資料總長
time=np.arange(0,(1/fsamp)*sleep_lengh,(1/fsamp)) #與資料點相匹配的時間軸

# label
#============================================================================== 
tree = ET.parse(name_event)
root = tree.getroot()  # 讀取xml檔

groups = ["Name","Start","Duration"] #收集 事件 發生時間 持續時間 
name = []
start = []
duration = []

# 子節點與屬性
for child in root:
    if child.tag == "ScoredEvents":
        for ch in child:
            Name = ch.find('Name').text            
            if Name == "Obstructive Hypopnea" or Name == "Obstructive Apnea": # Obstructive Apnea, Obstructive Hypopnea, Arousal (ARO SPONT), SpO2 desaturation
                Start = ch.find('Start').text
                Duration = ch.find('Duration').text
                name.append(Name)
                start.append(Start)
                duration.append(Duration)

dict = {
    groups[0]: name,
    groups[1]: start,
    groups[2]: duration
}
df_hy = pd.DataFrame(dict) #建立事件 發生時間 持續時間 列表
start = [float(item) for item in start]
duration = [float(item) for item in duration]


event_nu=len(df_hy)
ahi = event_nu/(sleep_lengh/25/60/60)
ahi=round(ahi,1)
ahi=str(ahi)

print("AHI = "+ahi)
# figure
#============================================================================== 


fig, ax = plt.subplots()
ax.plot(time/60,npress,'k',alpha=0.5)
# ax.plot(time/60,therm,'b',alpha=0.5)
# ax.plot(time/60,chest,'r',alpha=0.5)
ax.plot(time/60,abdo,'c',alpha=0.7)

for i in range(0,event_nu):    
    ax.add_patch(patches.Rectangle((start[i]/60, -0.5),duration[i]/60,1,
                                       facecolor = 'red',alpha=0.5,fill=True) )

