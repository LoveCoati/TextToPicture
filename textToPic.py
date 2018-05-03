import os
import json
import win32clipboard
from io import BytesIO
from PIL import Image,ImageDraw,ImageFont


class DrawText:
    def __init__(self):
        self.gap = 20                 # 预留的边距
        self.font_list = []           # 字体列表
        self.font_size = 24           # 字体大小
        self.row_max_len = 10         # 每一行文字数量控制
        self.font_source = ""
        self.font_background_color = "#FFFFFF"
        self.picture_sieze = (0, 0)
        self.keys = ["fontSize", "fontColor", "fontType", "maxLen", "fontBackgroundColor"]
        self.config()

    def config(self):
        try:
            if os.path.exists("config.txt"):
                with open("config.txt", "r") as file :
                    data = file.read()
                    json_data = json.loads(data)
                    for key in self.keys:
                        if key not in json_data.keys():
                            print ("缺少配置: ", key)
                            os.system("pause")
                            os._exit(1) 
                    self.font_size = int(json_data["fontSize"])
                    self.font_source = str(json_data["fontType"])
                    self.font_color = str(json_data["fontColor"])
                    self.row_max_len = int(json_data["maxLen"])
                    self.font_background_color = str(json_data["fontBackgroundColor"])
                    self.font = ImageFont.truetype(self.font_source, self.font_size)
            else:
                print ("not find config.txt")
                os.system("pause")
                os._exit(1)
        except Exception as error_message:
            print (str(error_message))
            os.system("pause")
            os._exit(1) 

    def send_to_clipboard(self, clip_type, data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, data)
        win32clipboard.CloseClipboard()

    def draw_text(self, text):
        try:
            print (text)
            row = int(len(text)/self.row_max_len)     # 先计算出文字有几行
            if len(text)%self.row_max_len > 0:
                row += 1
            print ("len----------", len(text))
            print ("row----------", row)
            print((int(self.row_max_len*(self.font_size + self.gap*3)), int(row*(self.font_size + self.gap) + self.gap )))
            
            # 创建图片空间
            if row == 1:
                img = Image.new('RGB', (int(len(text)*(self.font_size) + self.gap*3), int(row*(self.font_size + self.gap) + self.gap)), self.font_background_color)
            else:
                img = Image.new('RGB', (int(self.row_max_len*(self.font_size) + self.gap*3), int(row*(self.font_size + self.gap) + self.gap)), self.font_background_color)
            draw = ImageDraw.Draw(img)

            # 在图片空间上写字
            for index in range(0, row):
                print ("start", (0, index*(self.font_size+self.gap)))
                print (index*self.row_max_len, (index + 1)*self.row_max_len - 1)
                draw.text( (self.gap, index*(self.font_size + self.gap) + self.gap), text[index*self.row_max_len : (index + 1)*self.row_max_len], font=self.font, fill=self.font_color)
            
            output = BytesIO()
            img.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()
            self.send_to_clipboard(win32clipboard.CF_DIB, data)
        except Exception as error_message:
            print (str(error_message))

    # 获取字体列表
    def GetFileList(self, filePath, fileList):
        newDir = filePath
        if os.path.isfile(filePath):
            fileData = os.path.splitext(os.path.basename(filePath))
            if (str(fileData[1]).lower() == '.ttf' or str(fileData[1]).lower() == ".fon"):
                fileList.append(fileData[0] + fileData[1])
        elif os.path.isdir(filePath):  
            for s in os.listdir(filePath):
                newDir=os.path.join(filePath,s)
                self.GetFileList(newDir, fileList)  
        return fileList

    # 设置选项
    def set(self):
        try:
            print ("- "* 20)
            print ("--[1]  修改字体大小")
            print ("--[2]  修改字体颜色")
            print ("--[3]  修改每行长度")
            print ("--[4]  修改文字字体")
            print ("--[5]  修改背景颜色")
            print ("- "* 20)
            select = int(input("输入选择: "))
            if select == 1:
                self.font_size = int(input("字体大小: "))
                self.font = ImageFont.truetype(self.font_source, self.font_size)
            elif select == 2:
                self.font_color= str(input("字体颜色: "))
            elif select == 3:
                self.row_max_len = int(input("每行长度: "))
            elif select == 4:
                self.font_list = self.GetFileList(os.getcwd(), [])
                for index, data in enumerate(self.font_list):
                    print ("--[%d]  %s"  % (index, data))
                select_num  = int(input("字体编号: "))
                if select_num < 0 or select_num >= len(self.font_list):
                    print ("选择错误....")
                else:
                    self.font = ImageFont.truetype(self.font_list[select_num], self.font_size)
            elif select == 5:
                self.font_background_color = str(input("背景颜色: "))
        except Exception as error_message:
            print (str(error_message))
            os.system("pause")
            os._exit(1) 

if __name__ == '__main__':
    test = DrawText()
    os.system("title Word Art Generator")
    while True:
        text = input("小主请输入: ")
        if len(text) == 0:
            continue
        if text == "set":
            test.set()
        else:
            test.draw_text(text)


