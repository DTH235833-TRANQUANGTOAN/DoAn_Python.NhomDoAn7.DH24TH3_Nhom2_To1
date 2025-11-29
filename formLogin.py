import tkinter as tk # Thư viện giao diện đồ họa
from tkinter import messagebox # Thư viện hiển thị hộp thoại
import pyodbc # Thư viện kết nối cơ sở dữ liệu
from DuLieuChung import SharedVariables

class Form1(tk.Tk): # Form chính kế thừa từ tk.Tk là cửa sổ gốc main
    def __init__(self):
        super().__init__()
        self.InitializeComponent()
        self.Form1_Load()
        

    def InitializeComponent(self):
        # Cấu hình Form
        self.title("Login")
        SharedVariables.set_icon(self)
        self.geometry("599x299")
        self.resizable(False, False)

        # Label 1: ĐĂNG NHẬP
        self.label1 = tk.Label(self, text="ĐĂNG NHẬP", font=("Segoe UI", 17))
        self.label1.place(x=184, y=9, width=213, height=46)

        # Label 2: Tên đăng nhập
        self.label2 = tk.Label(self, text="Tên đăng nhập", font=("Segoe UI", 12))
        self.label2.place(x=21, y=83, width=174, height=32)

        # txtTenDangNhap
        self.txtTenDangNhap = tk.Entry(self, font=("Segoe UI", 12))
        self.txtTenDangNhap.place(x=218, y=80, width=322, height=39)

        # Label 3: Mật khẩu
        self.label3 = tk.Label(self, text="Mật khẩu", font=("Segoe UI", 12))
        self.label3.place(x=80, y=138, width=115, height=32)

        # txtMatKhau (UseSystemPasswordChar -> show="*")
        self.txtMatKhau = tk.Entry(self, font=("Segoe UI", 12), show="*")
        self.txtMatKhau.place(x=218, y=135, width=322, height=39)

        # btnDangNhap
        self.btnDangNhap = tk.Button(self, text="Đăng nhập", font=("Segoe UI", 12), command=self.btnDangNhap_Click)
        self.btnDangNhap.place(x=73, y=208, width=153, height=63)

        # btnThoat
        self.btnThoat = tk.Button(self, text="Thoát", font=("Segoe UI", 12), command=self.btnThoat_Click)
        self.btnThoat.place(x=365, y=208, width=153, height=63)

    def Vi_TrI_Form(self):
        scceen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (scceen_width / 2) - (599 / 2) # trừ nửa chiều rộng form
        y = (screen_height / 2) - (299 / 2) # trừ nửa chiều cao form
        self.geometry(f'+{int(x)}+{int(y)}')

    def Form1_Load(self):
        self.Vi_TrI_Form()
        pass

    def KiemTraDangNhap(self, taiKhoan, matKhau):
        ketQua = False
        try:
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            
            # Câu lệnh SQL để kiểm tra tài khoản và mật khẩu
            query = "SELECT COUNT(*) FROM NhanVien WHERE TAIKHOAN = ? AND MATKHAU = ?"
            cursor.execute(query, (taiKhoan, matKhau))
            
            count = cursor.fetchone()[0]
            
            if count > 0: # Nếu có bản ghi khớp
                ketQua = True
                # Câu lệnh SQL để lấy thông tin nhân viên
                queryMANV = "SELECT MANV FROM NhanVien WHERE TAIKHOAN = ? AND MATKHAU = ?"
                cursor.execute(queryMANV, (taiKhoan.strip(), matKhau.strip()))
                row = cursor.fetchone()
                if row:
                    SharedVariables.MaNV = str(row[0]) # Lấy giá trị MANV lưu vào biến chung
            
            conn.close()
        except Exception as ex:
            messagebox.showerror("Lỗi", "Lỗi kết nối cơ sở dữ liệu: " + str(ex))
        
        return ketQua

    def btnDangNhap_Click(self):
        taiKhoan = self.txtTenDangNhap.get().strip()
        matKhau = self.txtMatKhau.get().strip()

        if not taiKhoan or not matKhau:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin đăng nhập.")
            return

        if self.KiemTraDangNhap(taiKhoan, matKhau):
            messagebox.showinfo("Thông báo", "Đăng nhập thành công!")
            
            # Logic chuyển Form: Hide Login -> Show ChucNang
            self.withdraw() # Hide form hiện tại
            
            # Import ở đây để tránh lỗi circular import ban đầu
            from formChucNang import formChucNang 
            f2 = formChucNang(self) # Truyền form cha vào để quản lý
            f2.wait_window() # Chờ form con đóng (tương đương ShowDialog)
            
            # Khi formChucNang đóng, code sẽ chạy tiếp ở đây (nếu cần xử lý gì thêm)
            self.destroy() # Đóng luôn Login khi thoát
        else:
            messagebox.showerror("Lỗi đăng nhập", "Tên đăng nhập hoặc mật khẩu không đúng.")

    def btnThoat_Click(self):
        self.destroy()