import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random as rm
import tkinter as tk
import pandas as pd


# ============= Google Drive Environment =============== #
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]
json_file_name = 'soon-361013-a1bfe708a386.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1ODASwz-Ym1wPUzAIysxSaCD5prJqMQN07Ci9tBFtJ_o/edit#gid=1121346661'

# 문서 불러오기
doc = gc.open_by_url(spreadsheet_url)

# a 시트 불러오기
worksheet = doc.worksheet('sheet1')

# 순 편성 Flag
soon_flag = False

# ============= TKinter Environment =============== #
class Test():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("200x100")
        self.buttonA = tk.Button(self.root,
                                 text = "Clear",
                                 command=self.Clear_Sheet)

        self.buttonB = tk.Button(self.root,
                                text="Click to make Soon",
                                command=self.Make_Soon)

        self.buttonA.pack(side=tk.LEFT)
        self.buttonB.pack(side=tk.RIGHT)
        self.root.mainloop()

    def Clear_Sheet(self):
        worksheet.clear()

    def Make_Soon(self):
        global soon_flag
        soon_flag = True
      
app=Test()

# ============= Make Soon Squad =============== #
if soon_flag == True:
    # Make Name & 순장/예비순장 List
    names = worksheet.col_values(2)
    positions = worksheet.col_values(3)

    values = [[0 for col in range(len(names))] for row in range(2)]
    key_volunteer_sort = []
    soon_people_sort = []
    key_volunteer = []
    soon_people = []

    for i in range(1, len(names)):
        values[0][i] = names[i]
        values[1][i] = positions[i]

    for i in range(2):
        values[i] = list(filter(None, values[i]))

    # 전체 인원 / 순장수
    whole_num = len(values[0])
    squad_key = 4 # 순장 수 순원 수 비교하면서 적절하게 조절하면 됨

    print(f"전체인원 : {whole_num}명")

    # 1. 순장, 예비순장 분리
    for i in range(len(values[1])):
        if values[1][i] == '순장':
            key_volunteer_sort.append(values[0][i])
        else:
            soon_people_sort.append(values[0][i])

    # 이름 중복 제거
    for value in key_volunteer_sort:
        if value not in key_volunteer:
            key_volunteer.append(value)
    
    for value in soon_people_sort:
        if value not in soon_people:
            soon_people.append(value)

    whole_key = len(key_volunteer)
    whole_soon = len(soon_people)

    # 순장, 예비순장 인원 출력
    print(f"순장인원 : {whole_key}명")
    print(f"예비순장인원 : {whole_soon}명")


    # 2. 순 배치 한 조 당 6명 (4 / 2)
    squad_buf = []
    # 순장 배치
    for i in range(whole_key//squad_key):
        squad = []

    
        while len(squad) < squad_key:
            if len(key_volunteer) != 0:
                student = rm.choice(key_volunteer)
                if student not in squad:
                    squad.append(student)
                    key_volunteer.remove(student)

        # print(f"{i+1}", '조 :', squad)
        squad_buf.append(squad)

    for i in range(len(key_volunteer)):
        squad_buf[i].append(key_volunteer[i])

    # 예비순장 배치
    for i in range(len(squad_buf)):
        if len(soon_people) != 0:
            student = rm.choice(soon_people)
            if student not in squad:
                squad_buf[i].append(student)
                soon_people.remove(student)

    for i in range((whole_key//squad_key) - 1, 0, -1):
        if len(soon_people) != 0:
            student = rm.choice(soon_people)
            if student not in squad:
                squad_buf[i].append(student)
                soon_people.remove(student)
        else:
            break

    # 조 편성 결과 출력
    for i in range(len(squad_buf)):
        print(f"{i+1}", '조 :', squad_buf[i])

    # 엑셀파일로 Export
    formation = []
    for i in range(len(squad_buf)):
        formation.append(f"{i+1}"+'조')
    
    Soon = pd.DataFrame()
    Soon['조'] = formation
    Soon['이름'] = squad_buf

    Soon.to_excel(r"C:\Users\AnChangMin\Desktop\21-2\CCC\Soon_List.xlsx", index=False)
