import tkinter as tk
from tkinter import messagebox
import pyodbc
from DuLieuChung import SharedVariables  

class formChucNang(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.InitializeComponent()
        self.Form2_Load()

    def InitializeComponent(self):
        self.title("Chức năng")
        SharedVariables.set_icon(self)
        self.geometry("955x502")
        self.configure(bg="Beige")

        # Label Title
        self.label1 = tk.Label(self, text="CHỨC NĂNG", font=("Segoe UI", 15), bg="Beige")
        self.label1.place(x=378, y=9)

        # Label Chuc Vu
        self.label2 = tk.Label(self, text="chức vụ của bạn là: ...", font=("Segoe UI", 12), bg="Beige")
        self.label2.place(x=637, y=42)

        # Buttons style
        btn_style = {"bg": "Linen", "font": ("Segoe UI", 12)}

        self.btnBanHang = tk.Button(self, text="Bán hàng", **btn_style, command=self.btnBanHang_Click)
        self.btnBanHang.place(x=105, y=77, width=167, height=74)

        self.btnNhapNguyenLieu = tk.Button(self, text="Nhập Nguyên liệu", **btn_style, command=self.btnNhapNguyenLieu_Click)
        self.btnNhapNguyenLieu.place(x=278, y=77, width=167, height=74)

        self.btnQuanLyNhanVien = tk.Button(self, text="Quản lý", **btn_style, command=self.btnQuanLyNhanVien_Click) 
        self.btnQuanLyNhanVien.place(x=451, y=77, width=167, height=74)

        self.btnDanhSachSanPham = tk.Button(self, text="Danh Sách sản phẩm", **btn_style, command=self.btnDanhSachSanPham_Click)
        self.btnDanhSachSanPham.place(x=624, y=77, width=167, height=74)

        self.btnKiemTraKho = tk.Button(self, text="Kiểm tra kho", **btn_style, command=self.btnKiemTraKho_Click)
        self.btnKiemTraKho.place(x=105, y=157, width=167, height=74)

        self.btnKiemTraHoaDon = tk.Button(self, text="Kiểm tra Hóa Đơn", **btn_style, command=self.btnKiemTraHoaDon_Click)
        self.btnKiemTraHoaDon.place(x=278, y=157, width=167, height=74)

        self.btnKhachThanhVien = tk.Button(self, text="Khách Thành Viên", **btn_style, command=self.btnKhachThanhVien_Click)
        self.btnKhachThanhVien.place(x=451, y=157, width=167, height=74)

        self.btnThoat = tk.Button(self, text="Thoát", **btn_style, command=self.button7_Click)
        self.btnThoat.place(x=624, y=157, width=167, height=74)

    def Form2_Load(self):
        chucVu = ""
        queryCHUCVU = "SELECT CHUCVU FROM NhanVien WHERE MANV= ?"
        
        try:
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            cursor.execute(queryCHUCVU, (SharedVariables.MaNV,))
            row = cursor.fetchone()
            
            if row:
                chucVu = row[0].strip()
                self.label2.config(text="chức vụ của bạn: " + chucVu)
            conn.close()
        except Exception as ex:
            # Nếu lỗi kết nối thì thôi, không làm gì để tránh crash lúc load
            print(f"Lỗi load chức vụ: {ex}")

        # Phân quyền
        if chucVu == "Quản lý" or chucVu == "Quản Lý": # Python phân biệt hoa thường nên check cả 2 (để phòng)
            self.btnQuanLyNhanVien['state'] = 'normal'
        else:
            self.btnQuanLyNhanVien['state'] = 'disabled'

    #gọi form khác
    def btnBanHang_Click(self):
        try:
            from formBanHang import Form3
            self.withdraw()
            f = Form3(self)
            f.wait_window()
            self.deiconify()
        except Exception as ex: messagebox.showerror("Lỗi", str(ex))

    def btnKiemTraKho_Click(self):
        try:
            from formQuanLyKho import formQuanLyKho
            self.withdraw()
            f = formQuanLyKho(self)
            f.wait_window()
            self.deiconify()
        except Exception as ex: messagebox.showerror("Lỗi", str(ex))

    def btnNhapNguyenLieu_Click(self):
        try:
            from formNhapNguyenLieu import formNhapNguyenLieu
            self.withdraw()
            f = formNhapNguyenLieu(self)
            f.wait_window()
            self.deiconify()
        except Exception as ex: messagebox.showerror("Lỗi", str(ex))

    def btnKiemTraHoaDon_Click(self):
        try:
            from formQuanLyHoaDon import formQuanLyHoaDon
            self.withdraw()
            f = formQuanLyHoaDon(self)
            f.wait_window()
            self.deiconify()
        except Exception as ex: messagebox.showerror("Lỗi", str(ex))

    def btnKhachThanhVien_Click(self):
        try:
            from formKhachThanhVien import formKhachThanhVien
            self.withdraw()
            f = formKhachThanhVien(self)
            f.wait_window()
            self.deiconify()
        except Exception as ex: messagebox.showerror("Lỗi", str(ex))

    def btnQuanLyNhanVien_Click(self):
        try:
            from formQuanLyNhanVien import formQuanLyNhanVien
            self.withdraw()
            f = formQuanLyNhanVien(self)
            f.wait_window()
            self.deiconify()
        except Exception as ex: messagebox.showerror("Lỗi", str(ex))

    def btnDanhSachSanPham_Click(self):
        try:
            from formSanPham import formSanPham
            self.withdraw()
            f = formSanPham(self)
            f.wait_window()
            self.deiconify()
        except Exception as ex: messagebox.showerror("Lỗi", str(ex))

    def button7_Click(self):
        self.destroy()