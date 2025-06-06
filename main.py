import streamlit as st
import math


# Function for startup current pulse time calculation
def calculate_tq(k, c, m_label, un, ib, iq_percent_input):
    try:
        iq_percent = iq_percent_input / 100
        iq = ib * iq_percent
        m_values = {
            "单相 = 1": 1,
            "三相三线 = √3": round(math.sqrt(3), 4),
            "三相四线 = 3": 3
        }
        m = m_values.get(m_label, 1)
        denominator = c * m * un * iq
        if denominator == 0:
            return "❌ 分母为 0，无法计算"

        tq_min = k * 60 * 1000 / denominator
        tq_sec = tq_min * 60
        minutes = int(tq_sec // 60)
        seconds = int(tq_sec % 60)

        notice = "⚠️ Tq 超过 60 分钟，建议检查参数。\n" if tq_min > 60 else ""
        result = (
            f"{notice}"
            f"Tq ≈ {minutes} 分 {seconds} 秒（约 {int(tq_sec)} 秒）\n\n"
            f"参数说明：\n"
            f"启动时间系数 k = {k}\n"
            f"仪表常数 C = {c} imp/kWh\n"
            f"系数 m = {m_label}\n"
            f"额定电压 Un = {un} V\n"
            f"额定电流 Ib = {ib} A\n"
            f"启动电流 = {iq:.3f} A（{iq_percent_input:.2f}%）"
        )
        return result
    except Exception as e:
        return f"❌ 错误：{str(e)}"


# Function for cosine value and angle conversion
def cosine_converter(mode: str, value: str) -> str:
    try:
        val = float(value.strip())

        if mode == "余弦值 → 角度":
            if not -1 <= val <= 1:
                return "❌ 余弦值必须在 [-1, 1] 区间内"
            angle1 = round(math.degrees(math.acos(val)), 2)
            angle2 = round(360 - angle1, 2)
            return f"可能角度为：{angle1}° 和 {angle2}°"

        elif mode == "角度 → 余弦值":
            angle = val % 360  # 限制角度在 0~360 范围
            cos_val = round(math.cos(math.radians(angle)), 4)
            return f"余弦值为：{cos_val}"

        else:
            return "❌ 无效的模式选择"

    except ValueError:
        return "❌ 请输入有效的数值（例如 0.5 或 60）"


# Main function to handle the UI
def main():
    st.set_page_config(page_title="计算工具", layout="wide")  # Set the page layout to wide

    # Sidebar for selecting tools
    st.sidebar.title("选择工具")
    tool = st.sidebar.radio("选择你需要的工具", ["启动电流出脉冲时间计算", "余弦值 ↔ 角度换算"])

    # Tool 1: 启动电流出脉冲时间计算工具
    if tool == "启动电流出脉冲时间计算":
        st.header("⏱️ 启动电流出脉冲时间计算工具")
        k = st.number_input("启动时间系数 k", value=1.1, min_value=0.1, step=0.1)
        c = st.number_input("仪表常数 C (imp/kWh)", value=1000, min_value=1, step=10)
        m_label = st.selectbox("系数 m", ["单相 = 1", "三相三线 = √3", "三相四线 = 3"])
        un = st.number_input("额定电压 Un (V)", value=230, min_value=0)
        ib = st.number_input("额定电流 Ib (A)", value=5, min_value=0)
        iq_percent_input = st.number_input("启动电流百分比（例如 0.4 表示 0.4%）", value=0.4, min_value=0.0)

        if st.button("计算 Tq"):
            result = calculate_tq(k, c, m_label, un, ib, iq_percent_input)
            st.text_area("Tq 计算结果", result, height=200)

    # Tool 2: 余弦值 ↔ 角度换算工具
    elif tool == "余弦值 ↔ 角度换算":
        st.header("🎯 余弦值 ↔ 角度 双向换算工具")
        mode = st.selectbox("选择计算模式", ["余弦值 → 角度", "角度 → 余弦值"], index=0)
        input_val = st.text_input("请输入数值", placeholder="例如：0.5 或 60")

        if st.button("开始计算"):
            result = cosine_converter(mode, input_val)
            st.text_area("计算结果", result, height=150)


if __name__ == "__main__":
    main()
