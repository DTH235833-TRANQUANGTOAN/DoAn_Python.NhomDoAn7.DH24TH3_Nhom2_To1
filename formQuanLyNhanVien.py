# formQuanLyNhanVien.py
import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime
from DuLieuChung import SharedVariables

class formQuanLyNhanVien(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.InitializeComponent()
        self.formQuanLyNhanVien_Load()

    def InitializeComponent(self):
        self.title("QuanLyNhanVien")
        SharedVariables.set_icon(self)
        self.geometry("1156x720") # Tăng chiều cao để chứa vùng nhập liệu

        # Label Title
        self.label1 = tk.Label(self, text="NHÂN VIÊN", font=("Segoe UI", 25))
        self.label1.place(x=50, y=3)

        # Buttons
        self.btnReset = tk.Button(self, text="Reset", width=20, height=2, command=self.btnReset_Click)
        self.btnReset.place(x=407, y=22)

        self.btnCapNhat = tk.Button(self, text="Cập nhật danh sách", width=20, height=2, command=self.btnCapNhat_Click)
        self.btnCapNhat.place(x=656, y=20)

        self.btnThoat = tk.Button(self, text="Thoát", width=20, height=2, command=self.btnThoat_Click)
        self.btnThoat.place(x=905, y=20)

        # GridNhanVien (Treeview)
        cols = ("MaNV", "HoTen", "NgaySinh", "GioiTinh", "DiaChi", "SDT", "ChucVu", "TaiKhoan", "MatKhau", "TrangThai")
        self.GridNhanVien = ttk.Treeview(self, columns=cols, show='headings')
        
        self.GridNhanVien.heading("MaNV", text="Mã nhân viên")
        self.GridNhanVien.heading("HoTen", text="Họ tên")
        self.GridNhanVien.heading("NgaySinh", text="Ngày sinh")
        self.GridNhanVien.heading("GioiTinh", text="Giới tính")
        self.GridNhanVien.heading("DiaChi", text="Địa chỉ")
        self.GridNhanVien.heading("SDT", text="Số điện thoại")
        self.GridNhanVien.heading("ChucVu", text="Chức vụ")
        self.GridNhanVien.heading("TaiKhoan", text="Tài khoản")
        self.GridNhanVien.heading("MatKhau", text="Mật khẩu")
        self.GridNhanVien.heading("TrangThai", text="Trạng thái")

        # Set width nhỏ lại xíu để vừa màn hình
        self.GridNhanVien.column("MaNV", width=80); self.GridNhanVien.column("HoTen", width=150)
        self.GridNhanVien.column("NgaySinh", width=100); self.GridNhanVien.column("GioiTinh", width=60)
        self.GridNhanVien.column("DiaChi", width=150); self.GridNhanVien.column("SDT", width=100)
        self.GridNhanVien.column("ChucVu", width=100); self.GridNhanVien.column("TaiKhoan", width=100)
        self.GridNhanVien.column("MatKhau", width=100); self.GridNhanVien.column("TrangThai", width=100)

        self.GridNhanVien.place(x=12, y=99, width=1132, height=320)
        self.GridNhanVien.bind("<<TreeviewSelect>>", self.on_row_select)

        # --- Vùng Nhập Liệu (Thay thế Editing Control của GridView) ---
        edit_frame = tk.LabelFrame(self, text="Chi tiết nhân viên (Sửa/Thêm)")
        edit_frame.place(x=12, y=430, width=1132, height=250)

        # Tạo các ô nhập liệu
        tk.Label(edit_frame, text="Mã NV:").grid(row=0, column=0, padx=5, pady=5)
        self.txtMaNV = tk.Entry(edit_frame); self.txtMaNV.grid(row=0, column=1)

        tk.Label(edit_frame, text="Họ Tên:").grid(row=0, column=2, padx=5)
        self.txtHoTen = tk.Entry(edit_frame, width=30); self.txtHoTen.grid(row=0, column=3)

        tk.Label(edit_frame, text="Ngày Sinh:").grid(row=0, column=4, padx=5)
        self.txtNgaySinh = tk.Entry(edit_frame); self.txtNgaySinh.grid(row=0, column=5) # dd/mm/yyyy

        tk.Label(edit_frame, text="Giới Tính:").grid(row=1, column=0, padx=5, pady=5)
        self.txtGioiTinh = ttk.Combobox(edit_frame, values=["Nam", "Nữ"], width=17); self.txtGioiTinh.grid(row=1, column=1)

        tk.Label(edit_frame, text="Địa Chỉ:").grid(row=1, column=2, padx=5)
        self.txtDiaChi = tk.Entry(edit_frame, width=30); self.txtDiaChi.grid(row=1, column=3)

        tk.Label(edit_frame, text="SĐT:").grid(row=1, column=4, padx=5)
        self.txtSDT = tk.Entry(edit_frame); self.txtSDT.grid(row=1, column=5)

        tk.Label(edit_frame, text="Chức Vụ:").grid(row=2, column=0, padx=5, pady=5)
        self.txtChucVu = ttk.Combobox(edit_frame, values=["Quản Lý", "Nhân Viên"], width=17); self.txtChucVu.grid(row=2, column=1)

        tk.Label(edit_frame, text="Tài Khoản:").grid(row=2, column=2, padx=5)
        self.txtTaiKhoan = tk.Entry(edit_frame, width=30); self.txtTaiKhoan.grid(row=2, column=3)

        tk.Label(edit_frame, text="Mật Khẩu:").grid(row=2, column=4, padx=5)
        self.txtMatKhau = tk.Entry(edit_frame); self.txtMatKhau.grid(row=2, column=5)

        tk.Label(edit_frame, text="Trạng Thái:").grid(row=3, column=0, padx=5, pady=5)
        self.txtTrangThai = tk.Entry(edit_frame); self.txtTrangThai.grid(row=3, column=1)

        # Nút thao tác cục bộ trên Grid
        btn_frame = tk.Frame(edit_frame)
        btn_frame.grid(row=4, column=0, columnspan=6, pady=10)
        
        tk.Button(btn_frame, text="Lưu vào bảng (Tạm)", command=self.update_grid_row, bg="lightblue", width=20).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Thêm dòng mới", command=self.add_new_row, bg="lightgreen", width=20).pack(side=tk.LEFT, padx=10)
        tk.Label(btn_frame, text="(Sửa xong nhớ bấm 'Cập nhật danh sách' ở trên để lưu DB)", fg="red").pack(side=tk.LEFT)

    def formQuanLyNhanVien_Load(self):
        self.NapDuLieu()

    def NapDuLieu(self):
        query = "SELECT * FROM NhanVien"
        try:
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            cursor.execute(query)
            
            self.GridNhanVien.delete(*self.GridNhanVien.get_children())
            
            for row in cursor.fetchall():
                ns_str = ""
                if row[2]:
                    ns_str = row[2].strftime("%d/%m/%Y")
                # Map columns: MANV, HOTEN, NGAYSINH, GIOITINH, DIACHI, SDT, CHUCVU, TAIKHOAN, MATKHAU, TRANGTHAI
                self.GridNhanVien.insert("", tk.END, values=(row[0], row[1], ns_str, row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
            
            conn.close()
        except Exception as ex:
            messagebox.showerror("Lỗi", "Lỗi kết nối CSDL: " + str(ex))

    def on_row_select(self, event):
        # Đổ dữ liệu từ dòng chọn xuống ô nhập
        selected = self.GridNhanVien.selection()
        if selected:
            vals = self.GridNhanVien.item(selected[0])['values']
            self.txtMaNV.delete(0, tk.END); self.txtMaNV.insert(0, vals[0])
            self.txtHoTen.delete(0, tk.END); self.txtHoTen.insert(0, vals[1])
            self.txtNgaySinh.delete(0, tk.END); self.txtNgaySinh.insert(0, vals[2])
            self.txtGioiTinh.set(vals[3])
            self.txtDiaChi.delete(0, tk.END); self.txtDiaChi.insert(0, vals[4])
            self.txtSDT.delete(0, tk.END); self.txtSDT.insert(0, vals[5])
            self.txtChucVu.set(vals[6])
            self.txtTaiKhoan.delete(0, tk.END); self.txtTaiKhoan.insert(0, vals[7])
            self.txtMatKhau.delete(0, tk.END); self.txtMatKhau.insert(0, vals[8])
            self.txtTrangThai.delete(0, tk.END); self.txtTrangThai.insert(0, vals[9])

    def get_input_values(self):
        return (
            self.txtMaNV.get(), self.txtHoTen.get(), self.txtNgaySinh.get(),
            self.txtGioiTinh.get(), self.txtDiaChi.get(), self.txtSDT.get(),
            self.txtChucVu.get(), self.txtTaiKhoan.get(), self.txtMatKhau.get(),
            self.txtTrangThai.get()
        )

    def update_grid_row(self):
        selected = self.GridNhanVien.selection()
        if selected:
            self.GridNhanVien.item(selected[0], values=self.get_input_values())
        else:
            messagebox.showwarning("Chú ý", "Chưa chọn dòng để sửa")

    def add_new_row(self):
        self.GridNhanVien.insert("", tk.END, values=self.get_input_values())

    def btnCapNhat_Click(self):
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn cập nhật dữ liệu nhân viên không?")
        if confirm:
            self.CapNhatDuLieu()

    def CapNhatDuLieu(self):
        try:
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            
            for item in self.GridNhanVien.get_children():
                vals = self.GridNhanVien.item(item)['values']
                
                # Kiểm tra null (giả lập logic đếm cell null)
                if not vals[0] or not vals[1]: # Check cơ bản MaNV, TenNV
                    messagebox.showerror("Lỗi", "Dữ liệu nhân viên không được để trống!")
                    return

                manv = str(vals[0])
                hoten = str(vals[1])
                ngaysinh_str = str(vals[2])
                gioitinh = str(vals[3])
                diachi = str(vals[4])
                sdt = str(vals[5])
                chucvu = str(vals[6])
                taikhoan = str(vals[7])
                matkhau = str(vals[8])
                trangthai = str(vals[9])

                # Parse Date
                ngaysinh = None
                try:
                    ngaysinh = datetime.strptime(ngaysinh_str, "%d/%m/%Y")
                except: pass

                # Check Exist
                cursor.execute("SELECT COUNT(*) FROM NhanVien WHERE MANV = ?", (manv,))
                count = cursor.fetchone()[0]

                if count == 0:
                    # INSERT
                    sql = """INSERT INTO NhanVien (MANV, HOTEN, NGAYSINH, GIOITINH, DIACHI, SDT, CHUCVU, TAIKHOAN, MATKHAU, TRANGTHAI)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                    cursor.execute(sql, (manv, hoten, ngaysinh, gioitinh, diachi, sdt, chucvu, taikhoan, matkhau, trangthai))
                else:
                    # UPDATE
                    sql = """UPDATE NhanVien
                             SET HOTEN=?, NGAYSINH=?, GIOITINH=?, DIACHI=?, SDT=?, CHUCVU=?, TAIKHOAN=?, MATKHAU=?, TRANGTHAI=?
                             WHERE MANV=?"""
                    cursor.execute(sql, (hoten, ngaysinh, gioitinh, diachi, sdt, chucvu, taikhoan, matkhau, trangthai, manv))

            conn.commit()
            conn.close()
            messagebox.showinfo("Thông báo", "Cập nhật dữ liệu nhân viên thành công!")
            
        except Exception as ex:
            messagebox.showerror("Lỗi", "Lỗi cập nhật DB: " + str(ex))

    def btnReset_Click(self):
        self.NapDuLieu()

    def btnThoat_Click(self):
        self.destroy()