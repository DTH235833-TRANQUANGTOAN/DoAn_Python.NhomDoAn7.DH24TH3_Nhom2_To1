# formQuanLyHoaDon.py
import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from DuLieuChung import SharedVariables

class formQuanLyHoaDon(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.InitializeComponent()
        self.formQuanLyHoaDon_Load()

    def InitializeComponent(self):
        self.title("Quản Lý Hóa Đơn")
        SharedVariables.set_icon(self)
        self.geometry("1156x450") # Tăng chiều cao chút cho thoáng

        # Label Title
        self.label1 = tk.Label(self, text="HÓA ĐƠN", font=("Segoe UI", 25))
        self.label1.place(x=35, y=4)

        # Buttons
        self.btnXoa = tk.Button(self, text="Xóa hóa đơn", width=20, height=2, command=self.btnXoa_Click)
        self.btnXoa.place(x=641, y=21)

        self.btnThoat = tk.Button(self, text="Thoát", width=20, height=2, command=self.btnThoat_Click)
        self.btnThoat.place(x=890, y=21)

        # GridHoaDon (Treeview)
        cols = ("MaHD", "NgayLap", "MaNV", "MaKH", "TongTien")
        self.GridHoaDon = ttk.Treeview(self, columns=cols, show='headings')
        
        self.GridHoaDon.heading("MaHD", text="Mã hóa đơn")
        self.GridHoaDon.heading("NgayLap", text="Ngày lập")
        self.GridHoaDon.heading("MaNV", text="Mã nhân viên")
        self.GridHoaDon.heading("MaKH", text="Mã khách hàng")
        self.GridHoaDon.heading("TongTien", text="Tổng tiền")

        self.GridHoaDon.column("MaHD", width=150)
        self.GridHoaDon.column("NgayLap", width=200) # Python cần rộng hơn xíu để hiện đủ giờ
        self.GridHoaDon.column("MaNV", width=150)
        self.GridHoaDon.column("MaKH", width=150)
        self.GridHoaDon.column("TongTien", width=350)

        self.GridHoaDon.place(x=12, y=100, width=1132, height=253)

    def formQuanLyHoaDon_Load(self):
        self.XemQuyen()
        self.NapDuLieu()

    def XemQuyen(self):
        # Logic phân quyền: Chỉ Quản Lý mới được xóa
        query = "SELECT CHUCVU FROM NhanVien WHERE MANV= ?"
        try:
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            cursor.execute(query, (SharedVariables.MaNV,))
            row = cursor.fetchone()
            
            if row:
                chucVu = row[0].strip()
                # So sánh chuỗi (Python phân biệt hoa thường nên cẩn thận)
                if chucVu.lower() != "quản lý": 
                    self.btnXoa['state'] = 'disabled'
            conn.close()
        except Exception as ex:
            messagebox.showerror("Lỗi", "Lỗi kết nối CSDL: " + str(ex))

    def NapDuLieu(self):
        query = "SELECT * FROM HoaDon"
        try:
            self.GridHoaDon.delete(*self.GridHoaDon.get_children())
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            cursor.execute(query)
            
            for row in cursor.fetchall():
                # Format ngày tháng
                ngayLap = ""
                if row[3]: # Index 3 là NGAYLAP trong bảng HoaDon (tùy cấu trúc bảng thực tế)
                     # Lưu ý: check lại thứ tự cột trong DB của bạn. 
                     # Code C# dùng row["NGAYLAP"], ở đây giả định row[3]
                     try:
                         ngayLap = row[3].strftime("%d/%m/%Y")
                     except: ngayLap = str(row[3])

                # Lưu ý: row index dựa trên thứ tự cột trong DB: MAHD, MANV, MAKH, NGAYLAP, TONGTIEN
                # Cần map đúng vào thứ tự cột của Treeview
                self.GridHoaDon.insert("", tk.END, values=(row[0], ngayLap, row[1], row[2], f"{row[4]:,.0f}"))
            conn.close()
        except Exception as ex:
            messagebox.showerror("Lỗi", "Lỗi tải dữ liệu: " + str(ex))

    def btnXoa_Click(self):
        selected = self.GridHoaDon.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn hóa đơn cần xóa")
            return

        # Xác nhận xóa
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa hóa đơn này không?")
        if not confirm: return

        item = self.GridHoaDon.item(selected[0])
        maHD = item['values'][0] # Lấy MaHD ở cột đầu tiên
        
        self.XoaHoaDon(maHD)

    def XoaHoaDon(self, maHD):
        # Xóa Chi tiết trước, Hóa đơn sau
        sql_details = "DELETE FROM ChiTietHoaDon WHERE MAHD = ?"
        sql_header = "DELETE FROM HoaDon WHERE MAHD = ?"
        
        try:
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            
            cursor.execute(sql_details, (maHD,))
            cursor.execute(sql_header, (maHD,))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Thông báo", "Xóa hóa đơn thành công!")
            self.NapDuLieu()
            
        except Exception as ex:
            messagebox.showerror("Lỗi DB", str(ex))

    def btnThoat_Click(self):
        self.destroy()