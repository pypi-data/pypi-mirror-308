import pandas as pd
import re
import csv
from decrypt import decrypt
import numpy as np

def parse_scan_array(line):
    elements = line.strip().split()
    
    if len(elements) < 4:  # Cần ít nhất 4 phần tử cho version, basetime và hai giá trị frames_capture
        return None, None, [], [] , []

    version = elements[0]
    basetime = float(elements[1])
    
    frames_capture = [float(elements[2]), float(elements[3])]
    total_frames = int(sum(frames_capture))  # Tổng số frames

    data = []
    index = 4  # Bắt đầu từ phần tử thứ 4

    # Lấy thông tin cho từng frame
    for frame_index in range(total_frames):
        frame_data = {}
        if index + 6 + (468 * 3) <= len(elements): 
            frame_data = {
                'Time_Difference': float(elements[index]),
                'Face_Status': str(elements[index + 1]),
                'Box_Xmin': float(elements[index + 2]),
                'Box_Ymin': float(elements[index + 3]),
                'Box_Width': float(elements[index + 4]),
                'Box_Height': float(elements[index + 5]),
                'Landmarks': np.zeros((468, 3), dtype=np.float32)  
            }

            # Lấy 468 landmarks
            for landmark_index in range(468):
                frame_data['Landmarks'][landmark_index] = [
                    float(elements[index + 6 + landmark_index * 3]),
                    float(elements[index + 7 + landmark_index * 3]),
                    float(elements[index + 8 + landmark_index * 3])
                ]
            data.append(frame_data)

            index += 6 + 468 * 3  
        else:
            break  # Không đủ dữ liệu cho frame tiếp theo, dừng lại


    # Lấy thông tin sensor
    if index < len(elements):
        total_sensor_frames = int(float(elements[index]))  # Số frame sensor
        index += 1 
        sensor_data = []
        
        for sensor_frame_index in range(total_sensor_frames):
            sensor_info = {}
            if index + 8 <= len(elements): 
                sensor_info['Timestamp'] = float(elements[index])
                sensor_info['Proximity'] = float(elements[index + 1])
                sensor_info['Accelerometer_X'] = float(elements[index + 2])
                sensor_info['Accelerometer_Y'] = float(elements[index + 3])
                sensor_info['Accelerometer_Z'] = float(elements[index + 4])
                sensor_info['Gyroscope_X'] = float(elements[index + 5])
                sensor_info['Gyroscope_Y'] = float(elements[index + 6])
                sensor_info['Gyroscope_Z'] = float(elements[index + 7])
                
                index += 8  
            
            sensor_data.append(sensor_info)

        return version, total_frames, basetime, data, sensor_data
    return version, total_frames, basetime, data, []


def export_to_csv(csv_file, sensor_csv_file, version,total_frames, basetime, frame_data, sensor_data):
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        header = ['Version','Total_Frames', 'Basetime', 'Frame_Time_Difference', 'Frame_Face_Status', 
                  'Frame_Box_Xmin', 'Frame_Box_Ymin', 'Frame_Box_Width', 'Frame_Box_Height'] 
        for i in range(468):
            header.append(f'Frame_Landmark_{i} X')  # Tọa độ X
            header.append(f'Frame_Landmark_{i} Y')  # Tọa độ Y
            header.append(f'Frame_Landmark_{i} Z')  # Tọa độ Z
        
        writer.writerow(header)
       
        for frame in frame_data:
            row = [version, total_frames, basetime]
            row.append(frame.get('Time_Difference', ''))
            row.append(frame.get('Face_Status', ''))
            row.append(frame.get('Box_Xmin', ''))
            row.append(frame.get('Box_Ymin', ''))
            row.append(frame.get('Box_Width', ''))
            row.append(frame.get('Box_Height', ''))

            landmarks = frame.get('Landmarks', np.zeros((468, 3), dtype=np.float32))
            for landmark in landmarks:
                row.append(landmark[0])  # Tọa độ x
                row.append(landmark[1])  # Tọa độ y
                row.append(landmark[2])  # Tọa độ z

            writer.writerow(row)  
            
    # Tách dữ liệu cảm biến vào file CSV mới
    with open(sensor_csv_file, 'w', newline='') as sensor_csvfile:
        sensor_writer = csv.writer(sensor_csvfile)
        
        sensor_header = ['Version', 'Total_Frames', 'Basetime', 
                         'Sensor_Timestamp', 'Sensor_Proximity', 
                         'Sensor_Accelerometer_X', 'Sensor_Accelerometer_Y', 
                         'Sensor_Accelerometer_Z', 'Sensor_Gyroscope_X', 
                         'Sensor_Gyroscope_Y', 'Sensor_Gyroscope_Z']
        
        sensor_writer.writerow(sensor_header)

        for sensor in sensor_data:
            sensor_row = [version, len(sensor_data), basetime]  # Thêm thông tin chung
            sensor_row.append(sensor.get('Timestamp', ''))
            sensor_row.append(sensor.get('Proximity', ''))
            sensor_row.append(sensor.get('Accelerometer_X', ''))
            sensor_row.append(sensor.get('Accelerometer_Y', ''))
            sensor_row.append(sensor.get('Accelerometer_Z', ''))
            sensor_row.append(sensor.get('Gyroscope_X', ''))
            sensor_row.append(sensor.get('Gyroscope_Y', ''))
            sensor_row.append(sensor.get('Gyroscope_Z', ''))
            
            sensor_writer.writerow(sensor_row)


def parse_behavior_log(lines):
    data = []

    for line in lines:
        if line.startswith('LOG_RECORD'):
            continue  # Bỏ qua dòng "LOG_RECORD"
        if line.strip() == '':
            continue  

        parts = re.split(r'[_\[\]]+', line)  
        
        if len(parts) > 1:
            event_type = parts[0]  # HCS, FS, BS, ...
            event_id = parts[1]    # 1727239859749
            action_or_status = parts[2] if len(parts) > 2 else None  # Hành động hoặc trạng thái
            value = parts[3] if len(parts) > 3 else None  # Giá trị

            # Xử lý giá trị cho ACC, GYR, RV
            if value and ("ACC" in action_or_status or "GYR" in action_or_status or "RV" in action_or_status):
                value = re.sub(r'[^0-9.,-]', '', value)  # Lọc các ký tự không hợp lệ
                values_list = list(map(str, value.split(',')))
                data.append([event_type, event_id, action_or_status] + values_list)
            elif value and "LT" in action_or_status:  # Xử lý trường LT
                value = re.sub(r'[^0-9.-]', '', value)  
                data.append([event_type, event_id, action_or_status, float(value)])  # Chỉ có 1 giá trị
            else:
                data.append([event_type, event_id, action_or_status] + [None] * 3)  #Khong có gì thì None
    return data


if __name__ == '__main__':
    import time 
    i = 0
    while True:
        #Giải mã file scan3d
        file_path_enc = "scan3d"
        result_dec = decrypt(file_path_enc)
        lines = result_dec.split('\n')
        
        # Đọc và phân tích scan array
        version, total_frames, basetime, frame_data, sensor_data = parse_scan_array(lines[0])
        s = time.time()
        frame_info_path = "o/frame_info_{}.csv".format(s)
        sensor_info_path = "o/sensor_info{}.csv".format(s)
        export_to_csv(frame_info_path, sensor_info_path, version, total_frames, basetime, frame_data, sensor_data)
        
        # Đọc và phân tích hành vi
        behavior_data = parse_behavior_log(lines[1:])
        column_names = ["Event Type", "Base Time", "Action/Status", "Value 1", "Value 2", "Value 3"]
        df = pd.DataFrame(behavior_data, columns=column_names)
        output_file = 'o/behavior{}.csv'.format(s)
        df.to_csv(output_file, index=False)
        print(i)
        i = i +1
