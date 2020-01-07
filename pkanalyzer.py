# coding=GBK
# 中文注释
import sqlite3
import datetime


# 查询的两个表，组合成字典
def makeMap(name_list,value_list):
    # 空字典
    map_value = {}
    if (len(name_list) == len(value_list)):
        for index in range(0,len(name_list)):
            print(name_list[index],value_list[index])
            map_value[name_list[index]] = value_list[index]
    return map_value

# 查询表，返回结果字典
def query_value(c,table_name):
    c.execute("SELECT *  from " + table_name + " where FID = 66")
    #获取查询的值列表fetchone 查询一条,返回列表
    col_name_value_1 = c.fetchone() 
    #获取查询的字段列表
    col_name_list_1  = [tuple[0] for tuple in c.description]
    map_value = makeMap(col_name_list_1,col_name_value_1)
    return map_value
    
# 查询表，返回结果字典列表
def query_value_1(c,table_name):
    c.execute("SELECT *  from " + table_name + " where FParentID = 66")
    #获取查询的值列表fetchall 查询全部，返回列表的列表
    col_name_value_1 = c.fetchall()
    #获取查询的字段列表
    col_name_list_1  = [tuple[0] for tuple in c.description]
    #申请空表，表里装字典
    map_value = list() 
    for one_value in col_name_value_1:
        map_value.append(makeMap (col_name_list_1,one_value))
    return map_value

# 插入数据库一条数据
# table_name 表名
# map_value 字段：值
# 注：字符串值需要‘’，数字需要转为str,值为none的抛弃，值为字符串且为空的抛弃
def insert_value(c,table_name,map_value):
    insert_str = "INSERT INTO "+ table_name + " ("
    for key,value in map_value.items():
        if value == "NULL":
            insert_str += (key + ",")
        elif(type(value) == type("str") and  len(value) != 0 and value.isspace() != True ):
            insert_str += (key + ",")
        elif (value != None and type(value) != type("str")):
            insert_str += (key + ",")
    
    # 去除最后一个","逗号
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
    

#插入数据库多条数据
def insert_values(c,table_name,map_values):
    for map_value in map_values:
        insert_value(c,table_name,map_value)


#查询最大的FID值
def query_id(c):
    c.execute("SELECT MAX(FID)   from T_CountResult")
    col_name_value_1 = c.fetchone()
    #print(col_name_value_1[0])

    return col_name_value_1[0]
    

#1-连接数据库     
conn = sqlite3.connect('PkAnalyzer_131.db')
c = conn.cursor()
print ("Opened database successfully")


#2-查询数据库 
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

# 把查询到的数据,修改某些数据后，重复插入数据库
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
# T_CountResult 23 个参数  FID PRIMARY KEY  
# 时间相关：FTestTime 2019/12/31 08:46:14
#          FGUID
# T_InspectionInfo FID  PRIMARY KEY FParentID = T_CountResult.FID
# T_GraphicsInfo FID  PRIMARY KEY FParentID = T_CountResult.FID
# T_PatientInfo FID  PRIMARY KEY = T_CountResult.FID  FSampleID =  T_CountResult.FSampleID 
#             FTestTime FGetSampleTime FSendTime FCreateInfoTime


print ("Operation done successfully")
conn.close()


