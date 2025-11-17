# formBanHang.py
import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime
from DuLieuChung import SharedVariables

class Form3(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.InitializeComponent()
        
        # Data Tables (Cache dữ liệu để xử lý nhanh như DataTable trong C#)
        self._dtSanPham = [] 
        self._dtKhachHang = []
        
        self.Form3_Load()

    def InitializeComponent(self):
        self.title("Bán Hàng")
        SharedVariables.set_icon(self)
        self.geometry("1156x720")
        
        # --- Labels & Entries Thông tin nhân viên ---
        tk.Label(self, text="Mã nhân viên:").place(x=16, y=75)
        self.txtMaNV = tk.Entry(self, width=25); self.txtMaNV.place(x=188, y=68)
        
        tk.Label(self, text="Tên nhân viên:").place(x=12, y=120)
        self.txtTenNV = tk.Entry(self, width=25); self.txtTenNV.place(x=188, y=117)

        tk.Label(self, text="Chức vụ:").place(x=16, y=165)
        self.txtChucVu = tk.Entry(self, width=25); self.txtChucVu.place(x=188, y=162)

        tk.Label(self, text="BÁN HÀNG", font=("Segoe UI", 15)).place(x=452, y=9)

        # --- Buttons ---
        self.btnTao = tk.Button(self, text="Tạo hóa đơn", width=20, height=2, command=self.btnTao_Click)
        self.btnTao.place(x=784, y=68)

        self.btnReset = tk.Button(self, text="Reset", width=20, height=2, command=self.btnReset_Click)
        self.btnReset.place(x=535, y=147)

        self.btnThoat = tk.Button(self, text="Hủy", width=20, height=2, command=self.btnHuy_Click)
        self.btnThoat.place(x=784, y=147)

        # --- Khu vực Grid (Thay thế DataGridView) ---
        # Vì Tkinter Treeview không sửa trực tiếp được, ta làm vùng nhập liệu giả lập
        input_frame = tk.LabelFrame(self, text="Chọn sản phẩm thêm vào giỏ")
        input_frame.place(x=12, y=218, width=1132, height=80)

        tk.Label(input_frame, text="Sản phẩm:").place(x=10, y=20)
        self.cboSanPham_Input = ttk.Combobox(input_frame, width=35)
        self.cboSanPham_Input.place(x=80, y=20)
        # Event khi chọn SP để cập nhật giá (giống logic Grid1_ThayDoi)
        self.cboSanPham_Input.bind("<<ComboboxSelected>>", self.on_product_select)

        tk.Label(input_frame, text="Số lượng:").place(x=350, y=20)
        self.txtSoLuong_Input = tk.Entry(input_frame, width=10)
        self.txtSoLuong_Input.place(x=420, y=20)
        self.txtSoLuong_Input.bind("<KeyRelease>", self.on_quantity_change) # Tính thành tiền tạm

        tk.Label(input_frame, text="Đơn giá:").place(x=520, y=20)
        self.lblDonGia_Display = tk.Label(input_frame, text="0", fg="blue")
        self.lblDonGia_Display.place(x=580, y=20)

        tk.Button(input_frame, text="Thêm / Cập nhật", command=self.add_to_grid).place(x=700, y=15)
        tk.Button(input_frame, text="Xóa dòng chọn", command=self.remove_from_grid).place(x=820, y=15)

        # Grid1 (Treeview)
        columns = ("TenSP", "SoLuong", "DonGia", "ThanhTien")
        self.Grid1 = ttk.Treeview(self, columns=columns, show='headings', height=10)
        self.Grid1.heading("TenSP", text="Tên Sản Phẩm")
        self.Grid1.heading("SoLuong", text="Số Lượng")
        self.Grid1.heading("DonGia", text="Đơn Giá")
        self.Grid1.heading("ThanhTien", text="Thành Tiền")
        
        self.Grid1.column("TenSP", width=400)
        self.Grid1.column("SoLuong", width=100)
        self.Grid1.column("DonGia", width=300)
        self.Grid1.column("ThanhTien", width=300)
        
        self.Grid1.place(x=12, y=300, width=1132, height=171)

        # --- Footer ---
        tk.Label(self, text="Mã khách hàng").place(x=6, y=506)
        self.cboMaKH = ttk.Combobox(self, width=25)
        self.cboMaKH.place(x=188, y=503)

        tk.Label(self, text="Tổng tiền:").place(x=720, y=491) # Thêm label cho rõ
        self.txtThanhTien = tk.Entry(self, width=25, font=("Arial", 12, "bold"))
        self.txtThanhTien.place(x=822, y=491)

    def Form3_Load(self):
        self.txtMaNV['state'] = 'disabled'
        self.txtTenNV['state'] = 'disabled'
        self.txtChucVu['state'] = 'disabled'
        self.txtThanhTien.insert(0, "0")
        
        self.LayThongTinNV()
        self.LoadSanPhamvaKH()

    def LayThongTinNV(self):
        query = "SELECT MANV, HOTEN, CHUCVU FROM NhanVien WHERE MANV = ?"
        try:
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            cursor.execute(query, (SharedVariables.MaNV,))
            row = cursor.fetchone()
            if row:
                self.txtMaNV['state'] = 'normal'; self.txtMaNV.delete(0, tk.END); self.txtMaNV.insert(0, row[0]); self.txtMaNV['state'] = 'disabled'
                self.txtTenNV['state'] = 'normal'; self.txtTenNV.delete(0, tk.END); self.txtTenNV.insert(0, row[1]); self.txtTenNV['state'] = 'disabled'
                self.txtChucVu['state'] = 'normal'; self.txtChucVu.delete(0, tk.END); self.txtChucVu.insert(0, row[2]); self.txtChucVu['state'] = 'disabled'
            conn.close()
        except Exception as ex:
            print("Lỗi load NV: " + str(ex))

    def LoadSanPhamvaKH(self):
        # Load San Pham
        self._dtSanPham = []
        try:
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            cursor.execute("SELECT MASP, TENSP, GIABAN FROM SanPham ORDER BY TENSP")
            for row in cursor.fetchall():
                self._dtSanPham.append({"MASP": row[0], "TENSP": row[1], "GIABAN": float(row[2])})
            
            # Đổ dữ liệu vào ComboBox Input
            sp_names = [x["TENSP"] for x in self._dtSanPham]
            self.cboSanPham_Input['values'] = sp_names

            # Load Khach Hang
            self._dtKhachHang = [{"MAKH": None, "HOTEN": "-- Khách lẻ --"}]
            cursor.execute("SELECT MAKH, HOTEN FROM KhachThanhVien ORDER BY HOTEN")
            for row in cursor.fetchall():
                self._dtKhachHang.append({"MAKH": row[0], "HOTEN": row[1]})
            
            kh_names = [x["HOTEN"] for x in self._dtKhachHang]
            self.cboMaKH['values'] = kh_names
            self.cboMaKH.current(0)

            conn.close()
        except Exception as ex:
            messagebox.showerror("Lỗi", "Lỗi tải dữ liệu: " + str(ex))

    # --- Logic xử lý Grid (Thay thế Events Grid1_ThayDoi) ---
    def on_product_select(self, event):
        ten_sp = self.cboSanPham_Input.get()
        sp = next((s for s in self._dtSanPham if s["TENSP"] == ten_sp), None)
        if sp:
            self.lblDonGia_Display.config(text=f"{sp['GIABAN']:,.0f}")
            self.txtSoLuong_Input.focus()

    def on_quantity_change(self, event):
        # Chỉ để UX tốt hơn, không bắt buộc
        pass

    def add_to_grid(self):
        ten_sp = self.cboSanPham_Input.get()
        sl_str = self.txtSoLuong_Input.get()
        
        if not ten_sp or not sl_str.isdigit():
            messagebox.showwarning("Lỗi", "Vui lòng chọn SP và nhập số lượng hợp lệ (số nguyên).")
            return
            
        sl = int(sl_str)
        sp = next((s for s in self._dtSanPham if s["TENSP"] == ten_sp), None)
        
        if sp:
            gia = sp['GIABAN']
            thanh_tien = sl * gia
            
            # Kiểm tra trùng (Logic Grid1_ChongChonTrung)
            existing_item = None
            for item in self.Grid1.get_children():
                if self.Grid1.item(item)['values'][0] == ten_sp:
                    existing_item = item
                    break
            
            if existing_item:
                # Nếu trùng thì hỏi update hoặc báo lỗi tùy logic. Ở đây mình update luôn cho tiện
                self.Grid1.item(existing_item, values=(ten_sp, sl, f"{gia:,.0f}", f"{thanh_tien:,.0f}"))
            else:
                self.Grid1.insert("", tk.END, values=(ten_sp, sl, f"{gia:,.0f}", f"{thanh_tien:,.0f}"))
            
            self.CalculateTotal()
            # Reset input
            self.cboSanPham_Input.set("")
            self.txtSoLuong_Input.delete(0, tk.END)
            self.lblDonGia_Display.config(text="0")

    def remove_from_grid(self):
        selected = self.Grid1.selection()
        if selected:
            self.Grid1.delete(selected[0])
            self.CalculateTotal()

    def CalculateTotal(self):
        total = 0
        for item in self.Grid1.get_children():
            tt_str = self.Grid1.item(item)['values'][3]
            tt = float(str(tt_str).replace(",", ""))
            total += tt
        
        self.txtThanhTien.delete(0, tk.END)
        self.txtThanhTien.insert(0, f"{total:,.0f}")

    def btnTao_Click(self):
        self.TaoHoaDon()

    def TaoHoaDon(self):
        # Kiểm tra Grid có dữ liệu không
        if not self.Grid1.get_children():
            messagebox.showerror("Lỗi", "Chưa có sản phẩm nào.")
            return

        maHD = self.TaoMaHD()
        tong_tien_str = self.txtThanhTien.get().replace(",", "")
        tong_tien = float(tong_tien_str) if tong_tien_str else 0
        diemThuong = int(tong_tien / 10000) # Logic TinhDiem

        # Lấy MAKH
        kh_name = self.cboMaKH.get()
        kh_obj = next((k for k in self._dtKhachHang if k["HOTEN"] == kh_name), None)
        ma_kh = kh_obj["MAKH"] if kh_obj else None

        conn = None
        try:
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor() # Mặc định pyodbc dùng transaction, phải commit mới lưu
            
            # 1. Insert HoaDon
            sql_hd = "INSERT INTO HoaDon (MAHD, MANV, MAKH, NGAYLAP, TONGTIEN) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(sql_hd, (maHD, self.txtMaNV.get(), ma_kh, datetime.now(), tong_tien))

            # 2. Insert ChiTiet
            sql_ct = "INSERT INTO ChiTietHoaDon (MAHD, MASP, SOLUONG, DONGIA, THANHTIEN) VALUES (?, ?, ?, ?, ?)"
            
            for item in self.Grid1.get_children():
                vals = self.Grid1.item(item)['values']
                ten_sp = vals[0]
                sl = int(vals[1])
                dg = float(str(vals[2]).replace(",", ""))
                tt = float(str(vals[3]).replace(",", ""))
                
                # Lấy MASP từ tên
                sp_obj = next((s for s in self._dtSanPham if s["TENSP"] == ten_sp), None)
                masp = sp_obj["MASP"]
                
                cursor.execute(sql_ct, (maHD, masp, sl, dg, tt))

            # 3. Update DiemTichLuy
            if ma_kh:
                sql_diem = "UPDATE KhachThanhVien SET DIEMTICHLUY = DIEMTICHLUY + ? WHERE MAKH = ?"
                cursor.execute(sql_diem, (diemThuong, ma_kh))

            conn.commit() # Transaction Commit
            messagebox.showinfo("Thông báo", "Tạo hóa đơn thành công!")
            
            # Reset Form
            self.Grid1.delete(*self.Grid1.get_children())
            self.txtThanhTien.delete(0, tk.END); self.txtThanhTien.insert(0, "0")

        except Exception as ex:
            if conn: conn.rollback() # Rollback nếu lỗi
            messagebox.showerror("Lỗi DB", str(ex))
        finally:
            if conn: conn.close()

    def TaoMaHD(self):
        maHD = "HD001"
        try:
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            cursor.execute("SELECT TOP 1 MAHD FROM HoaDon ORDER BY MAHD DESC")
            row = cursor.fetchone()
            if row:
                last_ma = row[0] # VD: HD005
                num = int(last_ma[2:]) + 1 # Cắt chuỗi từ vị trí 2
                maHD = "HD" + f"{num:03d}" # Format 3 số
            conn.close()
        except: pass
        return maHD

    def btnReset_Click(self):
        self.LayThongTinNV()
        self.Grid1.delete(*self.Grid1.get_children())
        self.txtThanhTien.delete(0, tk.END); self.txtThanhTien.insert(0, "0")

    def btnHuy_Click(self):
        self.destroy()