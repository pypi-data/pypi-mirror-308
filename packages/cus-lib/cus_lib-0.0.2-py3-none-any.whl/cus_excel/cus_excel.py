import win32com.client as win32

def change_excel_format(file_path):
    """
    修改excel格式.
    支持xls->xlsx和xlsx->xls
    :param file_path:
    :return:

    """
    excel = win32.gencache.EnsureDispatch("Excel.Application")
    # 关闭显示警告
    excel.DisplayAlerts = False
    wb = excel.Workbooks.Open(file_path)
    try:
        is_xlsx = ".xlsx" in file_path
        if is_xlsx:
            wb.SaveAs(file_path[:-1], FileFormat=56)  # xlsx转xls
        else:
            wb.SaveAs(file_path + "x", FileFormat=51)  # xls转xlsx
    except Exception as e:
        print(f"xls<->xlsx转换异常:{e}")
    finally:
        wb.Close()
        excel.Application.Quit()
