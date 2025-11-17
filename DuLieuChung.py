import os

class SharedVariables:
    MaNV = ""
    
    # Đường dẫn kết nối SQL (Giữ nguyên như bạn đã sửa lúc nãy)
    connectionString = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=PERSONAL-01;"
        "Database=PY_CAFE;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    # --- THÊM PHẦN XỬ LÝ ICON ---
    # Tự động lấy đường dẫn thư mục chứa file code hiện tại
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Nối thêm folder Icon và tên file
    icon_path = os.path.join(base_dir, "Icon", "cafe_icon.ico")

    @staticmethod
    def set_icon(window):
        """Hàm hỗ trợ set icon cho form an toàn"""
        try:
            if os.path.exists(SharedVariables.icon_path):
                window.iconbitmap(SharedVariables.icon_path)
            else:
                print(f"Không tìm thấy icon tại: {SharedVariables.icon_path}")
        except Exception as ex:
            print(f"Lỗi set icon: {ex}")