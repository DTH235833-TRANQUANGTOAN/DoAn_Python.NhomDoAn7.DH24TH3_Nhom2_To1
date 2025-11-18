import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from DuLieuChung import SharedVariables

class formSanPham(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        # List lưu trữ mapping giữa Tên DM (hiển thị) và Mã DM (giá trị)
        # Cấu trúc: [{"id": "DM01", "name": "Cafe"}, ...] 
        self.categories_data = [] 
        
        self.InitializeComponent()
        self.formSanPham_Load()

    def InitializeComponent(self):
        self.title("formSanPham")
        SharedVariables.set_icon(self)
        self.geometry("1170x520")

        # Label Title
        self.label1 = tk.Label(self, text="SẢN PHẨM", font=("Segoe UI", 25))
        self.label1.place(x=50, y=8)

        # Inputs
        tk.Label(self, text="Danh mục:").place(x=56, y=90)
        self.cboDanhMuc = ttk.Combobox(self, width=30, state="readonly")
        self.cboDanhMuc.place(x=259, y=90)
        # Bind event chọn danh mục
        self.cboDanhMuc.bind("<<ComboboxSelected>>", self.CboDanhMuc_ThayDoiLuaChon)

        tk.Label(self, text="Tên sản phẩm:").place(x=56, y=139)
        self.txtTen = tk.Entry(self, width=30)
        self.txtTen.place(x=259, y=136)

        tk.Label(self, text="Giá bán:").place(x=56, y=188)
        self.txtGiaBan = tk.Entry(self, width=30)
        self.txtGiaBan.place(x=259, y=181)

        # GroupBox Trạng thái (Radio Buttons)
        self.gr1 = tk.LabelFrame(self, text="Trạng thái")
        self.gr1.place(x=574, y=90, width=326, height=100)
        
        self.var_status = tk.StringVar(value="Còn bán") # Default value
        self.rdoCon = tk.Radiobutton(self.gr1, text="Còn bán", variable=self.var_status, value="Còn bán")
        self.rdoCon.place(x=23, y=30)
        
        self.rdoHet = tk.Radiobutton(self.gr1, text="Hết", variable=self.var_status, value="Ngừng bán")
        self.rdoHet.place(x=207, y=30)

        # Buttons
        self.btnThem = tk.Button(self, text="Thêm sản phẩm", width=20, height=2, command=self.btnThem_Click)
        self.btnThem.place(x=919, y=24)

        self.btnCapNhat = tk.Button(self, text="Cập nhật sản phẩm", width=20, height=2, command=self.btnCapNhat_Click)
        self.btnCapNhat.place(x=670, y=24)
        
        self.btnHuy = tk.Button(self, text="Hủy (Reset)", width=20, height=2, command=self.btnHuy_Click)
        self.btnHuy.place(x=919, y=95)

        self.btnThoat = tk.Button(self, text="Thoát", width=20, height=2, command=self.btnThoat_Click)
        self.btnThoat.place(x=919, y=167)

        # GridSanPham (Treeview)
        cols = ("MASP", "TENSP", "GIABAN", "MADM", "TRANGTHAI")
        self.GridSanPham = ttk.Treeview(self, columns=cols, show='headings')
        
        self.GridSanPham.heading("MASP", text="Mã SP")
        self.GridSanPham.heading("TENSP", text="Tên SP")
        self.GridSanPham.heading("GIABAN", text="Giá Bán")
        self.GridSanPham.heading("MADM", text="Mã danh mục")
        self.GridSanPham.heading("TRANGTHAI", text="Trạng Thái")

        self.GridSanPham.column("MASP", width=150)
        self.GridSanPham.column("TENSP", width=300)
        self.GridSanPham.column("GIABAN", width=200) # Rộng hơn xíu để hiển thị số tiền
        self.GridSanPham.column("MADM", width=150)
        self.GridSanPham.column("TRANGTHAI", width=200)

        self.GridSanPham.place(x=12, y=242, width=1150, height=253)
        
        # Bind sự kiện chọn dòng
        self.GridSanPham.bind("<<TreeviewSelect>>", self.GridSanPham_CellClick)
        # Bind click vùng trống để bỏ chọn
        self.GridSanPham.bind("<Button-1>", self.check_empty_click)

    def formSanPham_Load(self):
        self.btnCapNhat['state'] = 'disabled'
        self.btnThem['state'] = 'normal'
        self.SetDanhMuc()
        # Mặc định chọn danh mục đầu tiên nếu có
        if self.categories_data:
            self.cboDanhMuc.current(0)
            self.NapDuLieu()

    def SetDanhMuc(self):
        query = "SELECT * FROM DANHMUC"
        self.categories_data = []
        try:
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            cursor.execute(query)
            for row in cursor.fetchall():
                # row[0]: MADM, row[1]: TENDANHMUC
                self.categories_data.append({"id": row[0], "name": row[1]})
            
            # Set values hiển thị cho ComboBox
            display_names = [item["name"] for item in self.categories_data]
            self.cboDanhMuc['values'] = display_names
            
            conn.close()
        except Exception as ex:
            messagebox.showerror("Lỗi", "Lỗi load danh mục: " + str(ex))

    def get_selected_madm(self): 
        # Helper: Lấy MADM từ tên đang chọn trong ComboBox
        selected_name = self.cboDanhMuc.get()
        for item in self.categories_data:
            if item["name"] == selected_name:
                return item["id"]
        return None

    def NapDuLieu(self): # Nạp dữ liệu sản phẩm theo danh mục đã chọn
        madm = self.get_selected_madm()
        if not madm: return

        query = "SELECT * FROM SANPHAM WHERE MADM = ?"
        try:
            self.GridSanPham.delete(*self.GridSanPham.get_children())
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            cursor.execute(query, (madm,))
            
            for row in cursor.fetchall():
                # row indices: 0=MASP, 1=TENSP, 2=GIABAN, 3=MADM, 4=TRANGTHAI (Check DB thực tế)
                # Format Giá bán
                gia = f"{row[2]:,.0f}" if row[2] else "0"
                self.GridSanPham.insert("", tk.END, values=(row[0], row[1], gia, row[3], row[4]))
                
            conn.close()
        except Exception as ex:
            messagebox.showerror("Lỗi", "Lỗi kết nối CSDL: " + str(ex))

    def CboDanhMuc_ThayDoiLuaChon(self, event):
        self.NapDuLieu()

    def check_empty_click(self, event):
        # Nếu click vào vùng không có item, Treeview trả về item rỗng
        item = self.GridSanPham.identify_row(event.y)
        if not item:
            self.reset_form_state()

    def reset_form_state(self):
        # Hủy chọn, reset inputs
        if self.GridSanPham.selection():
            self.GridSanPham.selection_remove(self.GridSanPham.selection())
        
        self.txtTen.delete(0, tk.END)
        self.txtGiaBan.delete(0, tk.END)
        self.var_status.set("Còn bán") # Reset radio về mặc định
        
        self.btnThem['state'] = 'normal'
        self.btnCapNhat['state'] = 'disabled'

    def GridSanPham_CellClick(self, event):
        selected = self.GridSanPham.selection()
        if not selected: return

        item = self.GridSanPham.item(selected[0])
        vals = item['values']
        
        # Đổ dữ liệu vào Inputs
        self.txtTen.delete(0, tk.END); self.txtTen.insert(0, vals[1])
        
        # Xử lý giá bán (xóa dấu phẩy để hiển thị raw)
        gia_clean = str(vals[2]).replace(",", "")
        self.txtGiaBan.delete(0, tk.END); self.txtGiaBan.insert(0, gia_clean)

        # Radio Button
        trang_thai = vals[4]
        # Logic check chuỗi "Còn bán" hay "Hết"
        # (C# logic: rdoCon.Checked = true if "Còn bán", else rdoHet)
        if "Còn bán" in str(trang_thai):
            self.var_status.set("Còn bán")
        else:
            self.var_status.set("Hết")

        self.btnThem['state'] = 'disabled'
        self.btnCapNhat['state'] = 'normal'

    def TaoMASP(self):
        masp = "SP001"
        query = "SELECT TOP 1 MASP FROM SANPHAM ORDER BY MASP DESC"
        try:
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            if row:
                last_id = row[0] # VD: SP005
                num = int(last_id[2:]) + 1
                masp = "SP" + f"{num:03d}"
            conn.close()
        except: pass
        return masp

    def btnThem_Click(self):
        self.ThemSanPham()
        self.txtGiaBan.delete(0, tk.END)
        self.txtTen.delete(0, tk.END)

    def ThemSanPham(self):
        masp = self.TaoMASP()
        tensp = self.txtTen.get()
        giaban_str = self.txtGiaBan.get()
        
        # Validate Giá bán
        try:
            giaban = float(giaban_str)
        except:
            messagebox.showerror("Lỗi", "Giá bán không hợp lệ.")
            return

        madm = self.get_selected_madm()
        trangthai = self.var_status.get()

        sql = "INSERT INTO SANPHAM (MASP, TENSP, GIABAN, MADM, TRANGTHAI) VALUES (?, ?, ?, ?, ?)"
        
        try:
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            cursor.execute(sql, (masp, tensp, giaban, madm, trangthai))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Thông báo", "Thêm sản phẩm thành công!")
            self.NapDuLieu()
        except Exception as ex:
            messagebox.showerror("Lỗi", "Lỗi thêm SP: " + str(ex))

    def btnCapNhat_Click(self):
        self.CapNhatSanPham()
        self.txtGiaBan.delete(0, tk.END)
        self.txtTen.delete(0, tk.END)
        self.reset_form_state() # Reset về trạng thái thêm

    def CapNhatSanPham(self): #Cập nhật sản phẩm
        selected = self.GridSanPham.selection()
        if not selected: return # Không có dòng nào được chọn
        
        # Lấy MASP từ dòng đang chọn (không cho sửa MASP)
        masp = self.GridSanPham.item(selected[0])['values'][0]
        
        tensp = self.txtTen.get()
        giaban_str = self.txtGiaBan.get()
        try:
            giaban = float(giaban_str)
        except:
            messagebox.showerror("Lỗi", "Giá bán không hợp lệ.")
            return
            
        madm = self.get_selected_madm()
        trangthai = self.var_status.get()

        sql = "UPDATE SANPHAM SET TENSP=?, GIABAN=?, MADM=?, TRANGTHAI=? WHERE MASP=?"
        
        try:
            conn = pyodbc.connect(SharedVariables.connectionString)
            cursor = conn.cursor()
            cursor.execute(sql, (tensp, giaban, madm, trangthai, masp))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Thông báo", "Cập nhật sản phẩm thành công!")
            self.NapDuLieu()
        except Exception as ex:
            messagebox.showerror("Lỗi", "Lỗi cập nhật SP: " + str(ex))

    def btnHuy_Click(self):
        self.reset_form_state()

    def btnThoat_Click(self):
        self.destroy()