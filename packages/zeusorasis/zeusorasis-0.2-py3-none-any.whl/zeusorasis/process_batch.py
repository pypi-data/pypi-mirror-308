import cv2 as cv
import numpy as np
import mediapipe as mp
import pandas as pd
import csv
import matplotlib.pyplot as plt
import math
import os
import zipfile
import json
from shutil import move

mp_face_mesh = mp.solutions.face_mesh
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]
NOSE = 4


def process_batch(video_filename):
    
    print("process_webcam")

    cap = cv.VideoCapture(video_filename)

    # video parameters
    fps = cap.get(cv.CAP_PROP_FPS)
    frame_size = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))

    # VideoWriter object to save the output video
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    output_video_filename = f'{os.path.splitext(os.path.basename(video_filename))[0]}_detected.mp4'
    out = cv.VideoWriter(output_video_filename, fourcc, fps, frame_size)

    # Open a CSV file for writing
    csv_filename = f'{os.path.splitext(os.path.basename(video_filename))[0]}_detected.csv'
    csv_file = open(csv_filename, "w", newline="")
    csv_writer = csv.writer(csv_file)

    cv.namedWindow('Processed Frame', cv.WINDOW_NORMAL)

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv.flip(frame, 1)
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img_h, img_w = frame.shape[:2]
            results = face_mesh.process(rgb_frame)
            frame_count += 1

            if results.multi_face_landmarks:
                mesh_points = np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in results.multi_face_landmarks[0].landmark])
            else:
                continue

            (l_cx, l_cy), l_radius = cv.minEnclosingCircle(mesh_points[LEFT_IRIS])
            (r_cx, r_cy), r_radius = cv.minEnclosingCircle(mesh_points[RIGHT_IRIS])
            center_left = np.array([l_cx, l_cy], dtype=np.int32)
            center_right = np.array([r_cx, r_cy], dtype=np.int32)
            cv.circle(frame, center_left, int(l_radius), (255, 0, 255), 1, cv.LINE_AA)
            cv.circle(frame, center_right, int(r_radius), (255, 0, 255), 1, cv.LINE_AA)

            # Convert pixel coordinates to degrees
            left_iris_x_deg = center_left[0]
            left_iris_y_deg = center_left[1]
            right_iris_x_deg = center_right[0]
            right_iris_y_deg = center_right[1]
            """
            nose_x_deg = mesh_points[NOSE][0]
            nose_y_deg = mesh_points[NOSE][1]
            """
            averages = np.mean(mesh_points, axis=0)

            # Calculate cosine values
            """
            right_iris_x_deg_normalized = -np.cos(right_iris_x_deg * 3.14159 / 180)
            right_iris_y_deg_normalized = -np.cos(right_iris_y_deg * 3.14159 / 180)
            left_iris_x_deg_normalized = -np.cos(left_iris_x_deg * 3.14159 / 180)
            left_iris_y_deg_normalized = -np.cos(left_iris_y_deg * 3.14159 / 180)
            """
            # Calculate elapsed time relative to the start time based on frame count and frame rate
            elapsed_time = frame_count / fps

            # Write coordinates and cosine values to CSV
            csv_writer.writerow([0, 0, elapsed_time, right_iris_x_deg-averages[0], right_iris_y_deg-averages[1], 0, left_iris_x_deg-averages[0], left_iris_y_deg-averages[1], 0,
                                 elapsed_time, 0, averages[0], averages[1], -2.68555, 2.38037, -3.2959, -0.0644531, -0.361816, -0.917969])

            # Write the frame to the output video
            out.write(frame)

            # Show the frame in a window
            cv.imshow('Processed Frame', frame)

            key = cv.waitKey(1)
            if key == ord('q'):
                break

    # Release the video capture and output video objects
    cap.release()
    out.release()
    cv.destroyAllWindows()

    # Close the CSV file
    csv_file.close()

    # Create a JSON file named info.json and save it at the same location as the CSV file
    json_content = {
        "calib_norm_points": [
            {"from_3D": {"x": 0.5038552284240723, "y": 0.5455120205879211}, "ref": {"x": 0.4968579113483429, "y": 0.8448643088340759}},
            {"from_3D": {"x": 0.4815937876701355, "y": 0.539290189743042}, "ref": {"x": 0.46241214871406555, "y": 0.6852521896362305}}
        ],
        "orasis_version": "2.0.0",
        "record_length": "147.60s",
        "record_mode": "remobi",
        "record_start_date": "2023-07-18 17:47:06",
        "scenario_type": "saccade",
        "with_overlap": True
    }

    json_filename = f'{os.path.splitext(os.path.basename(video_filename))[0]}_info.json'
    with open(json_filename, 'w') as json_file:
        json.dump(json_content, json_file, indent=4)

    df = pd.read_csv(csv_filename,header=None)
    # Reindex the DataFrame
    df_copy = df.copy()

    current_fps = int(len(df)/df[2].values[-1])
    #print(current_fps)
    factor = round(200/current_fps)
    #print(factor)

    def primeFactors(n):
        prime_list = []
        while n % 2 == 0:
            prime_list.append(2)
            n = n // 2
            
        for i in range(3,int(math.sqrt(n))+1,2):
            while n % i== 0:
                prime_list.append(i)
                n = n // i

        if n > 2:
            prime_list.append(n)
        return prime_list

    prime_list = primeFactors(factor)
    for i in range(len(prime_list)):

      # Upsample by a factor of 5
      upsample_factor = prime_list[i]
      new_index = np.arange(len(df_copy) * upsample_factor)

      df_copy.index = df_copy.index * upsample_factor
      df_upsampled = df_copy.reindex(new_index)

      # Interpolate the NaN values using linear interpolation
      df_3rd_col = df_upsampled.iloc[:, 2]  # 3rd column (index 2, as it's 0-based)
      df_other_cols = df_upsampled.drop(df_upsampled.columns[2], axis=1)  # Drop the 3rd column
      
      # Apply linear interpolation to the 3rd column
      df_3rd_col_interpolated = df_3rd_col.interpolate(method='linear')

      # Apply polynomial interpolation to the remaining columns
      df_other_cols_interpolated = df_other_cols.interpolate(method='polynomial', order=11)
      
      # Insert the 3rd column back into the interpolated DataFrame
      df_upsampled_interpolated = df_other_cols_interpolated.copy()
      df_upsampled_interpolated.insert(2, df_3rd_col.name, df_3rd_col_interpolated)
      df_copy = df_upsampled_interpolated

    #print(df_upsampled_interpolated)
    print(f"ora fps = {int(len(df_upsampled_interpolated)/df[2].values[-1])}")
    df_upsampled_interpolated.loc[20:][3].plot()

    df = df_upsampled_interpolated.iloc[11:-11]

    # Make a copy of the DataFrame for normalized values
    df_normalized = df.copy()

    # Select the columns to normalize (these are by their indices)
    cols_to_normalize = [3, 4, 6, 7]

    for col in cols_to_normalize:
        # Minimum et maximum de la colonne
        min_val = df[col].min()
        max_val = df[col].max()
        
        # Calcul de la plage
        range_val = max_val - min_val
        print(f'colonne {col}, min {min_val}, max {max_val}, range {range_val}')
        
        # Si la plage est supérieure à 180 degrés, appliquer la normalisation linéaire
        if range_val > 180:
            # Normalisation linéaire entre -1 et 1
            df_normalized[col] = 2 * (df[col] - min_val) / range_val - 1
        
        else:
            # Centre la série autour de sa moyenne
            mean_val = df[col].mean()
            
            # Décalage pour centrer les valeurs autour de 0 en cosinus
            offset = mean_val - 90  # Décalage de façon à centrer autour de cos(90°) = 0
            
            # Ajustement des valeurs
            adjusted_values = df[col] - offset
            
            # Appliquer la fonction cosinus sur les valeurs ajustées pour les normaliser entre -1 et 1
            df_normalized[col] = np.cos(np.radians(adjusted_values))

            print("normalized cosine")

    # Affichage pour vérifier les résultats
    #print(df_normalized)
    # Plot each column in the normalized DataFrame
    plt.figure(figsize=(12, 8))

    for col in cols_to_normalize:
        plt.plot(df_normalized[col], label=f'Column {col}')

    # Add titles and labels
    plt.title("Normalized Data for Selected Columns")
    plt.xlabel("Index")
    plt.ylabel("Normalized Value")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()

        
    plt.plot(df_normalized[11], label=f'Column {11}')
    plt.plot(df_normalized[12], label=f'Column {12}')
    plt.show()

    df_normalized.to_csv(csv_filename,index=False, header=False)

    # Create a folder within the zip file and put the CSV file inside it
    zip_filename = f'{os.path.splitext(os.path.basename(video_filename))[0]}_output.ora'
    zip_folder_name = f'{os.path.splitext(os.path.basename(video_filename))[0]}_output_folder'

    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        zip_file.write(csv_filename, arcname=f'{zip_folder_name}/all_samples_in_one.csv')
        zip_file.write(json_filename, arcname=f'{zip_folder_name}/info.json')

    # Remove the files
    os.remove(csv_filename)
    os.remove(json_filename)

    # Create folders if not exists
    ora_folder = os.path.join(os.path.dirname(video_filename) ,f"{os.path.dirname(video_filename)}_ORA")
    detected_videos_folder = os.path.join(os.path.dirname(video_filename) ,f"{os.path.dirname(video_filename)}_VID")
    os.makedirs(ora_folder, exist_ok=True)
    os.makedirs(detected_videos_folder, exist_ok=True)

    # Move files to folders
    move(zip_filename, os.path.join(ora_folder, zip_filename))
    move(output_video_filename, os.path.join(detected_videos_folder, output_video_filename))
    print(os.path.join(detected_videos_folder, output_video_filename))