import streamlit as st
from btc_coin import get_coin_price, get_coin_history

st.title("Coin Watcher 监控台")

name = st.sidebar.text_input("请输入您的名称")
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False


def login_callback():
    if name:
        st.session_state["is_logged_in"] = True
    else:
        st.error("请输入名称")


st.sidebar.button("登录", on_click=login_callback)
currency_icon = {"usd": "$", "cny": "¥"}
currency_map = {"美元": "usd", "人民币": "cny"}

col_ui_1, col_ui_2 = st.sidebar.columns(2)
with col_ui_1:
    coin_type = st.selectbox("选择一种虚拟币", ["bitcoin", "ethereum", "dogecoin"])
with col_ui_2:
    currency_label = st.selectbox("选择一种货币", list(currency_map.keys()))

currency_type = currency_map[currency_label]


if st.session_state["is_logged_in"]:
    with st.spinner("正在连接 CoinGecko 卫星..."):
        price_df = get_coin_history(coin_type=coin_type, currency_type=currency_type)
        price = get_coin_price(coin_type=coin_type, currency_type=currency_type)
    st.success(f"欢迎回来{name}")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.line_chart(price_df)
    with col2:
        st.metric(coin_type.upper(), value=f"{currency_icon[currency_type]}{price}")
    st.divider()
    st.subheader("盈亏计算器")
    c1, c2 = st.columns(2)
    with c1:
        buy_price = st.number_input("买入成本", value=90000)
    with c2:
        btc_number = st.number_input("持仓数量", value=0)
    if price:
        current_price = price * btc_number
        pnl = (price - buy_price) * btc_number
        currency_icon_curr = currency_icon[currency_type]
        st.write(f"当前总仓位: {currency_icon_curr}{current_price:,.2f}")
        if pnl == 0:
            st.info("不亏不赚")
        elif pnl > 0:
            st.success(f"赚了{currency_icon_curr}{pnl:,.2f}")
        elif pnl < 0:
            st.error(f"亏了{currency_icon_curr}{pnl:,.2f}")
    else:
        st.error("未获取到价格")
