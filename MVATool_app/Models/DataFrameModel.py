from PyQt5 import QtCore, QtGui
from Models.Model import Model
from GUI.Style import get_style
import pandas as pd

class DataFrameModel(QtCore.QAbstractTableModel):
    DtypeRole = QtCore.Qt.UserRole + 1000
    ValueRole = QtCore.Qt.UserRole + 1001

    def __init__(self, df=pd.DataFrame(), parent=None):
        super(DataFrameModel, self).__init__(parent)
        self._dataframe = df
        self.primary_rows = list()
        self.secondary_rows = list()
        self.discarded_rows = list()
        self.primary_cols = list()
        self.secondary_cols = list()
        self.discarded_cols = list()

        self.test_counter = 0

    def set_rows_and_cols_info(self, pr, sr, dr, pc, sc, dc):
        self.primary_rows = pr
        self.secondary_rows = sr
        self.discarded_rows = dr
        self.primary_cols = pc
        self.secondary_cols = sc
        self.discarded_cols = dc

    def setDataFrame(self, dataframe):
        self.beginResetModel()
        self._dataframe = dataframe.copy()
        self.endResetModel()

    def dataFrame(self):
        return self._dataframe

    dataFrame = QtCore.pyqtProperty(pd.DataFrame, fget=dataFrame, fset=setDataFrame)

    @QtCore.pyqtSlot(int, QtCore.Qt.Orientation, result=str)
    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._dataframe.columns[section]
            else:
                return str(self._dataframe.index[section])
        return QtCore.QVariant()

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._dataframe.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return self._dataframe.columns.size
    
    # MAIN FUNCTION
    def data(self, index, role=QtCore.Qt.DisplayRole):

        if role == QtCore.Qt.BackgroundColorRole:
            self.test_counter = self.test_counter + 1
            #print(self.test_counter)
            # if is not in primary cols o secondary cols
            is_in_primary_col = self.primary_cols is not None and index.column() in self.primary_cols
            is_in_secondary_col = self.secondary_cols is not None and index.column() in self.secondary_cols
            is_in_discarded_col = self.discarded_cols is not None and index.column() in self.discarded_cols

            is_in_primary_row = self.primary_rows is not None and index.row() in self.primary_rows
            is_in_secondary_row = self.secondary_rows is not None and index.row() in self.secondary_rows
            is_in_discarded_row = self.discarded_rows is not None and index.row() in self.discarded_rows

            if is_in_primary_row:
                return QtGui.QBrush(get_style().color_primary_row())
            elif is_in_secondary_row:
                return QtGui.QBrush(get_style().color_secondary_row())
            elif is_in_discarded_row:
                return QtGui.QBrush(get_style().color_discarded())

            if not is_in_primary_row and not is_in_secondary_row:
                if is_in_primary_col:
                    return QtGui.QBrush(get_style().color_primary_col())
                elif is_in_secondary_col:
                    return QtGui.QBrush(get_style().color_secondary_col())
                elif is_in_discarded_col:
                    return QtGui.QBrush(get_style().color_discarded())

        if not index.isValid() or not (0 <= index.row() < self.rowCount() \
            and 0 <= index.column() < self.columnCount()):
            return QtCore.QVariant()
        row = self._dataframe.index[index.row()]
        col = self._dataframe.columns[index.column()]
        dt = self._dataframe[col].dtype

        val = self._dataframe.iloc[row][col]
        if role == QtCore.Qt.DisplayRole:
            return str(val)
        elif role == DataFrameModel.ValueRole:
            return val
        if role == DataFrameModel.DtypeRole:
            return dt

        return QtCore.QVariant()

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role != QtCore.Qt.EditRole:
            return False
        row = index.row()
        if row < 0 or row >= len(self._dataframe.values):
            return False
        column = index.column()
        if column < 0 or column >= self._dataframe.columns.size:
            return False
            
            
        # TODO: Si es un campo data y no se puede castear a float, tralará
        if role == QtCore.Qt.EditRole and str(value) != "":
            self._dataframe.set_value(index.row(), index.column(), value)
            self.dataChanged.emit(index, index)


        print('index: ' + str(index.row()) + ',' + str(index.column()))
        print('value: ' + str(value))
        print('role: ' + str(role))
        print(QtCore.Qt.EditRole)
        return True

    def flags(self, index):
        flags = super(self.__class__,self).flags(index)
        flags |= QtCore.Qt.ItemIsEditable
        flags |= QtCore.Qt.ItemIsSelectable
        flags |= QtCore.Qt.ItemIsEnabled
        flags |= QtCore.Qt.ItemIsDragEnabled
        flags |= QtCore.Qt.ItemIsDropEnabled
        return flags

    def roleNames(self):
        roles = {
            QtCore.Qt.DisplayRole: b'display',
            DataFrameModel.DtypeRole: b'dtype',
            DataFrameModel.ValueRole: b'value'
        }
        return roles