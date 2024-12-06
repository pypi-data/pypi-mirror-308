from influxdb_client import InfluxDBClient
import numpy as np
from datetime import datetime, timedelta
import lab.wheel.wheel_data_process



def get_field_value_from_influxdb(database: dict, time_start, time_end, fields: list):
    fields_str = ''
    for i in range(len(fields)):
        if i == 0:
            fields_str += f'r._field == "{fields[i]}"'
        else:
            fields_str += f' or r._field == "{fields[i]}"'

    query = (f'from(bucket: "{database["bucket"]}") '
            f'|> range(start: {time_start}, stop: {time_end}) '
            f'|> filter(fn: (r) => {fields_str}) '
            f'|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")  ')


    with InfluxDBClient(url=database['url'], token=database['token'], org=database['org']) as client:
        tables = client.query_api().query(query)


    data_rows = []
    # 遍历查询结果
    for table in tables:
        for record in table.records:
            # 提取时间戳和每个字段的值
            row = []
            row.append(record.get_time().timestamp())
            for field in fields:
                row.append(record.values.get(field))
            
            data_rows.append(row)

    return data_rows


def beijing_to_utc_time_str(beijing_time_str):
    # 将字符串转换为 datetime 对象
    beijing_time = datetime.strptime(beijing_time_str, '%Y-%m-%dT%H:%M:%S')

    # 北京时间转为 UTC 时间，减去8小时
    utc_time = beijing_time - timedelta(hours=8)

    # 转换为字符串表示
    utc_time_str = utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    return utc_time_str


wheel_test = {
    "start_time": '2024-09-21T09:00:00',
    "end_time": '2024-09-21T09:40:00',
    "tm_tag": ['TMKA553', 'TMKA561', 'TMKA569', 'TMKA577']
}

sat_database = {
    "C03": {
        'url': "http://172.16.111.211:8086",
        'token': "u0OGUlvv6IGGYSxpoZGZNjenBtE-1ADcdun-W-0oacL66cef5DXPmDwVzj93oP1MRBBCCUOWNFS9yMb77o5OCQ==",
        'org': "gs",
        'bucket': "piesat02_c03_database"
    }
}

data_list = get_field_value_from_influxdb(
    sat_database['C03'],
    beijing_to_utc_time_str(wheel_test['start_time']), 
    beijing_to_utc_time_str(wheel_test['end_time']), 
    wheel_test['tm_tag'])

data_array = np.array(data_list)


for i in range(len(wheel_test['tm_tag'])):
    dt = lab.wheel.wheel_data_process.calc_slide_time(data_array[:,0], data_array[:,i+1], 5990, 3000)
    print(f"飞轮 {i} 惯滑时间为 {dt:.0f} s")

