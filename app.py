import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
from datetime import datetime

st.set_page_config(
    page_title="ISSI Pro Screener",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {background-color: #0E1117;}
    div[data-testid="metric-container"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        padding: 15px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

DEFAULT_ISSI = [
    "TLKM.JK", "ASII.JK", "UNTR.JK", "ADRO.JK", "PTBA.JK", "ITMG.JK",
    "ICBP.JK", "INDF.JK", "KLBF.JK", "MIKA.JK", "HEAL.JK", "MDKA.JK",
    "ANTM.JK", "INCO.JK", "TINS.JK", "PGAS.JK", "AKRA.JK", "BRIS.JK",
    "BTPS.JK", "CPIN.JK", "JPFA.JK", "EXCL.JK", "ISAT.JK", "MAPI.JK",
    "ACES.JK", "ERAA.JK", "BSDE.JK", "CTRA.JK", "PWON.JK", "SMRA.JK"
]

def round_idx_tick(price):
    if pd.isna(price) or price <= 0:
        return 0
    if price < 200:
        tick = 1
    elif price < 500:
        tick = 2
    elif price < 2000:
        tick = 5
    elif price < 5000:
        tick = 10
    else:
        tick = 25
    return int(round(price / tick) * tick)

@st.cache_data(ttl=900)
def get_ihsg_data():
    try:
        hist = yf.Ticker("^JKSE").history(period="5d")
        if len(hist) >= 2:
            last_close = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2]
            change = last_close - prev_close
            pct_change = (change / prev_close) * 100
            return last_close, change, pct_change
    except Exception:
        pass
    return 0, 0, 0

def calculate_indicators(df):
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['SMA50'] = df['Close'].rolling(window=50).mean()

    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).ewm(alpha=1/14, adjust=False).mean()
    loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/14, adjust=False).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    df['Vol_MA20'] = df['Volume'].rolling(window=20).mean()
    df['RVOL'] = df['Volume'] / df['Vol_MA20']

    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    true_range = np.max(pd.concat([high_low, high_close, low_close], axis=1), axis=1)
    df['ATR'] = true_range.ewm(alpha=1/14, adjust=False).mean()
    return df

def generate_recommendation(row):
    score = 0
    reasons = []

    if row['Close'] > row['EMA20'] and row['EMA20'] > row['SMA50']:
        score += 2
        reasons.append("Strong Uptrend")
    elif row['Close'] > row['EMA20']:
        score += 1
        reasons.append("Bullish (>EMA20)")

    if 30 <= row['RSI'] <= 45:
        score += 2
        reasons.append("RSI Rebound")
    elif 45 < row['RSI'] <= 65:
        score += 1
        reasons.append("Momentum Terjaga")
    elif row['RSI'] > 75:
        score -= 2
        reasons.append("Overbought")
    elif row['RSI'] < 30:
        score += 1
        reasons.append("Oversold")

    if row['MACD'] > row['Signal']:
        score += 1
        reasons.append("MACD Golden Cross")
    else:
        score -= 1

    if row['RVOL'] >= 1.5:
        score += 2
        reasons.append(f"Vol Spike {row['RVOL']:.1f}x")

    if score >= 5:
        rec = "🟢 STRONG BUY"
    elif score >= 3:
        rec = "🔵 BUY / AKUMULASI"
    elif score >= 0:
        rec = "🟡 HOLD / WAIT"
    else:
        rec = "🔴 SELL / AVOID"

    return rec, score, " | ".join(reasons) if reasons else "Konsolidasi"

def send_telegram_alert(bot_token, chat_id, df_signals, strategy_name):
    if not bot_token or not chat_id:
        return False, "Token Bot atau Chat ID belum diisi."
    top_picks = df_signals[df_signals['Rekomendasi'].str.contains("BUY")].head(10)
    if top_picks.empty:
        return False, "Tidak ada sinyal BUY/STRONG BUY untuk dikirim hari ini."

    now_str = datetime.now().strftime("%d %b %Y %H:%M WIB")
    msg = f"🕌 *SINYAL SCREENER ISSI*\n📅 {now_str}\n🎯 Strategi: _{strategy_name}_\n━━━━━━━━━━━━━━━━━━\n\n"
    for _, r in top_picks.iterrows():
        msg += f"*{r['Kode']}* — {r['Rekomendasi']}\n"
        msg += f"• Entry: Rp {int(r['Harga']):,} ({r['Perubahan (%)']:+.2f}%)\n"
        msg += f"• 🎯 TP: Rp {int(r['Target Profit']):,} | 🛑 SL: Rp {int(r['Stop Loss']):,}\n"
        msg += f"• 📦 Lot: {int(r['Saran Lot'])} lot | R/R: 1:{r['Risk/Reward']}\n\n"

    url = f"https://telegram.org{bot_token}/sendMessage"
    try:
        res = requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=10)
        if res.status_code == 200:
            return True, "Sinyal berhasil dikirim ke Telegram!"
        return False, f"Gagal mengirim: {res.text}"
    except Exception as e:
        return False, f"Error koneksi: {str(e)}"

@st.cache_data(ttl=1800)
def scan_issi_stocks(tickers, strategy_mode, modal_trading, risk_pct, sl_mult, tp_mult):
    results = []
    progress_bar = st.progress(0)
    total = len(tickers)
    max_risk_rp = modal_trading * (risk_pct / 100.0)

    for i, ticker in enumerate(tickers):
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period="1y")
            if len(df) < 50:
                continue

            df = calculate_indicators(df)
            latest = df.iloc[-1]
            prev = df.iloc[-2]
            pct_change = ((latest['Close'] - prev['Close']) / prev['Close']) * 100

            entry_price = round_idx_tick(latest['Close'])
            sl_price = max(50, round_idx_tick(entry_price - (sl_mult * latest['ATR'])))
            tp_price = round_idx_tick(entry_price + (tp_mult * latest['ATR'])))

            risk_per_share = max(1, entry_price - sl_price)
            rr_ratio = round(max(0, tp_price - entry_price) / risk_per_share, 2)
            suggested_lots = max(1, int((max_risk_rp / risk_per_share) // 100))
            if (suggested_lots * 100 * entry_price) > modal_trading:
                suggested_lots = max(0, int(modal_trading // (100 * entry_price)))

            info = stock.info
            per = info.get('trailingPE', np.nan)
            pbv = info.get('priceToBook', np.nan)
            roe = info.get('returnOnEquity', np.nan)
            if pd.notna(roe):
                roe = roe * 100

            row_data = {
                'Kode': ticker.replace(".JK", ""),
                'Harga': entry_price,
                'Perubahan (%)': round(pct_change, 2),
                'Stop Loss': sl_price,
                'Target Profit': tp_price,
                'Risk/Reward': rr_ratio,
                'Saran Lot': suggested_lots,
                'RVOL (x)': round(latest['RVOL'], 2),
                'RSI (14)': round(latest['RSI'], 1),
                'EMA20': round(latest['EMA20'], 0),
                'SMA50': round(latest['SMA50'], 0),
                'MACD': round(latest['MACD'], 2),
                'Signal': round(latest['Signal'], 2),
                'PER (x)': round(per, 2) if pd.notna(per) else None,
                'PBV (x)': round(pbv, 2) if pd.notna(pbv) else None,
                'ROE (%)': round(roe, 2) if pd.notna(roe) else None,
                'Close': latest['Close']
            }

            rec, score, reason = generate_recommendation(row_data)
            row_data['Rekomendasi'] = rec
            row_data['Skor'] = score
            row_data['Alasan Sinyal'] = reason

            if strategy_mode == "Semua Saham ISSI":
                results.append(row_data)
            elif strategy_mode == "Swing Trading (Uptrend + Momentum)":
                if latest['Close'] > latest['EMA20'] and 40 <= latest['RSI'] <= 68 and latest['MACD'] > latest['Signal']:
                    results.append(row_data)
            elif strategy_mode == "Bandarmologi / Volume Spike":
                if latest['RVOL'] >= 1.5 and pct_change > 0:
                    results.append(row_data)
            elif strategy_mode == "Value Investing Syariah (Murah & Sehat)":
                if (pd.notna(per) and 0 < per <= 15) and (pd.notna(pbv) and pbv <= 1.5):
                    results.append(row_data)
            elif strategy_mode == "BSJP (Beli Sore Jual Pagi)":
                if pct_change >= 2.0 and latest['RVOL'] >= 1.3 and latest['Close'] > latest['EMA20']:
                    results.append(row_data)
        except Exception:
            pass
        progress_bar.progress((i + 1) / total)

    progress_bar.empty()
    return pd.DataFrame(results)

ihsg_price, ihsg_chg, ihsg_pct = get_ihsg_data()
col_title, col_ihsg = st.columns([3, 1])
with col_title:
    st.title("🕌 ISSI Pro Stock Screener")
    st.caption("Penyaring Saham Syariah BEI + Kalkulator Manajemen Risiko ATR + Alert Telegram")
with col_ihsg:
    st.metric("📊 IHSG", f"{ihsg_price:,.2f}", f"{ihsg_chg:+.2f} ({ihsg_pct:+.2f}%)")

st.divider()

with st.sidebar:
    st.header("⚙️ Navigasi Utama")
    menu = st.radio("Pilih Halaman:", ["🔍 Screener & Trading Plan", "📈 Analisis Chart & SL/TP", "📚 Kamus Rumus", "📂 Kelola Daftar ISSI"])
    strategy = st.selectbox("Pilih Strategi:", [
        "Semua Saham ISSI", "Swing Trading (Uptrend + Momentum)",
        "Bandarmologi / Volume Spike", "Value Investing Syariah (Murah & Sehat)", "BSJP (Beli Sore Jual Pagi)"
    ])
    with st.expander("🛡️ Manajemen Risiko (ATR)", expanded=True):
        modal_trading = st.number_input("Modal Trading (Rp)", min_value=100000, value=10000000, step=1000000)
        risk_pct = st.slider("Risiko / Trade (%)", 0.5, 5.0, 2.0, step=0.5)
        sl_mult = st.slider("Stop Loss (x ATR)", 1.0, 3.0, 1.5, step=0.5)
