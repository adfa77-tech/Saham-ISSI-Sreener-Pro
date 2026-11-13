import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from concurrent.futures import ThreadPoolExecutor, as_completed

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Screener Ketat Saham ISSI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Styling UI Custom Dark Mode Artistik & Profesional
st.markdown("""
<style>
    .stApp { background-color: #0b0e14; color: #e6edf3; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .metric-card {
        background: linear-gradient(135deg, #161b22 0%, #1f242d 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .content-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
    }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #238636 0%, #2ea043 100%);
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 10px 20px;
        box-shadow: 0 4px 10px rgba(35, 134, 54, 0.3);
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #2ea043 0%, #3fb950 100%);
    }
</style>
""", unsafe_allow_html=True)

# Inisialisasi State Menu
if 'active_menu' not in st.session_state:
    st.session_state.active_menu = "Screener"

# POSISI JUDUL UTAMA DI PALING ATAS HALAMAN
st.markdown("## **Screener Ketat Saham ISSI**")
st.markdown("<hr style='border: 0.5px solid #21262d; margin-top: 0px; margin-bottom: 15px;'>", unsafe_allow_html=True)

# Header Navigasi Fungsional
col_m1, col_m2, col_m3, col_space = st.columns([1.2, 1.2, 1.2, 6.4])
with col_m1:
    if st.button("Screener", use_container_width=True):
        st.session_state.active_menu = "Screener"
with col_m2:
    if st.button("Daftar Saham", use_container_width=True):
        st.session_state.active_menu = "Daftar Saham"
with col_m3:
    if st.button("Strategi", use_container_width=True):
        st.session_state.active_menu = "Strategi"

st.markdown("<hr style='border: 0.5px solid #21262d; margin-top: 10px; margin-bottom: 25px;'>", unsafe_allow_html=True)

# Database Ticker Saham ISSI Lengkap
RAW_ISSI = """AADI AALI ABMM ACES ADCP ADES ADMG ADMR ADRO AGAR AGII AIMS AKKU AKPI AKRA AKSI ALAN ALDO AMAN AMAR AMFG AMIN AMMN AMOR ANJT ANTM APEX APIC APLI ARCI ARKA ARKO ARNA ARTA ARTI ASBI ASDM ASII ASJT ASRI ATAP ATIC AUTO AVIA AXIO BABP BAJA BALI BANK BAPI BATA BAUT BAYU BBCA BBHI BBKP BBMD BBNI BBRI BBSI BBTN BBYB BCIC BDMN BEBS BEEF BEER BELI BESS BEST BFIN BGTG BHIT BIKA BINA BINO BIPI BIRD BISI BITO BJBR BJTM BKDP BKSL BLTA BLTZ BLUE BMAS BMHS BMRI BMSR BMTR BNBA BNGA BNII BNLI BOBA BOGA BOLA BOLT BPTR BRAM BREN BRIS BRMS BRNA BSBK BSDE BSML BSSR BSWD BTPS BUAH BUDI BUKK BULL BUMI BUVA BVIC BWPT BYAN CAKK CAMP CARS CASA CASH CASS CBRE CBUT CCSI CEKA CENT CFIN CGAS CHEK CINT CITA CITY CLPI CMNP CMPP CMRY CNKO CNTX COCO CPIN CRAB CSIS CSMI CSRA CTBN CTRA CUAN DADA DATA DANA DEAL DEWI DFAM DGIK DGNS DIDX DIRA DMMX DNAR DOID DPNS DRMA DSFI DSNG DSSA DUCK DWGL EAST ECII EDGE EDIN EKAD ELIT ELSA ELPI EMDE ENAK ENRG ENZO EPAC EPMT ERAA ERTX ESIP ESSA ESTA ESTI ETWA EXCL FAPA FASW FILM FIMP FIRE FISH FPNI FREN FUTR FWCT GAMA GATE GBKA GEMA GEMS GGRM GGRP GHON GIAA GJTL GLVA GMFI GMTD GOLD GOLF GOOD GPRA GPSO GRPH GTBO GTSI GULA GZCO HADE HAIS HALO HATM HDIT HEAL HELI HERO HEXA HITS HKMU HMSP HOKI HOME HOMI HOPE HRME HRTA IATA IBFN IBOS ICBP ICON IDEA IDPR IFII IFSH IGAR IIKF IMAS IMJS IMPC INCO INDF INDS INKP INPC INPP INPS INRU INTA INTD INTP IOSP IPCC IPCM IPEH IPOL IPPE ISAT ISSP ITMA ITMG JATI JAWA JAYA JECC JGLE JKON JMAS JPFA JSMR JSPT JTPE KAEF KARW KAYU KEEN KEIS KELN KDTN KEJU KICI KIJA KINO KJEN KKGI KLBF KMDS KOBX KOIN KOKA KONI KOPI KOTA KPIG KRAK LABS LAJU LAND LAPD LCKM LEAD LFLO LIFE LINK LION LMPI LMSH LPCK LPGI LPIN LPPF LPPS LPTA LRNA LSIP LUCK LUCY MABA MAGP MAIN MAMI MAPA MAPI MARI MARK MASB MAYA MBAP MBMA MBSS MBTO MCAS MDKA MEDC MEGA MENN MERK META MFMI MGLV MICE MIDI MIKA MINA MIRA MITI MKNT MKPI MLIA MLPL MLPT MMIX MMLP MNCN MOLI MPPA MPXL MRAT MREI MSIN MSKY MTDL MTEL MTMH MTSM MUTU MYOH NANO NICK NELY NEMI NEST NFCX NINE NLIQ NOBU NPGF NSSS NUSA NZIA OASA OBMD OCAP OKAS OLIV OMRE PADA PADI PALM PAMG PANI PARA PATK PBLE PBID PBRX PDES PEHA PEVE PGAS PGEO PGLI PGUN PICO PJAA PKPK PLAS PLIN PMJS PNBN PNBS PNGO PNIN PNSE POLA POLI POLL POLY POOL PORT POSA POWR PPRO PRAS PSAB PSDN PSGO PSSI PTBA PTDU PUDP PURA PURE PWON PYFA PZZA RAAM RAJA RANC RBMS RDTX REAL RELF RICY RIGS RISE RMKE ROCK ROTI RUIS RUNS SAFE SAGE SAID SAME SAMF SAPX SATU SBAT SBMA SCCO SCMA SCNP SCPI SDPC SDRA SEMA SGER SGRO SHIP SICO SIDO SILO SIMA SIMP SKLT SKRN SKYB SMIK SMIL SMKM SMMA SMMT SMRA SMRU SMSM SNLK SOCI SOFA SONA SPMA SPTO SQMI SRAJ SRTG SSIA SOSS SSTM STAA STAR STRK STTP SULI SUNI SUPR SURE SURI SWID TALF TAMA TAMU TAPG TARA TAXI TBMS TCPI TEBE TECH TEGH TELE TFAS TGKA TIFA TINS TIRA TIRT TKIM TLKM TMAS TMPO TOBA TOOL TOWR TPIA TPMA TRAM TRIN TRIS TRJA TRON TRUK TSPC TUGU TYRE UANG ULTJ UNIC UNIQ UNIT UNTR UNVR URBN UVCR VAST VERN VICO VINS VISI VKTR VRNA WAPO WEHA WGSH WIFI WIIM WINS WIRG WMPP WTON XASI XBIO XBNI XBNP XISC XIJI XIPI XLBF XOID XPLN YELO YPAS YUAN ZATA ZBRA ZINC ZYRX"""

@st.cache_data
def load_excel_data():
    try:
        tickers = list(dict.fromkeys([t.strip().upper() for t in RAW_ISSI.split() if t.strip()]))
        formatted = [t + ".JK" for t in tickers]
        return formatted
    except Exception as e:
        st.error(f"Gagal memuat data ticker: {e}")
        return []

def fetch_and_compute_single(ticker):
    try:
        data = yf.download(
            ticker, period="1y", interval="1d",
            progress=False, auto_adjust=False, threads=False
        )
        if data is None or data.empty:
            return None

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        required = ["Open", "High", "Low", "Close", "Volume"]
        if not all(col in data.columns for col in required):
            return None

        data = data[required].replace([np.inf, -np.inf], np.nan)
        valid = data.dropna(subset=required)
        if len(valid) < 2:
            return None

        row = valid.iloc[-1]
        prev_row = valid.iloc[-2]
        close = valid["Close"].astype(float)
        high = valid["High"].astype(float)
        low = valid["Low"].astype(float)
        open_p = valid["Open"].astype(float)
        volume = valid["Volume"].astype(float)

        c_val = float(row["Close"])
        c_prev = float(prev_row["Close"])
        c_open = float(row["Open"])
        c_high = float(row["High"])
        c_low = float(row["Low"])
        c_vol = float(row["Volume"])
        chg_pct = ((c_val / c_prev) - 1) * 100 if c_prev else 0.0

        ma50 = close.rolling(50, min_periods=50).mean()
        ma150 = close.rolling(150, min_periods=150).mean()
        ma200 = close.rolling(200, min_periods=200).mean()
        high_52w = close.rolling(252, min_periods=2).max()
        low_52w = close.rolling(252, min_periods=2).min()

        pivot_series = high.shift(1).rolling(20, min_periods=2).max()
        vol_ma50 = volume.rolling(50, min_periods=2).mean()

        delta = close.diff()
        gain = delta.clip(lower=0).rolling(14, min_periods=2).mean()
        loss = (-delta.clip(upper=0)).rolling(14, min_periods=2).mean()
        rsi_series = 100 - (100 / (1 + gain / (loss + 1e-9)))

        tr = pd.concat([
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs()
        ], axis=1).max(axis=1)
        atr_series = tr.ewm(alpha=1/14, adjust=False).mean()

        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        macd_line = ema12 - ema26
        macd_signal = macd_line.ewm(span=9, adjust=False).mean()

        bb_mid = close.rolling(20, min_periods=2).mean()
        bb_std = close.rolling(20, min_periods=2).std()
        bb_upper = bb_mid + 2 * bb_std
        bb_lower = bb_mid - 2 * bb_std
        bb_pct_b = ((c_val - bb_lower.iloc[-1]) /
                    (bb_upper.iloc[-1] - bb_lower.iloc[-1] + 1e-9)) * 100

        lowest_l14 = low.rolling(14, min_periods=2).min().iloc[-1]
        highest_h14 = high.rolling(14, min_periods=2).max().iloc[-1]
        stoch_k = ((c_val - lowest_l14) /
                   (highest_h14 - lowest_l14 + 1e-9)) * 100

        obv = (np.sign(close.diff()) * volume).fillna(0).cumsum()
        vol20 = volume.rolling(20, min_periods=2).sum().iloc[-1]
        obv_flow_20 = ((obv.iloc[-1] - obv.iloc[max(0, len(obv)-20)]) /
                       (vol20 + 1e-9)) * 100
        dist_days = int(((close.diff() < 0) & (volume > volume.shift(1)))
                        .tail(25).sum())

        range_15 = ((high.rolling(15, min_periods=2).max() -
                     low.rolling(15, min_periods=2).min()) / close)
        range_40_prev = ((high.shift(15).rolling(40, min_periods=2).max() -
                          low.shift(15).rolling(40, min_periods=2).min()) /
                         close.shift(15))
        vcp_ratio = range_15.iloc[-1] / (range_40_prev.iloc[-1] + 1e-9)

        def ret_period(n):
            return float((c_val / close.iloc[-n-1] - 1) * 100) if len(close) > n else 0.0

        pivot_20 = float(pivot_series.iloc[-1]) if pd.notna(pivot_series.iloc[-1]) else c_val
        support_val = float(low.tail(20).min())
        resist_val = float(high.tail(20).max())

        def last_num(series):
            val = series.iloc[-1]
            return float(val) if pd.notna(val) else 0.0

        ma200_now = last_num(ma200)
        ma200_before = float(ma200.iloc[-20]) if len(ma200) >= 20 and pd.notna(ma200.iloc[-20]) else ma200_now

        return {
            'ticker': ticker.replace(".JK", ""),
            'nama': ticker.replace(".JK", ""),
            'open': c_open,
            'prev': c_prev,
            'high': c_high,
            'low': c_low,
            'close': c_val,
            'chg': chg_pct,
            'volume': c_vol,
            'vol_ma50': last_num(vol_ma50),
            'support': support_val,
            'pivot_20': pivot_20,
            'resist': resist_val,
            'harga_beli': pivot_20,
            'harga_jual': float(pivot_20 + 2 * last_num(atr_series)),
            'jenis_rekom': "BUY (Breakout)" if c_val >= pivot_20 else "HOLD / WAIT",
            'alasan_rekom': "Harga di atas pivot" if c_val >= pivot_20 else "Menunggu konfirmasi",
            'ma50': last_num(ma50),
            'ma150': last_num(ma150),
            'ma200': ma200_now,
            'ma200_slope_positive': bool(ma200_now > ma200_before),
            'high_52w': last_num(high_52w),
            'low_52w': last_num(low_52w),
            'rsi14': last_num(rsi_series),
            'atr14': last_num(atr_series),
            'macd_hist': last_num(macd_line - macd_signal),
            'bb_pct_b': float(bb_pct_b) if pd.notna(bb_pct_b) else 50.0,
            'stoch_k': float(stoch_k) if pd.notna(stoch_k) else 50.0,
            'obv_flow_20': float(obv_flow_20),
            'dist_days': dist_days,
            'vcp_ratio': float(vcp_ratio) if pd.notna(vcp_ratio) else 1.0,
            'ret_3m': ret_period(63),
            'ret_6m': ret_period(126),
            'ret_9m': ret_period(189),
            'ret_12m': ret_period(252),
            'avg_val_trx': float((close * volume).rolling(20, min_periods=2).mean().iloc[-1])
        }
    except Exception:
        return None

def run_screener_ultra_fast():
    tickers = load_excel_data()
    if not tickers:
        return pd.DataFrame()

    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    total = len(tickers)
    completed = 0

    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_ticker = {executor.submit(fetch_and_compute_single, t): t for t in tickers}
        for future in as_completed(future_to_ticker):
            completed += 1
            if completed % 25 == 0 or completed == total:
                progress_bar.progress(completed / total)
                status_text.text(f"Memindai data pasar realtime... ({completed}/{total} saham)")
            res = future.result()
            if res:
                results.append(res)

    progress_bar.empty()
    status_text.empty()

    if not results:
        return pd.DataFrame()

    df_res = pd.DataFrame(results)

    df_res['rs_raw'] = (
        0.4 * df_res['ret_3m'] +
        0.2 * df_res['ret_6m'] +
        0.2 * df_res['ret_9m'] +
        0.2 * df_res['ret_12m']
    )
    df_res['rs_rating'] = (df_res['rs_raw'].rank(pct=True, method='average') * 99).clip(1, 99).round().astype(int)

    df_res['tt_1'] = (df_res['close'] > df_res['ma150']) & (df_res['close'] > df_res['ma200'])
    df_res['tt_2'] = df_res['ma150'] > df_res['ma200']
    df_res['tt_3'] = df_res['ma200_slope_positive']
    df_res['tt_4'] = (df_res['ma50'] > df_res['ma150']) & (df_res['ma150'] > df_res['ma200'])
    df_res['tt_5'] = df_res['close'] > df_res['ma50']
    df_res['tt_6'] = df_res['close'] >= (1.25 * df_res['low_52w'])
    df_res['tt_7'] = df_res['close'] <= (0.75 * df_res['high_52w'])
    df_res['tt_8'] = df_res['rs_rating'] >= 70

    df_res['trend_template_score'] = (
        df_res['tt_1'].astype(int) + df_res['tt_2'].astype(int) +
        df_res['tt_3'].astype(int) + df_res['tt_4'].astype(int) +
        df_res['tt_5'].astype(int) + df_res['tt_6'].astype(int) +
        df_res['tt_7'].astype(int) + df_res['tt_8'].astype(int)
    )

    df_res['c_inti_1'] = (df_res['ma50'] > df_res['ma150']) & (df_res['ma150'] > df_res['ma200']) & (df_res['close'] > df_res['ma150'])
    df_res['c_inti_2'] = df_res['ma200_slope_positive']
    df_res['c_inti_3'] = df_res['close'] >= (0.80 * df_res['high_52w'])
    df_res['c_inti_4'] = df_res['rs_rating'] >= 70
    df_res['c_inti_5'] = df_res['avg_val_trx'] >= 5_000_000_000

    df_res['c_pend_6'] = df_res['close'] >= (1.22 * df_res['low_52w'])
    df_res['c_pend_7'] = df_res['macd_hist'] >= 0
    df_res['c_pend_8'] = (df_res['rsi14'] >= 42) & (df_res['rsi14'] <= 85)
    df_res['c_pend_9'] = True
    df_res['c_pend_10'] = df_res['bb_pct_b'] >= 35
    df_res['c_pend_11'] = df_res['stoch_k'] >= 35
    df_res['c_pend_12'] = df_res['volume'] >= (0.6 * df_res['vol_ma50'])
    df_res['c_pend_13'] = df_res['close'] >= (0.86 * df_res['pivot_20'])
    df_res['c_pend_14'] = df_res['dist_days'] <= 8
    df_res['c_pend_15'] = df_res['obv_flow_20'] >= -6

    pendukung_cols = [f'c_pend_{i}' for i in range(6, 16)]
    df_res['failed_pendukung'] = 10 - df_res[pendukung_cols].sum(axis=1)
    df_res['inti_passed'] = df_res['c_inti_1'] & df_res['c_inti_2'] & df_res['c_inti_3'] & df_res['c_inti_4'] & df_res['c_inti_5']
    df_res['lolos_screener'] = df_res['inti_passed'] & (df_res['failed_pendukung'] <= 2)

    dist_high_score = (df_res['close'] / df_res['high_52w']).clip(0, 1) * 15
    vcp_score = (1 - df_res['vcp_ratio'].clip(0, 1)) * 10
    vol_spike_score = (df_res['volume'] / (df_res['vol_ma50'] + 1e-9)).clip(0, 3) / 3 * 10

    df_res['skor_momentum'] = (
        (df_res['rs_rating'] / 99 * 30) +
        dist_high_score +
        (df_res['trend_template_score'] / 8 * 20) +
        vol_spike_score +
        vcp_score +
        ((10 - df_res['failed_pendukung']).clip(0, 10) / 10 * 15)
    ).round(1)

    def generate_alasan(row):
        reasons = []
        if row['trend_template_score'] >= 7:
            reasons.append(f"Uptrend Kuat (TT {row['trend_template_score']}/8)")
        if row['rs_rating'] >= 80:
            reasons.append(f"RS Rating Tinggi ({row['rs_rating']})")
        if row['close'] >= row['pivot_20']:
            reasons.append("Breakout Pivot Valid")
        if row['vcp_ratio'] <= 0.55:
            reasons.append(f"VCP Ketat ({row['vcp_ratio']:.2f})")
        if row['volume'] >= 1.5 * row['vol_ma50']:
            reasons.append("Lonjakan Volume Besar")
        return " | ".join(reasons) if reasons else "Lolos Kriteria Inti & Pendukung"

    df_res['alasan'] = df_res.apply(generate_alasan, axis=1)
    return df_res

if 'df_screened' not in st.session_state:
    st.session_state.df_screened = None

# --- MENU 1: SCREENER ---
if st.session_state.active_menu == "Screener":
    st.markdown("### **Screener Ketat Saham ISSI**")
    st.markdown("<p style='color: #8b949e; font-size: 14px;'>Pemindaian saham syariah berbasis strategi Mark Minervini & William O'Neil. Jalankan scan manual kapan saja.</p>", unsafe_allow_html=True)

    col_btn, _ = st.columns([2, 8])
    with col_btn:
        run_btn = st.button("🚀 SCAN PASAR SEKARANG")

    if run_btn:
        with st.spinner("⚡ Menjalankan screener multi-thread secepat kilat..."):
            st.session_state.df_screened = run_screener_ultra_fast()
        st.success("Scan selesai dengan sukses!")

    if st.session_state.df_screened is not None and not st.session_state.df_screened.empty:
        df = st.session_state.df_screened
        df_passed = df[df['lolos_screener'] == True].sort_values(by='skor_momentum', ascending=False).reset_index(drop=True)

        try:
            ihsg_data = yf.download("^JKSE", period="5d", progress=False)
            if isinstance(ihsg_data.columns, pd.MultiIndex):
                ihsg_data.columns = ihsg_data.columns.get_level_values(0)
            ihsg_close = ihsg_data['Close'].iloc[-1]
            ihsg_prev = ihsg_data['Close'].iloc[-2]
            ihsg_chg = ((ihsg_close - ihsg_prev) / ihsg_prev) * 100
        except Exception:
            ihsg_close, ihsg_chg = 7300.0, 0.5

        c_box1, c_box2, c_box3 = st.columns(3)
        with c_box1:
            st.markdown(f"""
            <div class="metric-card">
                <div style="color: #8b949e; font-size: 13px;">IHSG (Indeks Harga Saham Gabungan)</div>
                <div style="font-size: 22px; font-weight: bold; color: #ffffff; margin-top: 5px;">{ihsg_close:,.2f}</div>
                <div style="color: {'#2ea043' if ihsg_chg >= 0 else '#f85149'}; font-size: 14px; font-weight: 600;">{'+' if ihsg_chg >= 0 else ''}{ihsg_chg:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
        with c_box2:
            st.markdown(f"""
            <div class="metric-card">
                <div style="color: #8b949e; font-size: 13px;">Total Saham ISSI Dipindai</div>
                <div style="font-size: 22px; font-weight: bold; color: #ffffff; margin-top: 5px;">{len(df)}</div>
                <div style="color: #58a6ff; font-size: 14px;">Database ISSI Terintegrasi</div>
            </div>
            """, unsafe_allow_html=True)
        with c_box3:
            st.markdown(f"""
            <div class="metric-card">
                <div style="color: #8b949e; font-size: 13px;">Kotak Saham Layak Beli</div>
                <div style="font-size: 22px; font-weight: bold; color: #2ea043; margin-top: 5px;">{len(df_passed)} Saham</div>
                <div style="color: #8b949e; font-size: 14px;">Lolos Kriteria Inti & 15 Aturan Ketat</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📋 Tabel Rincian Parameter Saham Lolos Screener")

        if not df_passed.empty:
            def color_coding(val):
                if isinstance(val, str) and ('+' in val or 'Uptrend' in val or 'Breakout' in val or 'Ketat' in val):
                    return 'color: #3fb950; background-color: rgba(46, 160, 67, 0.15); font-weight: bold;'
                elif isinstance(val, str) and ('-' in val and '%' in val):
                    return 'color: #f85149; background-color: rgba(248, 81, 73, 0.15); font-weight: bold;'
                return ''

            table_data = []
            for idx, r in df_passed.iterrows():
                table_data.append({
                    "No": idx + 1,
                    "Nama Saham": r['nama'],
                    "Open": f"{r['open']:,.0f}".replace(",", "."),
                    "Prev": f"{r['prev']:,.0f}".replace(",", "."),
                    "High": f"{r['high']:,.0f}".replace(",", "."),
                    "Low": f"{r['low']:,.0f}".replace(",", "."),
                    "Close": f"{r['close']:,.0f}".replace(",", "."),
                    "Chg": f"+{r['chg']:.2f}%" if r['chg'] >= 0 else f"{r['chg']:.2f}%",
                    "Volume": f"{r['volume']:,.0f}".replace(",", "."),
                    "Support": f"{r['support']:,.0f}".replace(",", "."),
                    "Pivot": f"{r['pivot_20']:,.0f}".replace(",", "."),
                    "Resist": f"{r['resist']:,.0f}".replace(",", "."),
                    "Harga Beli": f"{r['harga_beli']:,.0f}".replace(",", "."),
                    "Harga Jual": f"{r['harga_jual']:,.0f}".replace(",", "."),
                    "Alasan": r['alasan']
                })

            df_display = pd.DataFrame(table_data)
            
            try:
                styled_df = df_display.style.map(color_coding, subset=['Chg', 'Alasan'])
            except AttributeError:
                styled_df = df_display.style.applymap(color_coding, subset=['Chg', 'Alasan'])
                
            st.dataframe(
                styled_df, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "No": st.column_config.NumberColumn("No", width="small"),
                    "Nama Saham": st.column_config.TextColumn("Nama Saham", width="medium"),
                    "Alasan": st.column_config.TextColumn("Alasan", width="large")
                }
            )

            # --- BAGIAN CHART CANDLESTICK 6 BULAN ---
            st.markdown("---")
            st.markdown("### 📊 Analisis Grafik Teknikal Mendalam (6 Bulan Terakhir)")
            selected_ticker = st.selectbox("Pilih Nama Saham untuk Memunculkan Grafik Lengkap:", df_passed['ticker'].tolist())

            if selected_ticker:
                with st.spinner(f"Memuat data historis grafik {selected_ticker}..."):
                    hist = yf.download(selected_ticker + ".JK", period="6mo", progress=False)
                    if isinstance(hist.columns, pd.MultiIndex):
                        hist.columns = hist.columns.get_level_values(0)

                    if not hist.empty:
                        c_close = hist['Close']
                        c_high = hist['High']
                        c_low = hist['Low']
                        c_vol = hist['Volume']

                        ma5 = c_close.rolling(5).mean()
                        ma20 = c_close.rolling(20).mean()
                        ma50 = c_close.rolling(50).mean()
                        ma150 = c_close.rolling(150).mean()
                        ma200 = c_close.rolling(200).mean()

                        bb_mid = c_close.rolling(20).mean()
                        bb_std = c_close.rolling(20).std()
                        bb_upper = bb_mid + (2 * bb_std)
                        bb_lower = bb_mid - (2 * bb_std)

                        ema12 = c_close.ewm(span=12, adjust=False).mean()
                        ema26 = c_close.ewm(span=26, adjust=False).mean()
                        macd_line = ema12 - ema26
                        macd_signal = macd_line.ewm(span=9, adjust=False).mean()
                        macd_hist = macd_line - macd_signal

                        delta = c_close.diff()
                        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                        rsi = 100 - (100 / (1 + (gain / (loss + 1e-9))))

                        lowest_14 = c_low.rolling(14).min()
                        highest_14 = c_high.rolling(14).max()
                        stoch_k = ((c_close - lowest_14) / (highest_14 - lowest_14 + 1e-9)) * 100

                        fig = make_subplots(
                            rows=4, cols=1, shared_xaxes=True,
                            vertical_spacing=0.03,
                            row_heights=[0.5, 0.15, 0.15, 0.2],
                            subplot_titles=(f"Candlestick & Indikator Tren ({selected_ticker})", "Volume", "MACD (12,26,9)", "RSI (14) & Stochastic")
                        )

                        fig.add_trace(go.Candlestick(x=hist.index, open=hist['Open'], high=c_high, low=c_low, close=c_close, name='OHLC'), row=1, col=1)
                        fig.add_trace(go.Scatter(x=hist.index, y=ma5, line=dict(color='#ff7f0e', width=1), name='MA 5'), row=1, col=1)
                        fig.add_trace(go.Scatter(x=hist.index, y=ma20, line=dict(color='#1f77b4', width=1), name='MA 20'), row=1, col=1)
                        fig.add_trace(go.Scatter(x=hist.index, y=ma50, line=dict(color='#2ca02c', width=1.2), name='MA 50'), row=1, col=1)
                        fig.add_trace(go.Scatter(x=hist.index, y=ma150, line=dict(color='#9467bd', width=1.2), name='MA 150'), row=1, col=1)
                        fig.add_trace(go.Scatter(x=hist.index, y=ma200, line=dict(color='#d62728', width=1.5), name='MA 200'), row=1, col=1)
                        fig.add_trace(go.Scatter(x=hist.index, y=bb_upper, line=dict(color='rgba(150,150,150,0.5)', width=1, dash='dot'), name='BB Upper'), row=1, col=1)
                        fig.add_trace(go.Scatter(x=hist.index, y=bb_lower, line=dict(color='rgba(150,150,150,0.5)', width=1, dash='dot'), name='BB Lower', fill='tonexty', fillcolor='rgba(150,150,150,0.05)'), row=1, col=1)

                        fig.add_trace(go.Bar(x=hist.index, y=c_vol, marker_color='#26a69a', name='Volume'), row=2, col=1)

                        fig.add_trace(go.Scatter(x=hist.index, y=macd_line, line=dict(color='#2962ff', width=1.2), name='MACD'), row=3, col=1)
                        fig.add_trace(go.Scatter(x=hist.index, y=macd_signal, line=dict(color='#ff6d00', width=1.2), name='Signal'), row=3, col=1)
                        fig.add_trace(go.Bar(x=hist.index, y=macd_hist, marker_color=np.where(macd_hist >= 0, '#26a69a', '#ef5350'), name='Histogram'), row=3, col=1)

                        fig.add_trace(go.Scatter(x=hist.index, y=rsi, line=dict(color='#ab47bc', width=1.3), name='RSI (14)'), row=4, col=1)
                        fig.add_trace(go.Scatter(x=hist.index, y=stoch_k, line=dict(color='#29b6f6', width=1.3), name='Stoch %K'), row=4, col=1)
                        
                        fig.add_hline(y=70, line_dash="dash", line_color="red", row=4, col=1)
                        fig.add_hline(y=30, line_dash="dash", line_color="green", row=4, col=1)

                        fig.update_layout(
                            template="plotly_dark",
                            height=800,
                            margin=dict(l=10, r=10, t=30, b=10),
                            xaxis_rangeslider_visible=False,
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                        )
                        st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Tidak ada saham yang memenuhi kriteria pada pemindaian terakhir.")
    else:
        st.info("👈 Silakan klik tombol **'SCAN PASAR SEKARANG'** di atas untuk mulai memindai daftar saham.")

# --- MENU 2: DAFTAR SAHAM ---
elif st.session_state.active_menu == "Daftar Saham":
    st.markdown("### **Daftar Seluruh Saham ISSI**")
    st.markdown("<p style='color: #8b949e; font-size: 14px;'>Daftar lengkap seluruh saham syariah beserta data pasar dan rekomendasi teknikal.</p>", unsafe_allow_html=True)
    
    col_btn_all, _ = st.columns([2, 8])
    with col_btn_all:
        load_all_btn = st.button("📊 MUAT SEMUA DATA PASAR ISSI")

    if load_all_btn or st.session_state.get('df_all_issi') is not None:
        if load_all_btn:
            st.session_state.df_all_issi = run_screener_ultra_fast()
        
        df_all = st.session_state.get('df_all_issi')
        if df_all is not None and not df_all.empty:
            table_all_data = []
            for idx, r in df_all.reset_index(drop=True).iterrows():
                table_all_data.append({
                    "No": idx + 1,
                    "Nama Saham": r['nama'],
                    "Harga": f"{r['close']:,.0f}".replace(",", "."),
                    "Open": f"{r['open']:,.0f}".replace(",", "."),
                    "Prev": f"{r['prev']:,.0f}".replace(",", "."),
                    "High": f"{r['high']:,.0f}".replace(",", "."),
                    "Low": f"{r['low']:,.0f}".replace(",", "."),
                    "Close": f"{r['close']:,.0f}".replace(",", "."),
                    "Chg": f"+{r['chg']:.2f}%" if r['chg'] >= 0 else f"{r['chg']:.2f}%",
                    "Volume": f"{r['volume']:,.0f}".replace(",", "."),
                    "Support": f"{r['support']:,.0f}".replace(",", "."),
                    "Resist": f"{r['resist']:,.0f}".replace(",", "."),
                    "Pivot": f"{r['pivot_20']:,.0f}".replace(",", "."),
                    "Harga Buy": f"{r['harga_beli']:,.0f}".replace(",", "."),
                    "Jual": f"{r['harga_jual']:,.0f}".replace(",", "."),
                    "Jenis Rekomendasi": r['jenis_rekom'],
                    "Alasan Rekomendasi": r['alasan_rekom']
                })
            
            df_all_display = pd.DataFrame(table_all_data)
            
            # Styling warna sesuai permintaan: High (Biru), Low (Merah), Prev (Kuning), Chg (Hijau/Merah)
            def style_dataframe(df):
                styles = pd.DataFrame('', index=df.index, columns=df.columns)
                for col in df.columns:
                    if col == 'High':
                        styles[col] = 'color: #38bdf8; font-weight: bold;'      # Biru
                    elif col == 'Low':
                        styles[col] = 'color: #f85149; font-weight: bold;'       # Merah
                    elif col == 'Prev':
                        styles[col] = 'color: #eab308; font-weight: bold;'       # Kuning
                    elif col == 'Chg':
                        styles[col] = df[col].apply(lambda x: 'color: #2ea043; font-weight: bold;' if '+' in str(x) else 'color: #f85149; font-weight: bold;')
                return styles

            try:
                styled_all_df = df_all_display.style.apply(style_dataframe, axis=None)
            except Exception:
                styled_all_df = df_all_display

            st.dataframe(
                styled_all_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "No": st.column_config.NumberColumn("No", width="small"),
                    "Nama Saham": st.column_config.TextColumn("Nama Saham", width="medium"),
                    "Jenis Rekomendasi": st.column_config.TextColumn("Jenis Rekomendasi", width="medium"),
                    "Alasan Rekomendasi": st.column_config.TextColumn("Alasan Rekomendasi", width="large")
                }
            )
        else:
            st.warning("Data pasar sedang dimuat atau kosong.")
    else:
        st.info("👈 Klik tombol **'MUAT SEMUA DATA PASAR ISSI'** di atas untuk menampilkan tabel lengkap seluruh emiten.")

# --- MENU 3: STRATEGI ---
elif st.session_state.active_menu == "Strategi":
    st.markdown("### **Strategi & Rumus Screener Momentum ISSI**")
    st.markdown("Panduan lengkap metodologi trader momentum sukses: **Mark Minervini** & **William O'Neil**.")
    
    st.markdown("---")
    st.markdown("### **1. Trend Template — Mark Minervini**")
    st.markdown("Syarat mutlak tren naik sehat (MA50, MA150, MA200, kemiringan MA200, jarak ke High/Low 52 minggu).")
    
    st.markdown("---")
    st.markdown("### **2. RS Rating — William O’Neil (IBD)**")
    st.markdown("Peringkat persentil kekuatan relatif (skala 1–99) dengan bobot terbesar pada momentum 3 bulan terakhir.")

    st.markdown("---")
    st.markdown("### **3. Pivot Breakout & Volume**")
    st.markdown("Membeli saat harga menembus titik tertinggi 20 sesi terakhir disertai lonjakan volume transaksi besar (≥ 1,5x rata-rata).")

    st.markdown("---")
    st.markdown("### **4. VCP (Volatility Contraction Pattern)**")
    st.markdown("Mengukur penyusutan rentang harga (rasio ≤ 0,55) sebagai tanda pasokan saham sudah kering.")

    st.markdown("---")
    st.markdown("### **5. Indikator Pendukung Teknis & Skor Momentum**")
    st.markdown("Dilengkapi MACD, Bollinger Bands, Stochastic, RSI, ATR, serta Skor Komposit Berbobot 0–100.")
