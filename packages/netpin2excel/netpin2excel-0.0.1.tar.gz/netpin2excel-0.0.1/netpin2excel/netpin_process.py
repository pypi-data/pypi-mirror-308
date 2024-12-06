import pandas as pd
import re
import io
import tkinter as tk

# 重定向标准输出到一个字符串缓冲区
class StdoutRedirector(io.StringIO):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def write(self, s):
        self.text_widget.insert(tk.END, s)
        self.text_widget.see(tk.END)  # 自动滚动到底部

# 公共的数据处理函数
def extract_data_from_file(file_path):
    data = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line == '(':
                i += 1
                if i < len(lines):
                    netname = lines[i].strip()
                    netpins = []
                    i += 1
                    while i < len(lines) and not lines[i].strip().startswith(')'):
                        netpin = lines[i].strip()
                        if netpin:
                            netpins.append(netpin)
                        i += 1
                    if i < len(lines) and lines[i].strip().startswith(')'):
                        i += 1
                    data[netname] = netpins
                    # print(f"Extracted: Netname={netname}, Netpins={netpins}")
            else:
                i += 1
    return data

def natural_keys(text):
    parts = re.split('(\d+)', text)
    return [int(part) if part.isdigit() else part for part in parts]

def process_data(data, type=None):
    data_list = []
    for netname, netpins in data.items():
        if type == 3:
            # 如果 netpins 只有一个子列表，直接将该子列表中的元素用空格连接
            netpins_str = ''.join(netpins[0])
        else:
            # 将 netpins 列表中的所有字符串用空格连接成一个单一的字符串
            netpins_str = ' '.join([''.join(pin) for pin in netpins])
        data_list.append([netname, netpins_str])
    first_pins = [(row[0], row[1].split()[0]) for row in data_list]
    sorted_first_pins = sorted(first_pins, key=lambda x: natural_keys(x[1]))
    sorted_data = []
    for net_name, first_pin in sorted_first_pins:
        for row in data_list:
            if row[0] == net_name and row[1].startswith(first_pin):
                sorted_data.append(row)
                break
    return sorted_data

def save_to_excel(data, output_file):
    new_df = pd.DataFrame(data, columns=['Net Name', 'Net Pins'])
    new_df.to_excel(output_file, index=False)

def read_excel(file_path):
    df = pd.read_excel(file_path)
    data = {}
    for _, row in df.iterrows():
        netname = row['Net Name']
        netpin = row['Net Pins']
        if netname not in data:
            data[netname] = []
        data[netname].append(netpin)
    return data
