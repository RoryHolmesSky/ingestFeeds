import requests
import json
import os

#fill these in with the correct values
my_username = 'dummy-da-account'
my_password = 'dummy-da-account'
instance = "onedata-dev"


columnId = "00000000-0000-0000-0000-000000031008"
tableId = "00000000-0000-0000-0000-000000031007"
schemaId = "00000000-0000-0000-0001-000400000002"
systemId = "00000000-0000-0000-0000-000000031302"
multipleValueId = "660bd800-0ba7-485b-8fcb-4e54a4dd5b49"
mappingId = "110ffa26-b351-4884-a398-9ebf96f52d2c"
domainId = "d81c7ff6-52e2-4c97-ae4a-4fc7fdcaf507"


def run_git():
    os.system("git init")
    os.system("git pull https://github.com/sky-uk/gottdata-io-config.git")


def create_system(path, username, password):
    name = path
    url = f'https://sky-{instance}.collibra.com/rest/2.0/assets'
    print (url)
    inputs = {"name" : name,
              "domainId" : domainId,
              "typeId" : systemId}
    http_response = requests.post(url, json = inputs, auth = (username, password))
    if http_response.status_code == 201:
        SorF = " success"
    else:
        SorF = "Failed"
    #print ("creating system -" + SorF)
    return name

def get_system_id(data, username, password):
    url = f'https://sky-{instance}.collibra.com/rest/2.0/assets'
    input_params = {"name": create_system(data, username=my_username, password=my_password),
                    "domainId" : domainId,
                    "nameMatchMode" : "EXACT"}
    http_response = requests.get(url, params = input_params, auth = (my_username, my_password))
    results = json.loads(http_response.text)['results']
    return results[0]['id']

def get_asset_id(assetName, mode):
    url = f'https://sky-{instance}.collibra.com/rest/2.0/assets'
    input_params = {"name": assetName,
                    "domainId" : domainId,
                    "nameMatchMode" : mode}
    http_response = requests.get(url, params = input_params, auth = (my_username, my_password))
    results = json.loads(http_response.text)['results']
    return results[0]['id']

def get_asset_id_from_tag(assetName, mode, tag):
    url = f'https://sky-{instance}.collibra.com/rest/2.0/assets'
    input_params = {"name": assetName,
                    "tagNames" : [tag],
                    "domainId" : domainId,
                    "nameMatchMode" : mode}
    http_response = requests.get(url, params = input_params, auth = (my_username, my_password))
    results = json.loads(http_response.text)['results']
    return results[0]['id']


def add_table(data, username, password):
    name = data["name"]
    url = f'https://sky-{instance}.collibra.com/rest/2.0/assets'
    inputs = {"typeId": tableId,
            "name" : name,
            "domainId" : domainId}
    http_response = requests.post(url, json = inputs, auth = (username, password))
    if http_response.status_code == 201:
        SorF = " success"
    else:
        SorF = "Failed"
    print ("uploading table -" + SorF)
    return name

def add_column(data, domainID, tableName, username, password):
    print (f"column is {data}")
    print (tableName)
    name = data["name"]
    if name != tableName:
        if "_" in tableName:
            if name == tableName[tableName.rindex('_')+1:]:
                full_name = tableName
            else:
                full_name = tableName + "_" + name
        else:
                full_name = tableName + "_" + name
        print (full_name)
        url = f'https://sky-{instance}.collibra.com/rest/2.0/assets'
        inputs = {"typeId": columnId,
                "name" : full_name,
                "domainId" : domainID,
                "displayName" : name}
        http_response = requests.post(url, json = inputs, auth = (username, password))
        if http_response.status_code == 201:
            SorF = " success"
        else:
            SorF = "Failed"
            print (http_response)
        print ("uploading column -" + SorF)
        return full_name

def add_data_source(columnId, value):
    url = f'https://sky-{instance}.collibra.com/rest/2.0/assets/' + columnId + '/tags'
    input_params = {
                    "tagNames": [
                    value
                    ]
                    }
    http_response = requests.post(url, json = input_params, auth = (my_username, my_password))
    if http_response.status_code == 201:
        SorF = " success"
    else:
        SorF = "Failed"
    #print ("uploading data type -" + SorF)

def add_data_type(columnId, value):
    if type(value) == list:
        value = value[1]
    url = f'https://sky-{instance}.collibra.com/rest/2.0/attributes'
    input_params = {"typeId" : "00000000-0000-0000-0000-000000000219",
                    "value" : value.upper(),
                    "assetId" : columnId}
    http_response = requests.post(url, json = input_params, auth = (my_username, my_password))
    if http_response.status_code == 201:
        SorF = " success"
    else:
        SorF = "Failed"
    print ("uploading data type -" + SorF)

def add_default(columnId, default):
    if type(default) == list:
        default = default[0]
    url = f'https://sky-{instance}.collibra.com/rest/2.0/attributes'
    input_params = {"typeId" : "00000000-0000-0000-0001-000500000014",
                    "value" : default,
                    "assetId" : columnId}
    http_response = requests.post(url, json = input_params, auth = (my_username, my_password))
    if http_response.status_code == 201:
        SorF = " success"
    else:
        SorF = "Failed"
    #print ("uploading default -" + SorF)

def add_multi_value(columnId):
        url = f'https://sky-{instance}.collibra.com/rest/2.0/attributes'
        input_params = {"typeId" : "660bd800-0ba7-485b-8fcb-4e54a4dd5b49",
                        "value" : True,
                        "assetId" : columnId}
        http_response = requests.post(url, json = input_params, auth = (my_username, my_password))
        if http_response.status_code == 201:
            SorF = " success"
        else:
            SorF = "Failed"
        #print ("uploading multi -" + SorF)

def add_enum(columnId, symbols):
        for val in symbols:
            url = f'https://sky-{instance}.collibra.com/rest/2.0/attributes'
            input_params = {"typeId" : "9a66dbf4-c31d-4d42-a38e-362c6fe19094",
                            "value" : val,
                            "assetId" : columnId}
            http_response = requests.post(url, json = input_params, auth = (my_username, my_password))
            if http_response.status_code == 201:
                SorF = " success"
            else:
                SorF = "Failed"
            #print ("uploading enum -" + SorF)

def relate_column_to_table(tableId, columnId):
    url = f'https://sky-{instance}.collibra.com/rest/2.0/relations'
    input_params = {"typeId" : "00000000-0000-0000-0000-000000007042",
                    "sourceId" : columnId,
                    "targetId" : tableId}
    http_response = requests.post(url, json = input_params, auth = (my_username, my_password))
    if http_response.status_code == 201:
        SorF = " success"
    else:
        SorF = "Failed"
    #print ("relating columns to tables -" + SorF)

def relate_table_to_system(systemID, tableID):
    url = f'https://sky-{instance}.collibra.com/rest/2.0/relations'
    input_params = {"typeId" : "379399c4-fca8-4c3f-95c5-5f9c4b389872",
                    "sourceId" : systemID,
                    "targetId" : tableID}
    http_response = requests.post(url, json = input_params, auth = (my_username, my_password))
    if http_response.status_code == 201:
        SorF = " success"
    else:
        SorF = "Failed"
    print ("relating tables to system -" + SorF)

def relate_system_to_layer(systemId):
    url = f'https://sky-{instance}.collibra.com/rest/2.0/relations'
    input_params = {"typeId" : "13a31e47-b77c-41f2-a416-d386b9e81c44",
                    "sourceId" : "40b28a42-0fbb-4e32-80f6-7eecff1d8d7d",
                    "targetId" : systemId}
    http_response = requests.post(url, json = input_params, auth = (my_username, my_password))
    if http_response.status_code == 201:
        SorF = " success"
    else:
        SorF = "Failed"
    #print ("relating system to layer -" + SorF)



def get_columns(data, tableName, tableId, k):
    next_layer = []
    for each in data['fields']:
        print (each)
        if type(each['type']) == dict:
            if each['type']['type'] == "enum":
                columnName = add_column(each, domainId, tableName, username=my_username, password=my_password)
                columnId = get_asset_id(columnName, "EXACT")
                add_data_source(columnId, k)
                add_enum(columnId, each['type']['symbols'])
                relate_column_to_table(tableId, columnId)
            elif each['type']['type'] == "record":
                next_layer.append(each['type'])
            elif each['type']['type'] == "map":
                next_layer.append(each['type']['values'])
            elif "logicalType" in each['type']:
                columnName = add_column(each, domainId, tableName, username=my_username, password=my_password)
                columnId = get_asset_id(columnName, "EXACT")
                add_data_type(columnId, each["type"]["type"])
                add_data_source(columnId, k)
                relate_column_to_table(tableId, columnId)
            elif type(each['type']['items']) == str:
                columnName = add_column(each, domainId, tableName, username=my_username, password=my_password)
                columnId = get_asset_id(columnName, "EXACT")
                add_data_source(columnId, k)
                add_data_type(columnId, each["type"]['items'])
                relate_column_to_table(tableId, columnId)
            elif type(each['type']['items']) == list:
                columnName = add_column(each, domainId, tableName, username=my_username, password=my_password)
                columnId = get_asset_id(columnName, "EXACT")
                add_data_source(columnId, k)
                add_data_type(columnId, each["type"]['items'])
                add_default(columnId, each["type"][0])
                relate_column_to_table(tableId, columnId)
            elif each['type']['type'] == "array":
                next_layer.append(each['type']['items'])
        elif type(each['type']) == list:
                if len(each['type']) == 1:
                    next_layer.append(each['type'][0])
                elif type(each['type'][1]) == str:
                    columnName = add_column(each, domainId, tableName, username=my_username, password=my_password)
                    columnId = get_asset_id(columnName, "EXACT")
                    add_data_source(columnId, k)
                    add_data_type(columnId, each["type"])
                    add_default(columnId, each["type"][0])
                    relate_column_to_table(tableId, columnId)
                elif type(each['type'][1]) == dict:
                    if each['type'][1]['type'] == "record":
                        next_layer.append(each['type'][1])
                    elif type(each['type'][1]['items']) == str:
                        columnName = add_column(each, domainId, tableName, username=my_username, password=my_password)
                        columnId = get_asset_id(columnName, "EXACT")
                        add_data_source(columnId, k)
                        add_data_type(columnId, each["type"][1]['items'])
                        add_default(columnId, each["type"][0])
                        add_multi_value(columnId)
                        relate_column_to_table(tableId, columnId)
                    elif type(each['type'][1]['items']) == dict:
                        next_layer.append(each['type'][1]['items'])
        elif (type(each['type']) == str):
            columnName = add_column(each, domainId, tableName, username=my_username, password=my_password)
            columnId = get_asset_id(columnName, "EXACT")
            add_data_source(columnId, k)
            add_data_type(columnId, each["type"])
            relate_column_to_table(tableId, columnId)
    #print ("number of tables in next layer: " + str(len(next_layer)))
    return next_layer

def upload_schema(data, domainId, tableId, tableName, k):
    base_name = tableName
    print (f"base name is {base_name}")
    next_layer_down = get_columns(data, tableName, tableId, k)
    for table in next_layer_down:
        print (table)
        if "_" in table['name']:
            tableName = tableName + "_" + table['name'][table['name'].rindex('_')+1:]
        else:
            tableName = tableName + "_" + table['name']
        columnName = add_column(table, domainId, tableName, username=my_username, password=my_password)
        columnId = get_asset_id(columnName, "EXACT")
        add_data_source(columnId, k)
        relate_column_to_table(tableId, columnId)
        print (f"table name is now {tableName}")
        upload_schema(table, domainId, tableId, tableName, k)
        tableName = base_name
        columnName = add_column(data, domainId, tableName, username=my_username, password=my_password)
        columnId = get_asset_id(columnName, "EXACT")
        #add_data_source(columnId, k)
        relate_column_to_table(tableId, columnId)

def run_program(data, commId, k):
    tableName = add_table(data, username=my_username, password=my_password)
    print (tableName)
    tableId = get_asset_id(tableName, "EXACT")
    relate_table_to_system(commId, tableId)
    upload_schema(data, domainId, tableId, tableName, k)

def master(filepath, sysName):
    comm = sysName
    commId = get_system_id(comm, username=my_username, password=my_password)
    filename =  filepath
    filename = filename.replace("\\", "/")
    filename = filename.replace("c:", "C:")
    print (filename)
    file = open(filename, "r")
    data = json.load(file)
    run_program(data, commId, sysName)


dirname = os.path.dirname(__file__)
singleFileName = os.listdir(path='.')
for each in singleFileName:
    avros = []
    # if os.path.isfile(each):
    #     if each.endswith(".avsc"):
    #         path = dirname + "/" + each
    #         singleName = each
    #         path = path.replace("//","/")
    if os.path.isdir(each):
        sys = os.listdir(path=each)
        for tab in sys:
            if tab.endswith(".avsc"):
                filepath = dirname + "/" + each + "/" + tab
                filepath = filepath.replace("\\","/")
                master(filepath, each)

