import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog

# Step 1: Load image
def load_image():
    root = tk.Tk()
    root.withdraw()  # Hide main window
    file_path = filedialog.askopenfilename(title="Select a graph image")
    return Image.open(file_path)

# Step 2: Click anchors and extract data
def digitize_graph(img):
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.set_title("Click 4 anchor points in order:\n"
                 "x_min, x_max, y_min, y_max (on the image)")
    anchor_pts = []
    point_artists = []

    def onclick(event):
        if len(anchor_pts) < 4:
            if event.button == 1:
                anchor_pts.append((event.xdata, event.ydata))
                point = ax.plot(event.xdata, event.ydata, color = 'tab:red', marker = "s", alpha = 0.7)
                point_artists.append(point)
            elif event.button == 3:  # Right click to remove last
                anchor_pts.pop(-1)
                point = point_artists.pop(-1)
                point[0].remove()
            fig.canvas.draw()
        if len(anchor_pts) == 4:
            plt.close()
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

    anchor_pts = [anchor_pts[0], anchor_pts[1], anchor_pts[3], anchor_pts[2]]

    return anchor_pts

# Step 3: Map from pixel space to data space
def extract_data(img, anchors, x_range, y_range):
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.set_title("LEFT click: add point | RIGHT click: remove last\nClose window when done.")
    curve_pts = []
    point_artists = []

    # Unpack anchor points
    (x0_px, _), (x1_px, _), (_, y0_px), (_, y1_px) = anchors
    x_data_min, x_data_max = x_range
    y_data_min, y_data_max = y_range

    for pp in anchors:
        ax.plot(pp[0], pp[1], color = 'tab:red', marker = "s", alpha = 0.7)

    def onclick(event):
        if event.button == 1:  # Left click to add
            curve_pts.append((event.xdata, event.ydata))
            point = ax.plot(event.xdata, event.ydata, color = 'magenta', marker = "s")[0]
            point_artists.append(point)
            fig.canvas.draw()
        elif event.button == 3 and curve_pts:  # Right click to remove last
            curve_pts.pop(-1)
            point = point_artists.pop(-1)
            point.remove()
            fig.canvas.draw()

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

    data_points = []
    for x_px, y_px in curve_pts:
        x_data = x_data_min + (x_px - x0_px) / (x1_px - x0_px) * (x_data_max - x_data_min)
        y_data = y_data_min + (y_px - y1_px) / (y0_px - y1_px) * (y_data_max - y_data_min)
        data_points.append((x_data, y_data))

    return np.array(data_points)

# ---- Main App Flow ---- #
if __name__ == "__main__":
    img = load_image()
    anchor_points = digitize_graph(img)

    print("Now enter the actual axis ranges based on the anchors:")
    x_min = float(input("X axis min: "))
    x_max = float(input("X axis max: "))
    y_min = float(input("Y axis min: "))
    y_max = float(input("Y axis max: "))

    log_x = str(input("Log the X axis (True/False): "))
    log_y = str(input("Log the Y axis (True/False): "))

    if log_x == "True":
        log_x = True
    else:
        log_x = False
    if log_y == "True":
        log_y = True
    else:
        log_y = False

    if log_x and not log_y:
        data = extract_data(img, anchor_points, (np.log10(x_min), np.log10(x_max)), (y_min, y_max))
        data[:, 0] = 10**data[:, 0]
    elif log_y and not log_x:
        data = extract_data(img, anchor_points, (x_min, x_max), (np.log10(y_min), np.log10(y_max)))
        data[:, 1] = 10 ** data[:, 1]
    elif log_x and log_y:
        data = extract_data(img, anchor_points, (np.log10(x_min), np.log10(x_max)), (np.log10(y_min), np.log10(y_max)))
        data[:, 0] = 10 ** data[:, 0]
        data[:, 1] = 10 ** data[:, 1]
    else:
        data = extract_data(img, anchor_points, (x_min, x_max), (y_min, y_max))

    print("Extracted Data Points:")
    print(data)

    # Optionally plot or save
    plt.figure()
    plt.plot(data[:, 0], data[:, 1], 'bo-')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Digitized Data")
    plt.grid(True)
    if log_x:
        plt.xscale('log')
    if log_y:
        plt.yscale('log')
    plt.show()

    import csv
    import os

    # Ask for filename and export to CSV
    filename = input("Enter a name for the CSV file (without extension): ")
    filename = filename.strip().replace(" ", "_") + ".csv"

    # Save the data
    csv_path = os.path.join(os.getcwd(), filename)
    with open(csv_path, mode='w', newline='') as file:
       writer = csv.writer(file)
       writer.writerow(["X", "Y"])
       writer.writerows(data)

    print(f"✅ Data saved to: {csv_path}")

