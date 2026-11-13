import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime

st.set_page_config(page_title="ISSI Pro Screener", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")

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
        res = requests.post(f"https://telegram.org{bot_token}/sendMessage", json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=10)
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
                        df_t = data[t].dropna(subset=['Close'])
                        if len(df_t) >= 30:
                            all_dfs[t] = df_t
                except Exception:
                    continue
        except Exception:
            continue
    return all_dfs

def scan_issi_stocks(tickers, strategy_mode, modal_trading, risk_pct, sl_mult, tp_mult):
    with st.spinner("⚡ Memindai 574+ saham ISSI secara batch (8-12 detik)..."):
        market_data = fetch_all_issi_market_data(tickers)
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
