
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from numpy.lib.npyio import NpzFile
from fcm1 import FCM1
from PyQt5 import uic
from fcm2 import FCM2

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

class MyWindowClass(QMainWindow):
    
    def __init__(self):
        super(MyWindowClass, self).__init__()
        uic.loadUi("FCM_application\main_window.ui", self)
        
        self.fcm1 = FCM1()
        self.fcm2 = FCM2()


    def choose_data(self):
        try:
            file_filter = 'Data File (*.xlsx *.csv *.data);; Excel File (*.xlsx *.xls)'
            path, _ = QFileDialog.getOpenFileName(parent=self, caption='Select a Data File', filter=file_filter,
                                                  options=QFileDialog.DontUseNativeDialog)
            
            self.data_path.setText(path)
            self.fcm1.read_data(path)
            self.fcm2.read_data(path)
            model_data = TableModel(self.fcm1.data_table)
            self.X_table.setModel(model_data)
            self.X_table.resizeColumnsToContents()
            self.begin_col.setText("1")
            self.begin_row.setText("1")
        except:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Please choose a data set !')
            
    def preprocess_data(self):
        if self.label_column.text()!='' and self.begin_col.text()!='' and self.begin_row.text()!='':
            label_col = int(self.label_column.text()) -1
            begin_col = int (self.begin_col.text()) -1
            begin_row = int (self.begin_row.text()) -1
            
            try:
                self.fcm1.preprocess_data(label_col, begin_col, begin_row)
                self.fcm2.preprocess_data(label_col, begin_col, begin_row) 
                self.message = QtWidgets.QMessageBox()
                self.message.setText("Column "+ str(label_col +1)+ " is label column ?")
                self.message.show()
                self.X_table.setModel(None)
                viewTable(self.fcm1.final_data_table, self.X_table)
            except:
                self.error_dialog = QtWidgets.QErrorMessage()
                self.error_dialog.showMessage('Please choose a column in range !')
    def reset_view(self):
        self.U_ngang_table_1.setModel(None)
        self.U_table_1.setModel(None)
        self.V_table_1.setModel(None)
        self.U_ngang_table_2.setModel(None)
        self.U_table_2.setModel(None)
        self.V_table_2.setModel(None)
        self.M_table_1.setModel(None)
        self.U_table_3.setModel(None)
        self.V_table_3.setModel(None)
        self.M_table_2.setModel(None)
        self.U_table_4.setModel(None)
        self.V_table_4.setModel(None)
        self.validity_table.clearContents()
    def caculate_cluster(self):
        self.reset_view()
        if self.k_text.text() != '' and (self.c_text.text() != '') and (self.epsilon_text.text() != ''):
            k = int(self.k_text.text())
            c = int(self.c_text.text())
            epsilon = float(self.epsilon_text.text())

            if self.algo1_check.isChecked(): #Kiểm tra có chạy thuật toán 1 hay ko
                try:
                    value_of_m = int(self.m_text.text())
                    self.fcm1.thuat_toan_1_pha(epsilon,value_of_m,c,k)
                    viewTable(self.fcm1.U_ngang, self.U_ngang_table_1)
                    viewTable(self.fcm1.U, self.U_table_1)
                    viewTable(self.fcm1.V, self.V_table_1)
                    
                    self.validity_table.setItem(0,0, QTableWidgetItem( str(round(self.fcm1.w1,4))))
                    self.validity_table.setItem(1,0, QTableWidgetItem(str(round(self.fcm1.w2,4))))
                    self.validity_table.setItem(2,0, QTableWidgetItem(str(round(self.fcm1.w3,4))))
                    
                    if self.check_2pha_algo1.isChecked():
                        self.fcm1.thuat_toan_2_pha(epsilon,value_of_m,c,k)
                        viewTable(self.fcm1.U_ngang, self.U_ngang_table_2)
                        viewTable(self.fcm1.U, self.U_table_2)
                        viewTable(self.fcm1.V, self.V_table_2)
                        
                        self.validity_table.setItem(0,1, QTableWidgetItem(str(round(self.fcm1.w1,4))))
                        self.validity_table.setItem(1,1, QTableWidgetItem(str(round(self.fcm1.w2,4))))
                        self.validity_table.setItem(2,1, QTableWidgetItem(str(round(self.fcm1.w3,4))))
                except:
                    self.error_dialog = QtWidgets.QErrorMessage()
                    self.error_dialog.showMessage('Please fill all input of Algorithm 1!')  
                
                    
            if self.algo2_check.isChecked(): #Kiểm tra có chạy thuật toán 2 hay ko
                try:
                    value_of_M = int(self.M_text.text())
                    value_of_M1= int(self.M1_text.text())
                    self.fcm2.thuat_toan_1_pha(value_of_M, value_of_M1, c, k, epsilon)
                    viewTable(self.fcm2.M, self.M_table_1)
                    viewTable(self.fcm2.U, self.U_table_3)
                    viewTable(self.fcm2.V, self.V_table_3)
                    
                    self.validity_table.setItem(0,2, QTableWidgetItem(str(round(self.fcm2.w1,4))))
                    self.validity_table.setItem(1,2, QTableWidgetItem(str(round(self.fcm2.w2,4))))
                    self.validity_table.setItem(2,2, QTableWidgetItem(str(round(self.fcm2.w3,4))))
                    
                    if self.check_2pha_algo2.isChecked():
                        self.fcm2.thuat_toan_2_pha(value_of_M, value_of_M1, c, k, epsilon)
                        viewTable(self.fcm2.M, self.M_table_2)
                        viewTable(self.fcm2.U, self.U_table_4)
                        viewTable(self.fcm2.V, self.V_table_4)
                        
                        self.validity_table.setItem(0,3, QTableWidgetItem(str(round(self.fcm2.w1,4))))
                        self.validity_table.setItem(1,3, QTableWidgetItem(str(round(self.fcm2.w2,4))))
                        self.validity_table.setItem(2,3, QTableWidgetItem(str(round(self.fcm2.w3,4))))
                except:
                    self.error_dialog = QtWidgets.QErrorMessage()
                    self.error_dialog.showMessage('Please fill all input of Algorithm 2!')  
        self.fcm1.freeMemory()
        self.fcm2.freeMemory()
            
def viewTable(table, nameView):
    model = TableModel(table)
    nameView.setModel(model)
    nameView.resizeColumnsToContents()
    
       
def main():
    app = QApplication([])
    mainWindow = MyWindowClass()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
