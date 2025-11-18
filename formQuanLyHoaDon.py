import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime
from DuLieuChung import SharedVariables

class formQuanLyHoaDon(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.InitializeComponent()
        self.formQuanLyHoaDon_Load()

    def InitializeComponent(self):
        self.title("Quản Lý Hóa Đơn")
        self.geometry("1156x700") 
        SharedVariables.set_icon(self)

        self.label1 = tk.Label(self, text="DANH SÁCH HÓA ĐƠN", font=("Segoe UI", 20, "bold"), fg="blue")
        self.label1.place(x=35, y=10)

        # Buttons
        self.btnXoa = tk.Button(self, text="Xóa hóa đơn", width=15, command=self.btnXoa_Click)
        self.btnXoa.place(x=500, y=21)

        self.btnThongKe = tk.Button(self, text="Thống kê DT", width=15, command=self.btnThongKe_Click, bg="lightyellow")
        self.btnThongKe.place(x=650, y=21)

        self.btnThoat = tk.Button(self, text="Thoát", width=15, command=self.btnThoat_Click)
        self.btnThoat.place(x=890, y=21)

        # GridHoaDon (Treeview)
        cols = ("MaHD", "NgayLap", "MaNV", "MaKH", "TongTien")
        self.GridHoaDon = ttk.Treeview(self, columns=cols, show='headings', height=8)
        
        self.GridHoaDon.heading("MaHD", text="Mã hóa đơn")
        self.GridHoaDon.heading("NgayLap", text="Ngày lập")
        self.GridHoaDon.heading("MaNV", text="Mã nhân viên")
        self.GridHoaDon.heading("MaKH", text="Mã khách hàng")
        self.GridHoaDon.heading("TongTien", text="Tổng tiền")

        self.GridHoaDon.column("MaHD", width=100)
        self.GridHoaDon.column("NgayLap", width=200)
        self.GridHoaDon.column("MaNV", width=100)
        self.GridHoaDon.column("MaKH", width=150)
        self.GridHoaDon.column("TongTien", width=200)

        self.GridHoaDon.place(x=12, y=70, width=1132, height=250)
        
        # BIND EVENT: Khi chọn dòng ở bảng trên -> Load bảng dưới
        self.GridHoaDon.bind("<<TreeviewSelect>>", self.on_invoice_select)

        tk.Label(self, text="CHI TIẾT HÓA ĐƠN", font=("Segoe UI", 16, "bold"), fg="green").place(x=35, y=340)

        # GridChiTiet (Treeview)
        cols_ct = ("TenSP", "SoLuong", "DonGia", "ThanhTien")
        self.GridChiTiet = ttk.Treeview(self, columns=cols_ct, show='headings', height=8)
        
        self.GridChiTiet.heading("TenSP", text="Tên Sản Phẩm")
        self.GridChiTiet.heading("SoLuong", text="Số Lượng")
        self.GridChiTiet.heading("DonGia", text="Đơn Giá")
        self.GridChiTiet.heading("ThanhTien", text="Thành Tiền")

        self.GridChiTiet.column("TenSP", width=400)
        self.GridChiTiet.column("SoLuong", width=100)
        self.GridChiTiet.column("DonGia", width=200)
        self.GridChiTiet.column("ThanhTien", width=200)

        self.GridChiTiet.place(x=12, y=380, width=1132, height=250)

    def formQuanLyHoaDon_Load(self):
        self.XemQuyen()
        self.NapDuLieu()

    def XemQuyen(self):
        query = "SELECT CHUCVU FROM NhanVien WHERE MANV= ?"
        try:
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            cursor.execute(query, (SharedVariables.MaNV,))
            row = cursor.fetchone()
            if row:
                chucVu = row[0].strip()
                if chucVu.lower() != "quản lý": 
                    self.btnXoa['state'] = 'disabled'
            conn.close()
        except Exception as ex: pass

    def NapDuLieu(self):
        query = "SELECT * FROM HoaDon ORDER BY NGAYLAP DESC"
        try:
            self.GridHoaDon.delete(*self.GridHoaDon.get_children())
            self.GridChiTiet.delete(*self.GridChiTiet.get_children()) 
            
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            cursor.execute(query)
            for row in cursor.fetchall():
                
                # row[1] là NGAYLAP 
                ngayLap = ""
                if row[1]:
                     try: ngayLap = row[1].strftime("%d/%m/%Y")
                     except: ngayLap = str(row[1])
                
                # row[4] là TONGTIEN
                tongTien = f"{row[4]:,.0f}" if row[4] else "0"

                self.GridHoaDon.insert("", tk.END, values=(row[0], ngayLap, row[2], row[3], tongTien))
                
            conn.close()
        except Exception as ex:
            messagebox.showerror("Lỗi", "Lỗi tải dữ liệu: " + str(ex))
    # --- LOGIC HIỂN THỊ CHI TIẾT ---
    def on_invoice_select(self, event):
        # Lấy dòng đang chọn
        selected = self.GridHoaDon.selection()
        if not selected: return
        
        # Lấy MaHD (cột đầu tiên)
        item = self.GridHoaDon.item(selected[0])
        maHD = item['values'][0]
        
        self.LoadChiTiet(maHD)

    def LoadChiTiet(self, maHD):
        # Query JOIN để lấy Tên SP thay vì Mã SP
        query = """
        SELECT B.TENSP, A.SOLUONG, A.DONGIA, A.THANHTIEN 
        FROM ChiTietHoaDon A 
        JOIN SanPham B ON A.MASP = B.MASP 
        WHERE A.MAHD = ?
        """
        try:
            self.GridChiTiet.delete(*self.GridChiTiet.get_children())
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            cursor.execute(query, (maHD,))
            
            for row in cursor.fetchall():
                # row[0]=TenSP, row[1]=SoLuong, row[2]=DonGia, row[3]=ThanhTien
                dg = f"{row[2]:,.0f}" if row[2] else "0"
                tt = f"{row[3]:,.0f}" if row[3] else "0"
                
                self.GridChiTiet.insert("", tk.END, values=(row[0], row[1], dg, tt))
            
            conn.close()
        except Exception as ex:
            print("Lỗi tải chi tiết: " + str(ex))

    def btnXoa_Click(self):
        selected = self.GridHoaDon.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn hóa đơn cần xóa")
            return
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa hóa đơn này không?")
        if not confirm: return
        item = self.GridHoaDon.item(selected[0])
        maHD = item['values'][0]
        self.XoaHoaDon(maHD)

    def XoaHoaDon(self, maHD):
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

    def btnThongKe_Click(self):
        self.hien_thi_popup_thong_ke()

    def hien_thi_popup_thong_ke(self):
        top = tk.Toplevel(self)
        top.title("Thống Kê Doanh Thu")
        top.geometry("400x300")
        SharedVariables.set_icon(top)
        
        tk.Label(top, text="Chọn kiểu thống kê:", font=("Arial", 12, "bold")).pack(pady=10)
        self.var_mode = tk.StringVar(value="Tháng")

        frame_opt = tk.Frame(top); frame_opt.pack()
        tk.Radiobutton(frame_opt, text="Theo Ngày", variable=self.var_mode, value="Ngày", command=lambda: self.update_inputs(frame_input)).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(frame_opt, text="Theo Tháng", variable=self.var_mode, value="Tháng", command=lambda: self.update_inputs(frame_input)).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(frame_opt, text="Theo Năm", variable=self.var_mode, value="Năm", command=lambda: self.update_inputs(frame_input)).pack(side=tk.LEFT, padx=10)

        frame_input = tk.Frame(top); frame_input.pack(pady=15)
        self.lbl_ketqua = tk.Label(top, text="Doanh thu: 0 VNĐ", font=("Arial", 14, "bold"), fg="red"); self.lbl_ketqua.pack(pady=20)

        self.cbo_day = ttk.Combobox(frame_input, width=5, values=[str(i) for i in range(1, 32)])
        self.cbo_month = ttk.Combobox(frame_input, width=5, values=[str(i) for i in range(1, 13)])
        self.cbo_year = ttk.Combobox(frame_input, width=8, values=[str(i) for i in range(2020, 2030)])
        
        tk.Button(top, text="Xem Doanh Thu", bg="lightblue", command=self.tinh_doanh_thu).pack()
        self.update_inputs(frame_input)
        now = datetime.now()
        self.cbo_day.set(now.day); self.cbo_month.set(now.month); self.cbo_year.set(now.year)

    def update_inputs(self, parent_frame):
        mode = self.var_mode.get()
        for widget in parent_frame.winfo_children(): widget.pack_forget()
        if mode == "Ngày":
            tk.Label(parent_frame, text="Ngày:").pack(side=tk.LEFT); self.cbo_day.pack(side=tk.LEFT)
            tk.Label(parent_frame, text="Tháng:").pack(side=tk.LEFT); self.cbo_month.pack(side=tk.LEFT)
            tk.Label(parent_frame, text="Năm:").pack(side=tk.LEFT); self.cbo_year.pack(side=tk.LEFT)
        elif mode == "Tháng":
            tk.Label(parent_frame, text="Tháng:").pack(side=tk.LEFT); self.cbo_month.pack(side=tk.LEFT)
            tk.Label(parent_frame, text="Năm:").pack(side=tk.LEFT); self.cbo_year.pack(side=tk.LEFT)
        elif mode == "Năm":
            tk.Label(parent_frame, text="Năm:").pack(side=tk.LEFT); self.cbo_year.pack(side=tk.LEFT)

    def tinh_doanh_thu(self):
        mode = self.var_mode.get()
        try:
            d, m, y = self.cbo_day.get(), self.cbo_month.get(), self.cbo_year.get()
            conn = pyodbc.connect(SharedVariables.connectionString); cursor = conn.cursor()
            sql = ""
            params = ()
            if mode == "Ngày": sql = "SELECT SUM(TONGTIEN) FROM HoaDon WHERE DAY(NGAYLAP)=? AND MONTH(NGAYLAP)=? AND YEAR(NGAYLAP)=?"; params = (d, m, y)
            elif mode == "Tháng": sql = "SELECT SUM(TONGTIEN) FROM HoaDon WHERE MONTH(NGAYLAP)=? AND YEAR(NGAYLAP)=?"; params = (m, y)
            elif mode == "Năm": sql = "SELECT SUM(TONGTIEN) FROM HoaDon WHERE YEAR(NGAYLAP)=?"; params = (y,)
            
            cursor.execute(sql, params)
            row = cursor.fetchone()
            total = float(row[0]) if row and row[0] else 0
            self.lbl_ketqua.config(text=f"Doanh thu: {total:,.0f} VNĐ")
            conn.close()
        except Exception as ex: messagebox.showerror("Lỗi", str(ex))

    def btnThoat_Click(self):
        self.destroy()