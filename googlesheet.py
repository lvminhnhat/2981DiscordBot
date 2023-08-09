import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

class Sheet():
    def __init__(self):
        self.ss_cred_path = "rokdata.json"
        # Định nghĩa phạm vi và thông tin xác thực
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.ss_cred_path, self.scope)
        # Xác thực và kết nối đến Google Sheets
        self.client = gspread.authorize(self.creds)
        # ID của bảng tính
        self.spreadsheet_id = "1QG-W1DRwFys-VOt1r6c5asO8fzRZT-qx_OB85V0oJF4"
        # Mở bảng tính
        self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
        # Lấy danh sách các trang tính
        self.worksheet_list = self.spreadsheet.worksheets()
    def readData(self,sheet:str):
        worksheet = self.spreadsheet.worksheet(sheet)
        data = worksheet.get_all_values()
        headers = data.pop(0)
        df = pd.DataFrame(data, columns=headers)
        return df
    def writeData(self, sheet: str, data):
        worksheet = self.spreadsheet.worksheet(sheet)
        
        # Xóa dữ liệu cũ trong trang tính nếu dữ liệu là DataFrame
        if isinstance(data, pd.DataFrame):
            worksheet.clear()
            
            # Lấy danh sách cột (tiêu đề) từ DataFrame và loại bỏ khoảng trắng không cần thiết
            headers = [column.strip() for column in data.columns.tolist()]
            
            # Ghi tiêu đề vào hàng đầu tiên của trang tính
            worksheet.append_row(headers)
            
            # Chuyển đổi DataFrame thành danh sách các hàng
            data_rows = data.values.tolist()
            # Ghi các hàng từ DataFrame vào trang tính
            worksheet.append_rows(data_rows, value_input_option='USER_ENTERED')
        
        # Kiểm tra nếu dữ liệu là danh sách các hàng
        elif isinstance(data, list):
            # Ghi các hàng vào cuối trang tính
            worksheet.append_rows(data, value_input_option='RAW')
        
        else:
            print("Invalid data type. Please provide a DataFrame or a list of rows.")
    def createWorksheet(self, title):
        worksheet = self.spreadsheet.add_worksheet(title, 100, 100)
        return worksheet

if __name__ == "__main__":
    gg = Sheet()
    worksheet_list = gg.worksheet_list
    for worksheet in worksheet_list:
        print(worksheet.title)
        t = gg.readData(worksheet.title)
        print(t)
        if worksheet.title == "Coins":
            gg.writeData(worksheet.title, [6, "morning", 30000])




    