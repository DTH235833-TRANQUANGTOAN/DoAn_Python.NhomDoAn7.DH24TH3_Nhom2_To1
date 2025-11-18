import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime
from DuLieuChung import SharedVariables

class formKhachThanhVien(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.InitializeComponent()
        self.formKhachThanhVien_Load()

    def InitializeComponent(self):
        self.title("Khách Thành Viên")
        SharedVariables.set_icon(self)
        self.geometry("1162x650") 

        # Label Title
        tk.Label(self, text="KHÁCH HÀNG", font=("Segoe UI", 25)).place(x=50, y=17)

        # Buttons
        self.btnReset = tk.Button(self, text="Reset", width=20, height=2, command=self.btnReset_Click)
        self.btnReset.place(x=401, y=34)

        self.btnCapNhat = tk.Button(self, text="Cập nhật danh sách", width=20, height=2, command=self.btnCapNhat_Click)
        self.btnCapNhat.place(x=656, y=34)

        self.btnThoat = tk.Button(self, text="Thoát", width=20, height=2, command=self.btnThoat_Click)
        self.btnThoat.place(x=905, y=34)

        # GridKhachHang (Treeview)
        cols = ("MaKH", "HoTen", "NgaySinh", "GioiTinh", "SDT", "DiemTichLuy")
        self.GridKhachHang = ttk.Treeview(self, columns=cols, show='headings')
        
        self.GridKhachHang.heading("MaKH", text="Mã khách hàng")
        self.GridKhachHang.heading("HoTen", text="Tên khách hàng")
        self.GridKhachHang.heading("NgaySinh", text="Ngày sinh")
        self.GridKhachHang.heading("GioiTinh", text="Giới tính")
        self.GridKhachHang.heading("SDT", text="Số điện thoại")
        self.GridKhachHang.heading("DiemTichLuy", text="Điểm tích lũy")

        self.GridKhachHang.column("MaKH", width=150)
        self.GridKhachHang.column("HoTen", width=300)
        self.GridKhachHang.column("NgaySinh", width=150)
        
        self.GridKhachHang.place(x=12, y=113, width=1132, height=320)
        
        # Bind sự kiện chọn dòng
        self.GridKhachHang.bind("<<TreeviewSelect>>", self.on_row_select)

        # --- Vùng Edit 
        edit_frame = tk.LabelFrame(self, text="Thông tin chi tiết (Sửa/Thêm)")
        edit_frame.place(x=12, y=450, width=1132, height=150)

        # Dòng 1
        tk.Label(edit_frame, text="Mã KH:").grid(row=0, column=0, padx=5, pady=5)
        self.txtMaKH = tk.Entry(edit_frame); self.txtMaKH.grid(row=0, column=1)

        tk.Label(edit_frame, text="Họ Tên:").grid(row=0, column=2, padx=5)
        self.txtHoTen = tk.Entry(edit_frame, width=30); self.txtHoTen.grid(row=0, column=3)

        tk.Label(edit_frame, text="Ngày Sinh (dd/MM/yyyy):").grid(row=0, column=4, padx=5)
        self.txtNgaySinh = tk.Entry(edit_frame); self.txtNgaySinh.grid(row=0, column=5)

        # Dòng 2
        tk.Label(edit_frame, text="Giới Tính:").grid(row=1, column=0, padx=5, pady=5)
        self.txtGioiTinh = tk.Entry(edit_frame); self.txtGioiTinh.grid(row=1, column=1)

        tk.Label(edit_frame, text="SĐT:").grid(row=1, column=2, padx=5)
        self.txtSDT = tk.Entry(edit_frame); self.txtSDT.grid(row=1, column=3)

        tk.Label(edit_frame, text="Điểm:").grid(row=1, column=4, padx=5)
        self.txtDiem = tk.Entry(edit_frame); self.txtDiem.grid(row=1, column=5)

        # Nút hỗ trợ cập nhật vào Grid (chưa lưu DB)
        tk.Button(edit_frame, text="Lưu vào bảng (Tạm)", command=self.update_grid_row, bg="lightblue").grid(row=2, column=1, columnspan=2, pady=10)
        tk.Button(edit_frame, text="Thêm mới vào bảng", command=self.add_new_to_grid, bg="lightgreen").grid(row=2, column=3, columnspan=2)
        tk.Label(edit_frame, text="(Sau khi sửa xong bảng, bấm 'Cập nhật danh sách' ở trên để lưu DB)", fg="red").grid(row=2, column=5)

    def formKhachThanhVien_Load(self):
        self.LayThongTinKH()

    def LayThongTinKH(self):
        self.GridKhachHang.delete(*self.GridKhachHang.get_children())
        query = "SELECT * FROM KhachThanhVien"
        try:
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            cursor.execute(query)
            for row in cursor.fetchall():
                # Xử lý ngày sinh
                ns_str = ""
                if row[2]: # row[2] là NGAYSINH
                    ns_str = row[2].strftime("%d/%m/%Y")
                
                self.GridKhachHang.insert("", tk.END, values=(row[0], row[1], ns_str, row[3], row[4], row[5]))
            conn.close()
        except Exception as ex:
            messagebox.showerror("Lỗi", str(ex))

    def on_row_select(self, event):
        selected = self.GridKhachHang.selection()
        if selected:
            vals = self.GridKhachHang.item(selected[0])['values']
            # Đổ dữ liệu xuống các ô text
            self.txtMaKH.delete(0, tk.END); self.txtMaKH.insert(0, vals[0])
            self.txtHoTen.delete(0, tk.END); self.txtHoTen.insert(0, vals[1])
            self.txtNgaySinh.delete(0, tk.END); self.txtNgaySinh.insert(0, vals[2])
            self.txtGioiTinh.delete(0, tk.END); self.txtGioiTinh.insert(0, vals[3])
            self.txtSDT.delete(0, tk.END); self.txtSDT.insert(0, vals[4])
            self.txtDiem.delete(0, tk.END); self.txtDiem.insert(0, vals[5])

    def update_grid_row(self):
        # Cập nhật dòng đang chọn
        selected = self.GridKhachHang.selection()
        if selected:
            self.GridKhachHang.item(selected[0], values=(
                self.txtMaKH.get(), self.txtHoTen.get(), self.txtNgaySinh.get(),
                self.txtGioiTinh.get(), self.txtSDT.get(), self.txtDiem.get()
            ))
        else:
            messagebox.showwarning("Chú ý", "Chưa chọn dòng nào để sửa")

    def add_new_to_grid(self):
        # Thêm dòng mới vào bảng
        self.GridKhachHang.insert("", tk.END, values=(
            self.txtMaKH.get(), self.txtHoTen.get(), self.txtNgaySinh.get(),
            self.txtGioiTinh.get(), self.txtSDT.get(), self.txtDiem.get()
        ))

    def btnCapNhat_Click(self):
        self.CapNhatThongTinKH()

    def CapNhatThongTinKH(self):
        try:
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            
            for item in self.GridKhachHang.get_children():
                vals = self.GridKhachHang.item(item)['values']
                maKH = str(vals[0])
                hoTen = str(vals[1])
                ngaySinhStr = str(vals[2])
                gioiTinh = str(vals[3])
                sdt = str(vals[4])
                diem = int(vals[5]) if vals[5] else 0

                # Parse Date
                ngaySinh = None
                if ngaySinhStr and ngaySinhStr.strip():
                    try:
                        ngaySinh = datetime.strptime(ngaySinhStr, "%d/%m/%Y")
                    except: pass 
                
                # Check exist logic
                cursor.execute("SELECT COUNT(*) FROM KhachThanhVien WHERE MAKH = ?", (maKH,))
                count = cursor.fetchone()[0]

                if count == 0:
                    # Insert
                    sql = "INSERT INTO KhachThanhVien (MAKH, HOTEN, NGAYSINH, GIOITINH, SDT, DIEMTICHLUY) VALUES (?, ?, ?, ?, ?, ?)"
                    cursor.execute(sql, (maKH, hoTen, ngaySinh, gioiTinh, sdt, diem))
                else:
                    # Update
                    sql = "UPDATE KhachThanhVien SET HOTEN=?, NGAYSINH=?, GIOITINH=?, SDT=?, DIEMTICHLUY=? WHERE MAKH=?"
                    cursor.execute(sql, (hoTen, ngaySinh, gioiTinh, sdt, diem, maKH))

            conn.commit()
            conn.close()
            messagebox.showinfo("Thông báo", "Cập nhật thành công!")
        except Exception as ex:
            messagebox.showerror("Lỗi DB", str(ex))

    def btnReset_Click(self):
        self.LayThongTinKH()

    def btnThoat_Click(self):
        self.destroy()