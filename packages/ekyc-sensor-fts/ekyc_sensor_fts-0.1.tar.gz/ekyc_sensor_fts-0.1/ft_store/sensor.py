import pandas as pd
import numpy as np
import copy

from server.decrypt import decrypt


def parse_scan_array(line):
    elements = line.strip().split()
    elements = copy.deepcopy(elements)
    if len(elements) < 4:  # Cần ít nhất 4 phần tử cho version, basetime và hai giá trị frames_capture
        del elements
        return None, None, [], [] , []

    version = elements[0]
    basetime = float(elements[1])

    if float(elements[3]) > 5:
        frames_capture = [float(elements[2]), 0]
        index = 3  # Bắt đầu từ phần tử thứ 3
    else:
        frames_capture = [float(elements[2]), float(elements[3])]
        index = 4  # Bắt đầu từ phần tử thứ 4
    total_frames = min(int(sum(frames_capture)),10)  # Tổng số frames
    
    data_df = pd.DataFrame()

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

            df_dictionary = pd.DataFrame([frame_data])
            data_df = pd.concat([data_df, df_dictionary], ignore_index=True)
            del frame_data
            index += 6 + 468 * 3  
        else:
            break  # Không đủ dữ liệu cho frame tiếp theo, dừng lại
    data_df["Version"] = version
    data_df["Total_Frames"] = total_frames
    data_df["Basetime"] = basetime
    # Lấy thông tin sensor
    if index < len(elements):
        total_sensor_frames = int(float(elements[index]))  # Số frame sensor
        index += 1 
        sensor_data_df = pd.DataFrame()
        sensor_info = {}
        
        for sensor_frame_index in range(total_sensor_frames)[-1000:]:
            sensor_info = {}
            if index + 8 <= len(elements): 
                sensor_info['Timestamp'] = elements[index]
                sensor_info['Proximity'] = elements[index + 1]
                sensor_info['Accelerometer_X'] = elements[index + 2]
                sensor_info['Accelerometer_Y'] = elements[index + 3]
                sensor_info['Accelerometer_Z'] = elements[index + 4]
                sensor_info['Gyroscope_X'] = elements[index + 5]
                sensor_info['Gyroscope_Y'] = elements[index + 6]
                sensor_info['Gyroscope_Z'] = elements[index + 7]
                
                index += 8  
            df_dictionary = pd.DataFrame([sensor_info])
            sensor_data_df = pd.concat([sensor_data_df, df_dictionary], ignore_index=True)
            del sensor_info
        del elements
        return data_df, sensor_data_df.astype("float")
    del elements
    return data_df, pd.DataFrame()


def decrypt_scan3d(scan_3d):
    ds = []
    for f in sorted(scan_3d):
        try:
            path = f.replace("scan3d", "")
            file_name = "scan3d"
            result_dec = decrypt(f)
            lines = result_dec.split('\n')
            frame_df, sensor_df = parse_scan_array(lines[0])
            d = {
                "_id" : f.split("/")[-2]
            }
            if len(sensor_df) == 0:
                continue

            for col in ['Proximity', 'Accelerometer_X', 'Accelerometer_Y', 'Accelerometer_Z', 'Gyroscope_X', 'Gyroscope_Y', 'Gyroscope_Z']:
                for agg in ["mean", "median", "max", "min", "std", "var"]:
                    d[f"{col}_{agg}"] = sensor_df[col].agg(agg)
            ds.append(d)
            print("Successfully run file: ", f)
        except:
            print(f"Can not process: {f}")

    df = pd.DataFrame(ds)
    return df


