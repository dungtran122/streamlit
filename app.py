import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 1. Cấu hình trang
st.set_page_config(page_title="Data Analytics Pro", page_icon="📈", layout="wide")

st.title("🚀 Phân Tích Dữ Liệu Chuyên Sâu")
st.markdown("---")

# 2. Sidebar
with st.sidebar:
    st.header("📥 Nhập Dữ Liệu")
    uploaded_file = st.file_uploader("Tải file Excel", type=["xlsx", "xls"])
    if uploaded_file:
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_name = st.selectbox("Chọn Sheet:", excel_file.sheet_names)

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
    
    # Tạo các Tabs chức năng
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Tổng quan & Clean", "📊 Phân tích nâng cao", "📉 Tương quan (Math)", "🔍 Truy vấn SQL-like"])

    # --- TAB 1: SỨC KHỎE DỮ LIỆU ---
    with tab1:
        st.subheader("Sức khỏe dữ liệu (Data Health)")
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            st.write("**Thông tin thiếu (Null values):**")
            st.write(df.isnull().sum())
        
        with col_info2:
            st.write("**Dữ liệu trùng lặp:**")
            duplicate_count = df.duplicated().sum()
            st.metric("Số dòng trùng", duplicate_count)
            if duplicate_count > 0:
                if st.button("Xóa trùng lặp ngay"):
                    df = df.drop_duplicates()
                    st.success("Đã xóa trùng lặp!")

        st.markdown("---")
        st.dataframe(df, use_container_width=True)

    # --- TAB 2: PIVOT TABLE TƯƠNG TÁC ---
    with tab2:
        st.subheader("Pivot & Biểu đồ tương tác")
        col_p1, col_p2, col_p3 = st.columns(3)
        
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        num_cols = df.select_dtypes(include=['float', 'int']).columns.tolist()

        if cat_cols and num_cols:
            group_by = col_p1.selectbox("Nhóm theo (Category):", cat_cols)
            value_col = col_p2.selectbox("Giá trị (Numeric):", num_cols)
            agg_func = col_p3.selectbox("Hàm gom nhóm:", ["Sum", "Mean", "Count", "Max", "Min"])

            # Xử lý Groupby
            pivot_df = df.groupby(group_by)[value_col].agg(agg_func.lower()).reset_index()
            
            # Vẽ biểu đồ với Plotly
            fig = px.bar(pivot_df, x=group_by, y=value_col, title=f"{agg_func} của {value_col} theo {group_by}",
                         color=value_col, color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(pivot_df, use_container_width=True)

    # --- TAB 3: PHÂN TÍCH TƯƠNG QUAN ---
    with tab3:
        st.subheader("Ma trận tương quan (Correlation)")
        st.write("Phân tích mối quan hệ giữa các biến số dựa trên hệ số tương quan Pearson:")
        
        # Công thức toán học Pearson
        st.latex(r"r = \frac{\sum (x_i - \bar{x})(y_i - \bar_y)}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar_y})^2}")
        
        if len(num_cols) > 1:
            corr = df[num_cols].corr()
            fig_corr = px.imshow(corr, text_auto=True, aspect="auto", 
                                 title="Heatmap Tương Quan", color_continuous_scale='RdBu_r')
            st.plotly_chart(fig_corr, use_container_width=True)
            
        else:
            st.warning("Cần ít nhất 2 cột số để thực hiện phân tích này.")

    # --- TAB 4: BỘ LỌC NÂNG CAO (REGEX) ---
    with tab4:
        st.subheader("Tìm kiếm nâng cao (Regex Search)")
        search_col = st.selectbox("Chọn cột muốn tìm kiếm:", df.columns)
        search_term = st.text_input(f"Nhập từ khóa hoặc biểu thức Regex để tìm trong '{search_col}':")
        
        if search_term:
            try:
                # Lọc sử dụng regex, không phân biệt hoa thường
                search_results = df[df[search_col].astype(str).str.contains(search_term, case=False, na=False, regex=True)]
                st.write(f"Tìm thấy {len(search_results)} kết quả:")
                st.dataframe(search_results, use_container_width=True)
            except Exception as e:
                st.error(f"Lỗi Regex: {e}")

else:
    st.info("Chào mừng! Hãy tải file lên để bắt đầu phân tích chuyên sâu.")