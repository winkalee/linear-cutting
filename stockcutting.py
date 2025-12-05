from PySide2.QtWidgets import QApplication, QLineEdit, QPlainTextEdit, QTextEdit, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
import re


# import numpy as np

class Stats:

    def __init__(self):
        # 从文件中加载UI定义
        qfile_stats = QFile("linear.ui")
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load(qfile_stats)

        self.ui.button.clicked.connect(self.handleCalc)
        self.ui.ycEdit.textChanged.connect(self.handleTextChange_yc)
        self.ui.dfEdit.textChanged.connect(self.handleTextChange_df)

        # self.ui.ycEdit.setText("5950")
        # self.ui.dfEdit.setText("5")
        # self.ui.ycnameEdit.setText("框型材")
        # self.ui.ycEdit.setPlaceholderText('请输入数值！')
        # self.ui.dfEdit.setPlaceholderText("请输入数值！")
        # self.ui.ycnameEdit.setPlaceholderText("请输入型材名称！")

    def handleTextChange_yc(self):
        yc = self.ui.ycEdit.text()
        if not yc.isdigit():
            self.ui.ycEdit.clear()
            self.ui.ycEdit.setPlaceholderText('请输入数值！')

    def handleTextChange_df(self):
        df = self.ui.dfEdit.text()
        if not df.isdigit():
            self.ui.dfEdit.clear()
            self.ui.dfEdit.setPlaceholderText('请输入数值！')

    def handleCalc(self):

        info = self.ui.textEdit.toPlainText()

        # W = int(self.ui.ycEdit.text())
        W = self.ui.ycEdit.text()
        df = int(self.ui.dfEdit.text())
        ycname = self.ui.ycnameEdit.text()

        if W == '':
            QMessageBox.about(self.ui,
                              '提醒',
                              f'''原材料长度不能为空值！'''
                              )
            # self.ui.ycEdit.setFocus()
            self.ui.ycEdit.setText("5950")
            W = int(self.ui.ycEdit.text())
        elif W == '0':
            QMessageBox.about(self.ui,
                              '提醒',
                              f'''原材料长度不能为0！'''
                              )
            # self.ui.ycEdit.setFocus()
            self.ui.ycEdit.setText("5950")
            W = int(self.ui.ycEdit.text())
        else:
            W = int(self.ui.ycEdit.text())

        # print(W)
        # print(df)
        # print(ycname)
        self.ui.getresultEdit.setPlainText(
            f'''原材料长度： {W}    切割锯缝： {df}    材料名称： {ycname}'''
        )

        # 2个列表转化成1个列表
        def two2one(arr1, arr2):
            lenth = len(arr1)
            # print(lenth)
            for i in range(lenth):
                nmax = int(arr2[i])
                nmax = int(arr2[i])
                # print(nmax)
                temp = arr1[i]
                for j in range(1, nmax):
                    arr1.append(temp)
            # print(arr1)
            return arr1

        # 冒泡排序函数【<降序，>升序】
        def bubbleSort(arr):
            length = len(arr)

            for passnum in range(length - 1, 0, -1):
                for i in range(passnum):
                    if arr[i] < arr[i + 1]:
                        arr[i], arr[i + 1] = arr[i + 1], arr[i]

            return arr

        w = []
        q = []

        for line in info.splitlines():
            if not line.strip():
                continue
            # parts = line.split(' ') #只能单字符分割
            parts = re.split("[ |\t]", line)
            # print(parts)
            # print(len(parts))
            parts = [p for p in parts if p]
            lenths, numbers = parts
            # print(lenths)
            # print(numbers)
            w.append(int(lenths))
            q.append(int(numbers))
            # w.append(int(lenths))
            # q.append(int(numbers))
        # print(w)
        # print(q)

        self.ui.getresultEdit.append(
            f'''\n锯切长度：\n {w}
                \n锯切数量：\n {q}'''
        )

        #  对长度进行拆分、降序排列
        px = two2one(w, q)
        # print(px)
        bubbleSort(px)
        # print(px)

        # - 假设每切割一根用一个原料时总共lzg根原料
        lzg = int(len(px))

        # print(lzg)
        # print("切割尺寸中最小长度：" + str(zx))
        zx = int(px[-1])
        zd = int(px[0])

        # print(zx)
        # print(zd)

        # zgs[]-数组就是每根原料的属性，第二维的1组是组合方式，2组是长度
        zgs = [['' for col in range(0, 2)] for row in range(0, lzg)]
        # print(zgs)
        #  hmax最后得出的是用多少根原料
        hmax = 0
        for t in range(0, lzg):
            for h in range(0, lzg):
                if h > hmax:
                    hmax = h
                    # print(h)
                    # print(hmax)
                if len(str(zgs[h][0])) == 0:
                    zgs[h][0] = str(px[t])
                    zgs[h][1] = px[t]
                    break
                elif W - int(zgs[h][1]) - df - int(px[t]) >= 0:
                    # elif W - zgs[h][1] - df - px[t] >= 0:
                    zgs[h][0] = str(zgs[h][0]) + "+" + str(px[t])
                    zgs[h][1] = zgs[h][1] + df + px[t]
                    break

        # print(hmax)
        # print(zgs)
        # ------------------------------------------------------------------true
        # wy[]-数组是整合zgs数组即输出信息，第二维1组同zgs的第二维的1组wy，
        #     '2组每样剩余，3组处理1组使之更直观，4组是每样个数
        wy = [['' for col in range(0, 4)] for row in range(0, hmax)]
        wy[0][0] = zgs[0][0]
        wy[0][1] = W - zgs[0][1]
        sumtol = zgs[0][1]  # sumtol 总长度值
        wyid = 1
        for i in range(0, hmax):
            sumtol = sumtol + zgs[i + 1][1]
            # print(zgs[i][0])
            # print(zgs[i+1][0])
            if zgs[i][0] != zgs[i + 1][0]:
                wy[wyid][0] = zgs[i + 1][0]
                wy[wyid][1] = W - zgs[i + 1][1]
                wyid = wyid + 1
                # 利用wyid滚动

        # print(wy)
        # print(sumtol)
        # print(wyid)

        # ------------------------------------true
        # 处理第二维3组,简化列表
        mlgs = 1
        for i in range(0, wyid):
            sczh = wy[i][0].split("+", -1)
            sczh.append("999999999")
            # print(sczh)
            lb = min(list(enumerate(sczh)))[0]
            ub = max(list(enumerate(sczh)))[0]
            # print(sczh)
            # print(lb)
            # print(ub)
            for j in range(lb, ub):
                if sczh[j] == sczh[j + 1]:
                    mlgs = mlgs + 1
                    # print(sczh[j])
                    #  利用mlgs滚动'
                else:
                    scc = str(sczh[j]) + "mm×" + str(mlgs) + "  "
                    wy[i][2] = wy[i][2] + scc
                    mlgs = 1
                    # print(scc)
            # print(wy[i][2])

        # print(wy)

        # ------------------------------true
        # 处理第二维4组，每种切割方案的根数

        lbb = min(list(enumerate(wy)))[0]
        ubb = max(list(enumerate(wy)))[0]
        # print(lbb)
        # print(ubb)

        for j in range(0, hmax):
            wy[j][3] = 0
            # print(wy[j][3])

        for i in range(lbb, ubb + 1):
            for j in range(0, hmax + 1):
                if wy[i][0] == zgs[j][0]:
                    wy[i][3] += 1
                    # print(wy[i][3])
                    # print(wy[j][3])

        # print(hmax + 1)
        # print(wyid)
        # print(wy)
        # print(sumtol)
        lt = (hmax + 1) * W - sumtol
        bl = int(sumtol * 100.00 / ((hmax + 1) * W))
        # print(lt)
        # print(bl)

        # 输出结果
        arr10 = [x[1:] for x in wy]
        arr20 = arr10[0:wyid]
        # print(arr10)
        # print(arr20)

        self.ui.getresultEdit.append(
            f'''\n需要根数： {hmax + 1}    剩余料头： {lt}    方案数量： {wyid}    优化比率： {bl}%
                \n剩余料头 + 锯切方案 + 每种数量：\n'''
        )

        for i in range(0, wyid):
            self.ui.getresultEdit.append(f'''{arr20[i]}\n''')


app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()

# data
# 460 25
# 5776 23
# 4346 18
# 3360 45
# 460 25
# 660 45
# 5034 65
# 5324 24
# 5663 25
# 3443 35
# 4522 25
# 5905 22
# 4603 35


# # ------------------------excel部分--------------
# import xlrd
#
#
#
# # 冒泡排序函数【<降序，>升序】
# def bubbleSort(arr):
#     length = len(arr)
#
#     for passnum in range(length - 1, 0, -1):
#         for i in range(passnum):
#             if arr[i] < arr[i + 1]:
#                 arr[i], arr[i + 1] = arr[i + 1], arr[i]
#
#     return arr
#
#
# # 2个列表转化成1个列表
# def two2one(arr1, arr2):
#     lenth = len(arr1)
#     # print(lenth)
#     for i in range(lenth):
#         nmax = int(numbers[i])
#         nmax = int(arr2[i])
#         # print(nmax)
#         temp = arr1[i]
#         for j in range(1, nmax):
#             arr1.append(temp)
#     # print(arr1)
#     return arr1
#
#
# # ----------------------正文开始------------------------------
# book = xlrd.open_workbook("linearcutfile.xls")
# # print(f"表单数量：{book.nsheets}")
# # print(f"表单名称：{book.sheet_names()}")
# # 表单索引从0开始，获取第一个表单对象
# # sheet1 = book.sheet_by_index(0)
# # 获取名为2018的表单对象
# sheet1 = book.sheet_by_name('下料')
# # 获取所有的表单对象，放入一个列表返回
# # book.sheets()
# # 表单名（name）
# # 表单索引（number）
# # 表单行数（nrows）
# # 列数（ncols）
# # print(f"表单名：{sheet1.name} ")
# # print(f"表单索引：{sheet1.number}")
# # print(f"表单行数：{sheet1.nrows}")
# # print(f"表单列数：{sheet1.ncols}")
# # # 行号、列号都是从0开始计算
# # print(f"第一行内容是: {sheet1.row_values(rowx=0)}")
# # # 行号、列号都是从0开始计算
# # print(f"切割长度列表: {sheet1.col_values(colx=0, start_rowx=3)}")
# lenths = sheet1.col_values(colx=0, start_rowx=3)
# # print(lenths)
# # print(f"切割数量列表: {sheet1.col_values(colx=1, start_rowx=3)}")
# numbers = sheet1.col_values(colx=1, start_rowx=3)
# # print(numbers)
#
# # print(lenths)
# # print(numbers)
#
# #  对长度进行拆分、降序排列
# px = two2one(lenths, numbers)
# # print(px)
# bubbleSort(px)
# # print(px)
#
# # numbers = [1]*int(len(px))
# # print(numbers)
# # 数组Z调用值
# # print(px[0])
# # print(px[1])
# # print(int(px[1]))
# # print(px[0] - px[1])
#
# # 组合成二维数组px[]-未排序之前
# # lennum = list(zip(px, num))
# # print(lennum)
# # # 调用函数bubbleSort()-降序排列
#
# # # 行号、列号都是从0开始计算    ycsizeEdit
# # print(f"单元格B2-原料名称: {sheet1.cell_value(rowx=1, colx=1)}")
# ycname = sheet1.cell_value(rowx=1, colx=1)
# # print(ycname)
# # print(f"单元格D3-原料长度: {sheet1.cell_value(rowx=2, colx=3)}")
# yc = sheet1.cell_value(rowx=2, colx=3)
# # print(int(yc))
# # print(f"单元格D2-刀缝: {sheet1.cell_value(rowx=1, colx=3)}")
# df = sheet1.cell_value(rowx=1, colx=3)
# # print(int(df))
# # print(f"切割总根数为:{int(sum(numbers))}")
# # - 假设每切割一根用一个原料时总共lzg根原料
# lzg = int(len(px))
# # print(lzg)
# # print("切割尺寸中最小长度：" + str(zx))
# zx = int(px[-1])
# # print(zx)
#
# # zgs[]-数组就是每根原料的属性，第二维的1组是组合方式，2组是长度
# zgs = [['' for col in range(0, 2)] for row in range(0, lzg)]
# # print(zgs)
# #  hmax最后得出的是用多少根原料
# hmax = 0
# for t in range(0, lzg):
#     for h in range(0, lzg):
#         if h > hmax:
#             hmax = h
#             # print(h)
#             # print(hmax)
#         if len(str(zgs[h][0])) == 0:
#             zgs[h][0] = px[t]
#             zgs[h][1] = px[t]
#             break
#         elif yc - zgs[h][1] - df - px[t] >= 0:
#             zgs[h][0] = str(zgs[h][0]) + "+" + str(px[t])
#             zgs[h][1] = zgs[h][1] + df + px[t]
#             break
#
# # print(hmax)
# # print(zgs)
# # ------------------------------------------------------------------true
# # wy[]-数组是整合zgs数组即输出信息，第二维1组同zgs的第二维的1组wy，
# #     '2组每样剩余，3组处理1组使之更直观，4组是每样个数
# wy = [['' for col in range(0, 4)] for row in range(0, hmax)]
# wy[0][0] = zgs[0][0]
# wy[0][1] = yc - zgs[0][1]
# sumtol = zgs[0][1]  # sumtol 总长度值
# wyid = 1
# for i in range(0, hmax):
#     sumtol = sumtol + zgs[i + 1][1]
#     # print(zgs[i][0])
#     # print(zgs[i+1][0])
#     if zgs[i][0] != zgs[i + 1][0]:
#         wy[wyid][0] = zgs[i + 1][0]
#         wy[wyid][1] = yc - zgs[i + 1][1]
#         wyid = wyid + 1
#         # 利用wyid滚动
#
# # print(wy)
# # print(sumtol)
# # print(wyid)
# # ------------------------------------true
# # 处理第二维3组,简化列表
# mlgs = 1
# for i in range(0, wyid):
#     sczh = wy[i][0].split("+", -1)
#     sczh.append("9999")
#     # print(sczh)
#     lb = min(list(enumerate(sczh)))[0]
#     ub = max(list(enumerate(sczh)))[0]
#     # print(sczh)
#     # print(lb)
#     # print(ub)
#     for j in range(lb, ub):
#         if sczh[j] == sczh[j + 1]:
#             mlgs = mlgs + 1
#             # print(sczh[j])
#             #  利用mlgs滚动'
#         else:
#             scc = str(sczh[j]) + "mm×" + str(mlgs) + "  "
#             wy[i][2] = wy[i][2] + scc
#             mlgs = 1
#             # print(scc)
#     # print(wy[i][2])
#
# # print(wy)
# # ------------------------------true
#
# # 处理第二维4组，每种切割方案的根数
#
# lbb = min(list(enumerate(wy)))[0]
# ubb = max(list(enumerate(wy)))[0]
# # print(lbb)
# # print(ubb)
#
# for j in range(0, hmax):
#     wy[j][3] = 0
#     # print(wy[j][3])
#
# for i in range(lbb, ubb + 1):
#     for j in range(0, hmax + 1):
#         if wy[i][0] == zgs[j][0]:
#             wy[i][3] += 1
#             # print(wy[i][3])
#             # print(wy[j][3])
# # print(wy)
#
# # for i in range(0, hmax):
# #     while len(str(wy[-1][0])) == 0:
# #         wy[-1].remove()
#
# print(hmax + 1)
# print(wyid)
# print(wy)
# print(sumtol)
# lt = (hmax + 1) * yc - sumtol
# bl = sumtol * 100 / ((hmax + 1) * yc)
# print(lt)
# print(bl)
#
# # ---------------------------思维列表再整理,列表输出按 wyid 列出
# # 输出模块
# #     For i = 6 To wyid + 4
# #         Sheets("输出").Cells(i, 1) = i - 5
# #         Sheets("输出").Cells(i, 2) = wy(i - 5, 3)
# #         Sheets("输出").Cells(i, 6) = wy(i - 5, 4)
# #         Sheets("输出").Cells(i, 7) = wy(i - 5, 2)
# #     Next
# #     Sheets("输出").[b3] = Sheets("下料").[b2]
# #     Sheets("输出").[f2] = Now
# #     Sheets("输出").[d3] = yc
# #     Sheets("输出").[f3] = df
# #     Sheets("输出").[b4] = hmax
# #     Sheets("输出").[d4] = hmax * yc - sumtol
# #     Sheets("输出").[f4] = sumtol / (hmax * yc)
# #     Sheets("输出").Select
