# formQuanLyKho.py
import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from DuLieuChung import SharedVariables

class formQuanLyKho(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.InitializeComponent()
        self.formQuanLyKho_Load()

    def InitializeComponent(self):
        self.title("formQuanLyKho")
        SharedVariables.set_icon(self)
        self.geometry("831x425")

        # Label Title
        self.label1 = tk.Label(self, text="KHO HÀNG", font=("Segoe UI", 25))
        self.label1.place(x=50, y=22)

        # Button Thoat
        self.btnThoat = tk.Button(self, text="Thoát", width=20, height=2, command=self.btnThoat_Click)
        self.btnThoat.place(x=569, y=41)

        # GridKho (Treeview)
        cols = ("MaNL", "TenNL", "DonViTinh", "SoLuong")
        self.GridKho = ttk.Treeview(self, columns=cols, show='headings')
        
        self.GridKho.heading("MaNL", text="Mã nguyên liệu")
        self.GridKho.heading("TenNL", text="Tên nguyên liệu")
        self.GridKho.heading("DonViTinh", text="Đơn vị tính")
        self.GridKho.heading("SoLuong", text="Số lượng")

        self.GridKho.column("MaNL", width=250)
        self.GridKho.column("TenNL", width=250)
        self.GridKho.column("DonViTinh", width=150)
        self.GridKho.column("SoLuong", width=150)

        self.GridKho.place(x=12, y=118, width=800, height=253)

    def formQuanLyKho_Load(self):
        # Trong C# có code set icon, Python bỏ qua
        self.LayThongTinKho()
        # GridKho.ReadOnly = True (Tkinter Treeview mặc định là ReadOnly)

    def LayThongTinKho(self):
        query = "SELECT * FROM TonKho"
        try:
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            cursor.execute(query)
            
            self.GridKho.delete(*self.GridKho.get_children())
            
            for row in cursor.fetchall():
                # Map đúng thứ tự cột: MANGUYENLIEU, TENNGUYENLIEU, DONVITINH, SOLUONGTON
                self.GridKho.insert("", tk.END, values=(row[0], row[1], row[2], row[3]))
            
            conn.close()
        except Exception as ex:
            messagebox.showerror("Lỗi", "Lỗi kết nối cơ sở dữ liệu: " + str(ex))
    def btnThoat_Click(self):
        self.destroy()