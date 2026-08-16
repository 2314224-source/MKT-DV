import streamlit as st
import pandas as pd
import os

# =========================
# CẤU HÌNH APP
# =========================
st.set_page_config(
    page_title="Quản lý khách hàng",
    page_icon="👤",
    layout="wide"
)

FILE_NAME = "khach_hang.csv"

# =========================
# TẠO FILE NẾU CHƯA CÓ
# =========================
columns = [
    "Số điện thoại",
    "Tên khách hàng",
    "Khu vực",
    "Ghi chú"
]

if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=columns)
    df.to_csv(FILE_NAME, index=False, encoding="utf-8-sig")


# =========================
# HÀM ĐỌC DỮ LIỆU
# =========================
def load_data():
    try:
        return pd.read_csv(FILE_NAME, encoding="utf-8-sig")
    except:
        return pd.DataFrame(columns=columns)


# =========================
# TIÊU ĐỀ
# =========================
st.title("👤 QUẢN LÝ THÔNG TIN KHÁCH HÀNG")
st.write("Nhập và quản lý thông tin khách hàng")

st.divider()


# =========================
# FORM NHẬP KHÁCH HÀNG
# =========================
st.subheader("➕ Thêm khách hàng")

with st.form("customer_form"):

    col1, col2 = st.columns(2)

    with col1:
        phone = st.text_input(
            "Số điện thoại *",
            placeholder="Ví dụ: 0901234567"
        )

        customer_name = st.text_input(
            "Tên khách hàng *",
            placeholder="Nhập họ và tên"
        )

    with col2:
        area = st.selectbox(
            "Khu vực",
            [
                "Đà Lạt",
                "Đức Trọng",
                "Bảo Lộc",
                "Lâm Hà",
                "Di Linh",
                "Đơn Dương",
                "Lạc Dương",
                "Khác"
            ]
        )

        note = st.text_area(
            "Ghi chú",
            placeholder="Nhập ghi chú về khách hàng..."
        )

    submit = st.form_submit_button(
        "💾 Lưu khách hàng",
        use_container_width=True
    )


# =========================
# XỬ LÝ LƯU DỮ LIỆU
# =========================
if submit:

    phone = phone.strip()
    customer_name = customer_name.strip()

    if phone == "":
        st.error("❌ Vui lòng nhập số điện thoại!")

    elif customer_name == "":
        st.error("❌ Vui lòng nhập tên khách hàng!")

    elif not phone.isdigit():
        st.error("❌ Số điện thoại chỉ được chứa chữ số!")

    else:
        df = load_data()

        # Kiểm tra số điện thoại đã tồn tại
        if phone in df["Số điện thoại"].astype(str).values:
            st.warning("⚠️ Số điện thoại này đã tồn tại!")

        else:
            new_customer = pd.DataFrame([{
                "Số điện thoại": phone,
                "Tên khách hàng": customer_name,
                "Khu vực": area,
                "Ghi chú": note
            }])

            df = pd.concat(
                [df, new_customer],
                ignore_index=True
            )

            df.to_csv(
                FILE_NAME,
                index=False,
                encoding="utf-8-sig"
            )

            st.success("✅ Đã lưu thông tin khách hàng!")

            # Làm mới app
            st.rerun()


st.divider()


# =========================
# DANH SÁCH KHÁCH HÀNG
# =========================
st.subheader("📋 Danh sách khách hàng")

df = load_data()

if len(df) == 0:

    st.info("Chưa có khách hàng nào.")

else:

    # =========================
    # TÌM KIẾM
    # =========================
    search = st.text_input(
        "🔎 Tìm kiếm khách hàng",
        placeholder="Nhập tên hoặc số điện thoại..."
    )

    filtered_df = df.copy()

    if search:
        search = search.lower()

        filtered_df = df[
            df["Tên khách hàng"]
            .astype(str)
            .str.lower()
            .str.contains(search)
            |
            df["Số điện thoại"]
            .astype(str)
            .str.contains(search)
        ]

    # =========================
    # THỐNG KÊ
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "👥 Tổng khách hàng",
            len(df)
        )

    with col2:
        st.metric(
            "🔎 Kết quả tìm kiếm",
            len(filtered_df)
        )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


    # =========================
    # XÓA KHÁCH HÀNG
    # =========================
    st.subheader("🗑️ Xóa khách hàng")

    phone_delete = st.text_input(
        "Nhập số điện thoại khách hàng cần xóa",
        placeholder="Ví dụ: 0901234567"
    )

    if st.button(
        "🗑️ Xóa khách hàng",
        type="secondary"
    ):

        if phone_delete in df["Số điện thoại"].astype(str).values:

            df = df[
                df["Số điện thoại"].astype(str)
                != phone_delete
            ]

            df.to_csv(
                FILE_NAME,
                index=False,
                encoding="utf-8-sig"
            )

            st.success("✅ Đã xóa khách hàng!")

            st.rerun()

        else:
            st.error("❌ Không tìm thấy số điện thoại này!")


    # =========================
    # TẢI FILE EXCEL/CSV
    # =========================
    st.subheader("📥 Xuất dữ liệu")

    csv_data = df.to_csv(
        index=False,
        encoding="utf-8-sig"
    ).encode("utf-8-sig")

    st.download_button(
        label="📥 Tải danh sách khách hàng",
        data=csv_data,
        file_name="danh_sach_khach_hang.csv",
        mime="text/csv",
        use_container_width=True
    )
