import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from DuLieuChung import SharedVariables

class formNhapNguyenLieu(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.InitializeComponent()

    def InitializeComponent(self):
        self.title("Nhập Nguyên Liệu")
        SharedVariables.set_icon(self)
        self.geometry("1180x550") 

        # Label Title
        self.label1 = tk.Label(self, text="NHẬP NGUYÊN LIỆU", font=("Segoe UI", 25))
        self.label1.place(x=51, y=9)

        # Buttons
        self.btnNhap = tk.Button(self, text="NHẬP KHO (Lưu)", width=20, height=2, command=self.btnNhap_Click, bg="lightgreen")
        self.btnNhap.place(x=639, y=26)

        self.btnHuy = tk.Button(self, text="Xóa danh sách", width=20, height=2, command=self.btnHuy_Click)
        self.btnHuy.place(x=906, y=82)

        self.btnThoat = tk.Button(self, text="Thoát", width=20, height=2, command=self.btnThoat_Click)
        self.btnThoat.place(x=906, y=26)

        #Vùng Nhập liệu (Thêm dòng vào Grid)
        input_frame = tk.LabelFrame(self, text="Thông tin nguyên liệu nhập")
        input_frame.place(x=17, y=80, width=600, height=150)

        tk.Label(input_frame, text="Mã NL:").grid(row=0, column=0, pady=5)
        self.txtMaNL = tk.Entry(input_frame); self.txtMaNL.grid(row=0, column=1)

        tk.Label(input_frame, text="Tên NL:").grid(row=0, column=2, pady=5)
        self.txtTenNL = tk.Entry(input_frame, width=30); self.txtTenNL.grid(row=0, column=3)

        tk.Label(input_frame, text="Đơn vị:").grid(row=1, column=0, pady=5)
        self.txtDVT = tk.Entry(input_frame); self.txtDVT.grid(row=1, column=1)

        tk.Label(input_frame, text="Số lượng:").grid(row=1, column=2, pady=5)
        self.txtSoLuong = tk.Entry(input_frame); self.txtSoLuong.grid(row=1, column=3)

        tk.Button(input_frame, text="Thêm vào bảng bên dưới", command=self.add_to_grid).grid(row=2, column=1, columnspan=3, pady=10)


        # GridNhap (Treeview)
        cols = ("MaNL", "TenNL", "DonViTinh", "SoLuong")
        self.GridNhap = ttk.Treeview(self, columns=cols, show='headings')
        
        self.GridNhap.heading("MaNL", text="Mã nguyên liệu")
        self.GridNhap.heading("TenNL", text="Tên nguyên liệu")
        self.GridNhap.heading("DonViTinh", text="Đơn vị tính")
        self.GridNhap.heading("SoLuong", text="Số lượng")

        self.GridNhap.column("MaNL", width=250)
        self.GridNhap.column("TenNL", width=350)
        self.GridNhap.column("DonViTinh", width=150)
        self.GridNhap.column("SoLuong", width=150)

        self.GridNhap.place(x=17, y=240, width=1132, height=253)

    def add_to_grid(self):
        # Lấy dữ liệu từ ô nhập
        ma = self.txtMaNL.get().strip()
        ten = self.txtTenNL.get().strip()
        dvt = self.txtDVT.get().strip()
        sl_str = self.txtSoLuong.get().strip()

        if not ma or not ten or not dvt or not sl_str:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return
        
        if not sl_str.isdigit() or int(sl_str) <= 0:
            messagebox.showwarning("Lỗi", "Số lượng phải là số dương")
            return

        # Thêm vào Treeview
        self.GridNhap.insert("", tk.END, values=(ma, ten, dvt, sl_str))
        
        # Clear ô nhập để nhập tiếp
        self.txtMaNL.delete(0, tk.END)
        self.txtTenNL.delete(0, tk.END)
        self.txtDVT.delete(0, tk.END)
        self.txtSoLuong.delete(0, tk.END)
        self.txtMaNL.focus()

    def btnHuy_Click(self):
        # Xóa hết dòng trong Grid
        self.GridNhap.delete(*self.GridNhap.get_children())

    def btnNhap_Click(self):
        self.CapNhatCSDL()

    def CapNhatCSDL(self):
        # Kiểm tra Grid có dữ liệu không
        if not self.GridNhap.get_children():
            messagebox.showwarning("Lỗi", "Danh sách nhập đang trống")
            return

        try:
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            
            # Duyệt từng dòng trong Grid
            for item in self.GridNhap.get_children():
                vals = self.GridNhap.item(item)['values']
                maNL = str(vals[0])
                tenNL = str(vals[1])
                donViTinh = str(vals[2])
                soLuong = int(vals[3])

                # 1. Kiểm tra tồn tại trong kho
                check_sql = "SELECT TENNGUYENLIEU, SOLUONGTON FROM TonKho WHERE MANGUYENLIEU = ? OR TENNGUYENLIEU = ?"
                cursor.execute(check_sql, (maNL, tenNL))
                rows = cursor.fetchall() # Lấy tất cả các dòng khớp

                if len(rows) > 0:
                    # Logic check trùng tên/mã
                    maTenTrung = False
                    # Nếu tìm thấy dòng khớp Mã và Tên (trong DB, row[0] là TENNGUYENLIEU)
                    match_exact = False
                    for r in rows:
                         if r[0] == tenNL: # Tên khớp (và Mã đã khớp hoặc Tên đã khớp do câu Query)
                             match_exact = True
                             break
                    
                    if match_exact:
                         # UPDATE cộng dồn số lượng
                         up_sql = "UPDATE TonKho SET SOLUONGTON = SOLUONGTON + ? WHERE MANGUYENLIEU = ? AND TENNGUYENLIEU = ?"
                         cursor.execute(up_sql, (soLuong, maNL, tenNL))
                    else:
                         # Tồn tại Mã hoặc Tên nhưng không khớp cả hai -> Lỗi
                         raise Exception(f"Dữ liệu không hợp lệ: Mã '{maNL}' hoặc Tên '{tenNL}' bị trùng lệch với dữ liệu kho.")
                else:
                    # INSERT Mới
                    in_sql = "INSERT INTO TonKho (MANGUYENLIEU, TENNGUYENLIEU, DONVITINH, SOLUONGTON) VALUES (?, ?, ?, ?)"
                    cursor.execute(in_sql, (maNL, tenNL, donViTinh, soLuong))

            conn.commit() # Xác nhận transaction
            conn.close()
            
            messagebox.showinfo("Thành công", "Cập nhật kho thành công!")
            self.GridNhap.delete(*self.GridNhap.get_children()) # Clear lưới sau khi nhập xong

        except Exception as ex:
            messagebox.showerror("Lỗi CSDL", str(ex))

    def btnThoat_Click(self):
        self.destroy()