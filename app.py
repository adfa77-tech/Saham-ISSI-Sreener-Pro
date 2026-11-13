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
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main {background-color: #0E1117;}
    div[data-testid="metric-container"] {
        background-color: #161B22; border: 1px solid #30363D; padding: 15px; border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

RAW_ISSI = """AADI AALI ABMM ACES ADCP ADES ADMG ADMR ADRO AGAR AGII AIMS AKKU AKPI AKRA AKSI ALAN ALDO AMAN AMAR AMFG AMIN AMMN AMOR ANJT ANTM APEX APIC APLI ARCI ARKA ARKO ARNA ARTA ARTI ASBI ASDM ASII ASJT ASRI ATAP ATIC AUTO AVIA AXIO BABP BAJA BALI BANK BAPI BATA BAUT BAYU BBCA BBHI BBKP BBMD BBNI BBRI BBSI BBTN BBYB BCIC BDMN BEBS BEEF BEER BELI BESS BEST BFIN BGTG BHIT BIKA BINA BINO BIPI BIRD BISI BITO BJBR BJTM BKDP BKSL BLTA BLTZ BLUE BMAS BMHS BMRI BMSR BMTR BNBA BNGA BNII BNLI BOBA BOGA BOLA BOLT BPTR BRAM BREN BRIS BRMS BRNA BSBK BSDE BSML BSSR BSWD BTPS BUAH BUDI BUKK BULL BUMI BUVA BVIC BWPT BYAN CAKK CAMP CARS CASA CASH CASS CBRE CBUT CCSI CEKA CENT CFIN CGAS CHEK CINT CITA CITY CLPI CMNP CMPP CMRY CNKO CNTX COCO CPIN CRAB CSIS CSMI CSRA CTBN CTRA CUAN DADA DATA DANA DEAL DEWI DFAM DGIK DGNS DIDX DIRA DMMX DNAR DOID DPNS DRMA DSFI DSNG DSSA DUCK DWGL EAST ECII EDGE EDIN EKAD ELIT ELSA ELPI EMDE ENAK ENRG ENZO EPAC EPMT ERAA ERTX ESIP ESSA ESTA ESTI ETWA EXCL FAPA FASW FILM FIMP FIRE FISH FPNI FREN FUTR FWCT GAMA GATE GBKA GEMA GEMS GGRM GGRP GHON GIAA GJTL GLVA GMFI GMTD GOLD GOLF GOOD GPRA GPSO GRPH GTBO GTSI GULA GZCO HADE HAIS HALO HATM HDIT HEAL HELI HERO HEXA HITS HKMU HMSP HOKI HOME HOMI HOPE HRME HRTA IATA IBFN IBOS ICBP ICON IDEA IDPR IFII IFSH IGAR IIKF IMAS IMJS IMPC INCO INDF INDS INKP INPC INPP INPS INRU INTA INTD INTP IOSP IPCC IPCM IPEH IPOL IPPE ISAT ISSP ITMA ITMG JATI JAWA JAYA JECC JGLE JKON JMAS JPFA JSMR JSPT JTPE KAEF KARW KAYU KEEN KEIS KELN KDTN KEJU KICI KIJA KINO KJEN KKGI KLBF KMDS KOBX KOIN KOKA KONI KOPI KOTA KPIG KRAK LABS LAJU LAND LAPD LCKM LEAD LFLO LIFE LINK LION LMPI LMSH LPCK LPGI LPIN LPPF LPPS LPTA LRNA LSIP LUCK LUCY MABA MAGP MAIN MAMI MAPA MAPI MARI MARK MASB MAYA MBAP MBMA MBSS MBTO MCAS MDKA MEDC MEGA MENN MERK META MFMI MGLV MICE MIDI MIKA MINA MIRA MITI MKNT MKPI MLIA MLPL MLPT MMIX MMLP MNCN MOLI MPPA MPXL MRAT MREI MSIN MSKY MTDL MTEL MTMH MTSM MUTU MYOH NANO NICK NELY NEMI NEST NFCX NINE NLIQ NOBU NPGF NSSS NUSA NZIA OASA OBMD OCAP OKAS OLIV OMRE PADA PADI PALM PAMG PANI PARA PATK PBLE PBID PBRX PDES PEHA PEVE PGAS PGEO PGLI PGUN PICO PJAA PKPK PLAS PLIN PMJS PNBN PNBS PNGO PNIN PNSE POLA POLI POLL POLY POOL PORT POSA POWR PPRO PRAS PSAB PSDN PSGO PSSI PTBA PTDU PUDP PURA PURE PWON PYFA PZZA RAAM RAJA RANC RBMS RDTX REAL RELF RICY RIGS RISE RMKE ROCK ROTI RUIS RUNS SAFE SAGE SAID SAME SAMF SAPX SATU SBAT SBMA SCCO SCMA SCNP SCPI SDPC SDRA SEMA SGER SGRO SHIP SICO SIDO SILO SIMA SIMP SKLT SKRN SKYB SMIK SMIL SMKM SMMA SMMT SMRA SMRU SMSM SNLK SOCI SOFA SONA SPMA SPTO SQMI SRAJ SRTG SSIA SOSS SSTM STAA STAR STRK STTP SULI SUNI SUPR SURE SURI SWID TALF TAMA TAMU TAPG TARA TAXI TBMS TCPI TEBE TECH TEGH TELE TFAS TGKA TIFA TINS TIRA TIRT TKIM TLKM TMAS TMPO TOBA TOOL TOWR TPIA TPMA TRAM TRIN TRIS TRJA TRON TRUK TSPC TUGU TYRE UANG ULTJ UNIC UNIQ UNIT UNTR UNVR URBN UVCR VAST VERN VICO VINS VISI VKTR VRNA WAPO WEHA WGSH WIFI WIIM WINS WIRG WMPP WTON XASI XBIO XBNI XBNP XISC XIJI XIPI XLBF XOID XPLN YELO YPAS YUAN ZATA ZBRA ZINC ZYRX"""

EXCEL_ISSI_TICKERS = [f"{k}.JK" for k in RAW_ISSI.split()]

def round_idx_tick(price):
    if pd.isna(price) or price <= 0:
        return 0
    tick = 1 if price < 200 else (2 if price < 500 else (5 if price < 2000 else (10 if price < 5000 else 25)))
    return int(round(price / tick) * tick)

def flatten_df(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df.loc[:, ~df.columns.duplicated()]

@st.cache_data(ttl=600)
def get_ihsg_data():
    try:
        hist = flatten_df(yf.download("^JKSE", period="5d", progress=False))
        if len(hist) >= 2:
            lc, pc = float(hist['Close'].iloc[-1]), float(hist['Close'].iloc[-2])
            return lc, lc - pc, ((lc - pc) / pc) * 100
    except Exception:
        pass
    return 0.0, 0.0, 0.0

def calculate_indicators(df):
    df = df.copy()
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).ewm(alpha=1/14, adjust=False).mean()
    loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/14, adjust=False).mean()
    df['RSI'] = (100 - (100 / (1 + (gain / loss.replace(0, np.nan))))).fillna(50)
    df['MACD'] = df['Close'].ewm(span=12, adjust=False).mean() - df['Close'].ewm(span=26, adjust=False).mean()
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['RVOL'] = (df['Volume'] / df['Volume'].rolling(window=20).mean().replace(0, np.nan)).fillna(1.0)
    tr = np.max(pd.concat([df['High'] - df['Low'], np.abs(df['High'] - df['Close'].shift()), np.abs(df['Low'] - df['Close'].shift())], axis=1), axis=1)
    df['ATR'] = tr.ewm(alpha=1/14, adjust=False).mean()
    return df

def generate_recommendation(row):
    score, reasons = 0, []
    if row['Close'] > row['EMA20'] and row['EMA20'] > row['SMA50']:
        score += 2; reasons.append("Strong Uptrend")
    elif row['Close'] > row['EMA20']:
        score += 1; reasons.append("Bullish (>EMA20)")
    if 30 <= row['RSI'] <= 48:
        score += 2; reasons.append("RSI Area Rebound")
    elif 48 < row['RSI'] <= 68:
        score += 1; reasons.append("Momentum Sehat")
    elif row['RSI'] > 75:
        score -= 2; reasons.append("Overbought")
    elif row['RSI'] < 30:
        score += 1; reasons.append("Oversold")
    if row['MACD'] > row['Signal']:
        score += 1; reasons.append("MACD Golden Cross")
    else:
        score -= 1
    if row['RVOL'] >= 1.3:
        score += 2; reasons.append(f"Vol Spike {row['RVOL']:.1f}x")
    rec = "🟢 STRONG BUY" if score >= 5 else ("🔵 BUY / AKUMULASI" if score >= 3 else ("🟡 WATCHLIST" if score >= 1 else "🔴 AVOID"))
    return rec, score, " | ".join(reasons) if reasons else "Konsolidasi"

def send_telegram_alert(bot_token, chat_id, df_signals, strategy_name):
    if not bot_token or not chat_id:
        return False, "Token Bot atau Chat ID belum diisi."
    top = df_signals[df_signals['Rekomendasi'].str.contains("BUY")].head(10)
    if top.empty:
        return False, "Tidak ada sinyal BUY hari ini."
    msg = f"🕌 *SINYAL SCREENER ISSI*\n🎯 _{strategy_name}_\n━━━━━━━━━━━━━━━━━━\n\n"
    for _, r in top.iterrows():
        msg += f"*{r['Kode']}* — {r['Rekomendasi']}\n• Entry: Rp {int(r['Harga']):,} ({r['Perubahan (%)']:+.2f}%)\n• 🎯 TP: Rp {int(r['Target Profit']):,} | 🛑 SL: Rp {int(r['Stop Loss']):,}\n• 📦 Lot: {int(r['Saran Lot'])} lot | R/R: 1:{r['Risk/Reward']}\n\n"
    try:
        res = requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=10)
        return (True, "Terkirim ke Telegram!") if res.status_code == 200 else (False, f"Gagal: {res.text}")
    except Exception as e:
        return False, f"Error: {str(e)}"

@st.cache_data(ttl=1800)
def fetch_all_issi_market_data(tickers):
    all_dfs = {}
    for i in range(0, len(tickers), 150):
        chunk = tickers[i:i + 150]
        try:
            data = yf.download(tickers=chunk, period="6mo", group_by="ticker", threads=True, progress=False)
            for t in chunk:
                try:
                    if t in data.columns.get_level_values(0):
                        df_t = flatten_df(data[t]).dropna(subset=['Close'])
                        if len(df_t) >= 30:
                            all_dfs[t] = df_t
                except Exception:
                    continue
        except Exception:
            continue
    return all_dfs

def scan_issi_stocks(tickers, strategy_mode, modal_trading, risk_pct, sl_mult, tp_mult):
    with st.spinner("⚡ Memindai seluruh saham ISSI secara batch..."):
        market_data = fetch_all_issi_market_data(tuple(tickers))
    results, max_risk_rp = [], modal_trading * (risk_pct / 100.0)
    for ticker, df_raw in market_data.items():
        try:
            df = calculate_indicators(df_raw)
            latest, prev = df.iloc[-1], df.iloc[-2]
            if latest['Volume'] <= 0 or pd.isna(latest['Close']):
                continue
            pct_chg = ((latest['Close'] - prev['Close']) / prev['Close']) * 100
            entry = round_idx_tick(latest['Close'])
            sl = max(50, round_idx_tick(entry - (sl_mult * latest['ATR'])))
            tp = round_idx_tick(entry + (tp_mult * latest['ATR']))
            risk_ps = max(1, entry - sl)
            rr = round(max(0, tp - entry) / risk_ps, 2)
            lots = max(1, int((max_risk_rp / risk_ps) // 100))
            if (lots * 100 * entry) > modal_trading:
                lots = max(0, int(modal_trading // (100 * entry)))
            row = {
                'Kode': ticker.replace(".JK", ""), 'Harga': entry, 'Perubahan (%)': round(pct_chg, 2),
                'Volume': int(latest['Volume']), 'Stop Loss': sl, 'Target Profit': tp, 'Risk/Reward': rr,
                'Saran Lot': lots, 'RVOL (x)': round(latest['RVOL'], 2), 'RSI (14)': round(latest['RSI'], 1),
                'EMA20': round(latest['EMA20'], 0), 'SMA50': round(latest['SMA50'], 0) if pd.notna(latest['SMA50']) else 0,
                'MACD': round(latest['MACD'], 2), 'Signal': round(latest['Signal'], 2), 'Close': latest['Close']
            }
            rec, score, reason = generate_recommendation(row)
            row['Rekomendasi'], row['Skor'], row['Alasan Sinyal'] = rec, score, reason

            if strategy_mode == "Semua Saham ISSI":
                results.append(row)
            elif strategy_mode == "Swing Trading (Uptrend + Momentum)" and latest['Close'] > latest['EMA20'] and 40 <= latest['RSI'] <= 68 and latest['MACD'] > latest['Signal']:
                results.append(row)
            elif strategy_mode == "Bandarmologi / Volume Spike" and latest['RVOL'] >= 1.3 and pct_chg > 0:
                results.append(row)
            elif strategy_mode == "BSJP (Beli Sore Jual Pagi)" and pct_chg >= 1.5 and latest['RVOL'] >= 1.2:
                results.append(row)
        except Exception:
            continue
    return pd.DataFrame(results)

# HEADER UTAMA & IHSG
ihsg_price, ihsg_chg, ihsg_pct = get_ihsg_data()
col_t, col_i = st.columns([3, 1])
with col_t:
    st.title("🕌 ISSI Pro Stock Screener")
    st.caption("Penyaring Saham Syariah BEI + Kalkulator Risiko ATR + Batch Downloader Cepat")
with col_i:
    st.metric("📊 IHSG", f"{ihsg_price:,.2f}" if ihsg_price > 0 else "Memuat...", f"{ihsg_chg:+.2f} ({ihsg_pct:+.2f}%)")

st.divider()

# PANEL KONTROL UTAMA (DI HALAMAN UTAMA)
if 'issi_list' not in st.session_state:
    st.session_state['issi_list'] = EXCEL_ISSI_TICKERS

st.subheader("⚙️ Panel Kontrol & Pengaturan Strategi")
c1, c2 = st.columns(2)
with c1:
    menu = st.selectbox("Pilih Menu Halaman:", ["🔍 Screener & Trading Plan", "📈 Analisis Chart & SL/TP", "📚 Kamus Rumus", "📂 Daftar Saham ISSI"])
with c2:
    strategy = st.selectbox("Pilih Strategi:", ["Semua Saham ISSI", "Swing Trading (Uptrend + Momentum)", "Bandarmologi / Volume Spike", "BSJP (Beli Sore Jual Pagi)"])

with st.expander("🎛️ Pengaturan Manajemen Risiko & Filter", expanded=False):
    f1, f2, f3 = st.columns(3)
    with f1:
        modal_trading = st.number_input("Modal Trading (Rp)", min_value=100000, value=10000000, step=1000000)
        risk_pct = st.slider("Risiko / Trade (%)", 0.5, 5.0, 2.0, step=0.5)
    with f2:
        sl_mult = st.slider("Stop Loss (x ATR)", 1.0, 3.0, 1.5, step=0.5)
        tp_mult = st.slider("Take Profit (x ATR)", 1.5, 6.0, 3.0, step=0.5)
    with f3:
        min_price = st.number_input("Harga Minimal (Rp)", min_value=0, value=0, step=50)
        max_rsi = st.slider("Maksimal RSI (14)", 20, 100, 100)
        only_buy = st.checkbox("Hanya Sinyal BUY / STRONG BUY", value=False)
    
    t1, t2 = st.columns(2)
    with t1:
        tg_token = st.text_input("Telegram Bot Token", type="password")
    with t2:
        tg_chat_id = st.text_input("Telegram Chat ID")

if st.button("🔄 Refresh Data Pasar & Jalankan Screener", use_container_width=True, type="primary"):
    st.cache_data.clear()
    st.rerun()

st.divider()

# KONTEN HALAMAN
if menu == "🔍 Screener & Trading Plan":
    df_screen = scan_issi_stocks(st.session_state['issi_list'], strategy, modal_trading, risk_pct, sl_mult, tp_mult)
    if not df_screen.empty:
        df_filtered = df_screen[(df_screen['Harga'] >= min_price) & (df_screen['RSI (14)'] <= max_rsi)]
        if only_buy:
            df_filtered = df_filtered[df_filtered['Rekomendasi'].str.contains("BUY")]
        df_filtered = df_filtered.sort_values(by="Skor", ascending=False)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Emiten Lolos", f"{len(df_filtered)}")
        m2.metric("Sinyal Strong Buy", f"{len(df_filtered[df_filtered['Rekomendasi'] == '🟢 STRONG BUY'])}")
        m3.metric("Batas Risiko", f"Rp {int(modal_trading * (risk_pct/100)):,}")
        m4.metric("Rata-rata R/R", f"1 : {df_filtered['Risk/Reward'].mean():.2f}" if len(df_filtered) > 0 else "-")
        
        st.markdown("---")
        col_sub, col_tg = st.columns([3, 1])
        with col_sub:
            st.subheader(f"📋 Hasil Screening: {strategy}")
        with col_tg:
            if st.button("📲 Kirim ke Telegram", use_container_width=True):
                ok, msg = send_telegram_alert(tg_token, tg_chat_id, df_filtered, strategy)
                st.success(msg) if ok else st.error(msg)
        
        cols = ['Kode', 'Rekomendasi', 'Harga', 'Perubahan (%)', 'Stop Loss', 'Target Profit', 'Risk/Reward', 'Saran Lot', 'RVOL (x)', 'RSI (14)', 'Alasan Sinyal']
        st.dataframe(df_filtered[cols], use_container_width=True, hide_index=True)
        
        csv = df_filtered[cols].to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", data=csv, file_name=f"issi_screener_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")
    else:
        st.warning("Tidak ada saham yang memenuhi kriteria atau data sedang dimuat. Coba klik tombol Refresh di atas.")

elif menu == "📈 Analisis Chart & SL/TP":
    st.subheader("📈 Grafik Teknikal Interaktif & Level Otomatis")
    clean_tickers = [t.replace(".JK", "") for t in st.session_state['issi_list']]
    selected_stock = st.selectbox("Pilih Kode Saham ISSI:", clean_tickers)
    
    if selected_stock:
        try:
            df_chart = calculate_indicators(flatten_df(yf.Ticker(f"{selected_stock}.JK").history(period="6mo")))
            if not df_chart.empty:
                last_row = df_chart.iloc[-1]
                entry_p = round_idx_tick(last_row['Close'])
                sl_p = max(50, round_idx_tick(entry_p - (sl_mult * last_row['ATR'])))
                tp_p = round_idx_tick(entry_p + (tp_mult * last_row['ATR']))
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Harga Acuan Entry", f"Rp {entry_p:,}")
                c2.metric("Target Profit (TP)", f"Rp {tp_p:,}")
                c3.metric("Batas Stop Loss (SL)", f"Rp {sl_p:,}")
                
                fig = go.Figure()
                fig.add_trace(go.Candlestick(x=df_chart.index, open=df_chart['Open'], high=df_chart['High'], low=df_chart['Low'], close=df_chart['Close'], name="Harga"))
                fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['EMA20'], line=dict(color='#00E5FF', width=1.5), name="EMA 20"))
                fig.add_trace(go.Scatter(x=df_chart.unstack() if False else df_chart.index, y=df_chart['SMA50'], line=dict(color='#FFAB00', width=1.5), name="SMA 50"))
                fig.add_hline(y=tp_p, line_dash="dash", line_color="#00E676", annotation_text=f"TP: Rp {tp_p:,}")
                fig.add_hline(y=sl_p, line_dash="dash", line_color="#FF5252", annotation_text=f"SL: Rp {sl_p:,}")
                fig.update_layout(template="plotly_dark", height=500, xaxis_rangeslider_visible=False, title=f"Visualisasi Trading Plan {selected_stock}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Data chart tidak tersedia.")
        except Exception as e:
            st.error(f"Gagal memuat chart: {str(e)}")

elif menu == "📚 Kamus Rumus":
    st.subheader("📚 Penjelasan Rumus & Strategi Kuantitatif")
    st.markdown("""
    * **Semua Saham ISSI:** Menampilkan seluruh daftar 574+ emiten syariah terdaftar tanpa syarat filter strategi.
    * **Trend Following (EMA 20 & SMA 50):** Menguji arah tren jangka pendek dan menengah.
    * **Momentum (RSI 14):** Mendeteksi area pantulan sehat (30–48) dan momentum kuat (48–68).
    * **Bandarmologi (RVOL):** Memantau lonjakan volume transaksi harian terhadap rata-rata 20 hari ($\ge 1.3\text{x}$).
    * **Manajemen Risiko ATR:** Menentukan jarak Stop Loss dan Take Profit secara dinamis berdasarkan volatilitas harga.
    """)

elif menu == "📂 Daftar Saham ISSI":
    st.subheader("📂 Daftar Lengkap Emiten Syariah ISSI (574+ Saham)")
    st.write(f"Total emiten aktif yang tersimpan dalam sistem: **{len(st.session_state['issi_list'])} emiten**")
    df_list_view = pd.DataFrame({"No": range(1, len(st.session_state['issi_list'])+1), "Kode Saham": st.session_state['issi_list']})
    st.dataframe(df_list_view, use_container_width=True, hide_index=True)
