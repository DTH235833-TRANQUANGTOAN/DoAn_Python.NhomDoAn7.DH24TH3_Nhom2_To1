import os

class SharedVariables:
    MaNV = ""
    
    # Đường dẫn kết nối SQL
    connectionString = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=PERSONAL-01;"
        "Database=PY_CAFE;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    # Tự động lấy đường dẫn thư mục chứa file code hiện tại
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Nối thêm folder Icon và tên file
    icon_path = os.path.join(base_dir, "Icon", "cafe_icon.ico")

    @staticmethod
    def set_icon(window): # Đặt icon cho cửa sổ, không cần truyền đường dẫn mỗi lần
        try:
            if os.path.exists(SharedVariables.icon_path):
                window.iconbitmap(SharedVariables.icon_path)
            else:
                print(f"Không tìm thấy icon tại: {SharedVariables.icon_path}") # không có thì in log ở console
        except Exception as ex:
            print(f"Lỗi set icon: {ex}")