import streamlit as st
import pandas as pd

# 1. Cấu hình trang web (Tiêu đề, icon, giao diện rộng)
st.set_page_config(
    page_title="Công Cụ Đọc Excel",
    page_icon="📊",
    layout="wide"
)

# 2. Tiêu đề ứng dụng
st.title("📂 Ứng Dụng Đọc & Phân Tích Excel")
st.markdown("---")

# 3. Khung upload file (Sidebar bên trái)
with st.sidebar:
    st.header("1. Nhập Dữ Liệu")
    uploaded_file = st.file_uploader("Chọn file Excel (.xlsx)", type=["xlsx", "xls"])
    st.info("Mẹo: File không nên có dòng trống ở đầu.")

# 4. Xử lý logic chính
if uploaded_file is not None:
    try:
        # Đọc file Excel vào DataFrame
        df = pd.read_excel(uploaded_file)
        
        # --- PHẦN THỐNG KÊ TỔNG QUAN ---
        col1, col2, col3 = st.columns(3)
        col1.metric("Tổng Số Dòng", len(df))
        col2.metric("Tổng Số Cột", len(df.columns))
        col3.metric("Tên File", uploaded_file.name)
        
        st.markdown("---")
        
        # --- PHẦN HIỂN THỊ DỮ LIỆU ---
        st.subheader("2. Dữ Liệu Chi Tiết")
        
        # Tạo bộ lọc nhanh (Ví dụ lọc theo cột đầu tiên)
        first_col = df.columns[0]
        unique_values = df[first_col].unique().tolist()
        
        # Hộp chọn để lọc
        selected_value = st.multiselect(
            f"Lọc theo cột '{first_col}':",
            options=unique_values,
            default=unique_values # Mặc định chọn tất cả
        )
        
        # Lọc dữ liệu dựa trên lựa chọn
        df_filtered = df[df[first_col].isin(selected_value)]
        
        # Hiển thị bảng (width=True để bảng giãn full màn hình)
        st.dataframe(df_filtered, width=True, height=500)
        
        # --- PHẦN BIỂU ĐỒ (Tự động vẽ nếu có số) ---
        st.subheader("3. Biểu Đồ Tự Động")
        # Lấy các cột số
        numeric_cols = df_filtered.select_dtypes(include=['float', 'int']).columns
        
        if len(numeric_cols) > 0:
            chart_col = st.selectbox("Chọn cột số liệu để vẽ:", numeric_cols)
            st.bar_chart(df_filtered[chart_col])
        else:
            st.warning("Không tìm thấy cột dữ liệu số để vẽ biểu đồ.")

    except Exception as e:
        st.error(f"Có lỗi khi đọc file: {e}")
else:
    # Màn hình chờ khi chưa chọn file
    st.markdown("### 👋 Chào mừng!")
    st.write("Vui lòng tải file Excel lên từ cột bên trái để bắt đầu.")