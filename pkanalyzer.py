# coding=GBK
# ����ע��
import sqlite3
import datetime


# ��ѯ����������ϳ��ֵ�
def makeMap(name_list,value_list):
    # ���ֵ�
    map_value = {}
    if (len(name_list) == len(value_list)):
        for index in range(0,len(name_list)):
            print(name_list[index],value_list[index])
            map_value[name_list[index]] = value_list[index]
    return map_value

# ��ѯ�����ؽ���ֵ�
def query_value(c,table_name):
    c.execute("SELECT *  from " + table_name + " where FID = 66")
    #��ȡ��ѯ��ֵ�б�fetchone ��ѯһ��,�����б�
    col_name_value_1 = c.fetchone() 
    #��ȡ��ѯ���ֶ��б�
    col_name_list_1  = [tuple[0] for tuple in c.description]
    map_value = makeMap(col_name_list_1,col_name_value_1)
    return map_value
    
# ��ѯ�����ؽ���ֵ��б�
def query_value_1(c,table_name):
    c.execute("SELECT *  from " + table_name + " where FParentID = 66")
    #��ȡ��ѯ��ֵ�б�fetchall ��ѯȫ���������б���б�
    col_name_value_1 = c.fetchall()
    #��ȡ��ѯ���ֶ��б�
    col_name_list_1  = [tuple[0] for tuple in c.description]
    #����ձ�����װ�ֵ�
    map_value = list() 
    for one_value in col_name_value_1:
        map_value.append(makeMap (col_name_list_1,one_value))
    return map_value

# �������ݿ�һ������
# table_name ����
# map_value �ֶΣ�ֵ
# ע���ַ���ֵ��Ҫ������������ҪתΪstr,ֵΪnone��������ֵΪ�ַ�����Ϊ�յ�����
def insert_value(c,table_name,map_value):
    insert_str = "INSERT INTO "+ table_name + " ("
    for key,value in map_value.items():
        if value == "NULL":
            insert_str += (key + ",")
        elif(type(value) == type("str") and  len(value) != 0 and value.isspace() != True ):
            insert_str += (key + ",")
        elif (value != None and type(value) != type("str")):
            insert_str += (key + ",")
    
    # ȥ�����һ��","����
    insert_str = insert_str[:-1]
    insert_str  += (") VALUES (")
    for key,value in map_value.items():
        if value == "NULL":
            insert_str += (value + ",")
        elif(type(value) == type("str") and  len(value) != 0 and value.isspace() != True ):
            insert_str += ("'" + value + "'" + ",")
        elif (value != None and type(value) != type("str")):
            insert_str += (str(value) + ",")
            
    insert_str = insert_str[:-1]
    insert_str  += (");")
    
    #print(insert_str)
    c.execute(insert_str)
    

#�������ݿ��������
def insert_values(c,table_name,map_values):
    for map_value in map_values:
        insert_value(c,table_name,map_value)


#��ѯ����FIDֵ
def query_id(c):
    c.execute("SELECT MAX(FID)   from T_CountResult")
    col_name_value_1 = c.fetchone()
    #print(col_name_value_1[0])

    return col_name_value_1[0]
    

#1-�������ݿ�     
conn = sqlite3.connect('PkAnalyzer_131.db')
c = conn.cursor()
print ("Opened database successfully")


#2-��ѯ���ݿ� 
map_CountResult     = query_value(  c,"T_CountResult"   )
map_PatientInfo     = query_value(  c,"T_PatientInfo"   )
list_InspectionInfo = query_value_1(c,"T_InspectionInfo")
list_GraphicsInfo   = query_value_1(c,"T_GraphicsInfo"  )

# print(map_CountResult)
# print(map_PatientInfo)
# print(list_InspectionInfo)
# print(list_InspectionInfo)
FSampleId = query_id(c);
today = datetime.datetime.now()
print(today.strftime("%Y-%m-%d %H:%M:%S"))

# �Ѳ�ѯ��������,�޸�ĳЩ���ݺ��ظ��������ݿ�
for index in range(1,10):
    offset = datetime.timedelta(minutes = index)
    timeStr = (today + offset).strftime("%Y/%m/%d %H:%M:%S")
    
    map_CountResult["FID"      ] = FSampleId + index;
    map_CountResult["FSampleId"] = "Test" + str(FSampleId + index).rjust(4,'0');
    map_CountResult["FTestTime"] = timeStr
    map_CountResult["FGUID"    ] = (today + offset).strftime("%Y%m%d_%H%M%S") + "_111"
    map_CountResult["FPatientInfoID"] = map_CountResult["FID"      ] 
    
    map_PatientInfo["FID"            ] = map_CountResult["FID"      ]
    map_PatientInfo["FSampleID"      ] = map_CountResult["FSampleId"]
    map_PatientInfo["FTestTime"      ] = timeStr
    map_PatientInfo["FGetSampleTime" ] = timeStr
    map_PatientInfo["FSendTime"      ] = timeStr
    map_PatientInfo["FCreateInfoTime"] = timeStr
    
    for map_value in list_InspectionInfo:
        map_value["FID"] = "NULL"
        map_value["FParentID"] = map_CountResult["FID"      ]
        map_value["FModifiedTime"] = timeStr
        
    for map_value in list_GraphicsInfo:
        map_value["FID"] = "NULL"
        map_value["FParentID"] = map_CountResult["FID"      ]
        
    insert_value(c,"T_CountResult",map_CountResult)    
    insert_value(c,"T_PatientInfo", map_PatientInfo)  
    insert_values(c,"T_InspectionInfo",list_InspectionInfo)  
    insert_values(c,"T_GraphicsInfo",list_GraphicsInfo) 
    conn.commit()   

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 
# T_CountResult 23 ������  FID PRIMARY KEY  
# ʱ����أ�FTestTime 2019/12/31 08:46:14
#          FGUID
# T_InspectionInfo FID  PRIMARY KEY FParentID = T_CountResult.FID
# T_GraphicsInfo FID  PRIMARY KEY FParentID = T_CountResult.FID
# T_PatientInfo FID  PRIMARY KEY = T_CountResult.FID  FSampleID =  T_CountResult.FSampleID 
#             FTestTime FGetSampleTime FSendTime FCreateInfoTime


print ("Operation done successfully")
conn.close()


