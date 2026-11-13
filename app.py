import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
from datetime import datetime

st.set_page_config(
    page_title="ISSI Pro Screener & Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main {background-color: #0E1117;}
    div[data-testid="metric-container"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATABASE SAHAM ISSI LENGKAP (574+ EMITEN)
# ---------------------------------------------------------
EXCEL_ISSI_TICKERS = [
    "AADI.JK", "AALI.JK", "ABMM.JK", "ACES.JK", "ADCP.JK", "ADES.JK", "ADMG.JK", "ADMR.JK", "ADRO.JK", "AGAR.JK",
    "AGII.JK", "AIMS.JK", "AKKU.JK", "AKPI.JK", "AKRA.JK", "AKSI.JK", "ALAN.JK", "ALDO.JK", "AMAN.JK", "AMAR.JK",
    "AMFG.JK", "AMIN.JK", "AMMN.JK", "AMOR.JK", "ANJT.JK", "ANTM.JK", "APEX.JK", "APIC.JK", "APLI.JK", "ARCI.JK",
    "ARKA.JK", "ARKO.JK", "ARNA.JK", "ARTA.JK", "ARTI.JK", "ASBI.JK", "ASDM.JK", "ASII.JK", "ASJT.JK", "ASRI.JK",
    "ATAP.JK", "ATIC.JK", "AUTO.JK", "AVIA.JK", "AXIO.JK", "BABP.JK", "BAJA.JK", "BALI.JK", "BANK.JK", "BAPI.JK",
    "BATA.JK", "BAUT.JK", "BAYU.JK", "BBCA.JK", "BBHI.JK", "BBKP.JK", "BBMD.JK", "BBNI.JK", "BBRI.JK", "BBSI.JK",
    "BBTN.JK", "BBYB.JK", "BCIC.JK", "BDMN.JK", "BEBS.JK", "BEEF.JK", "BEER.JK", "BELI.JK", "BESS.JK", "BEST.JK",
    "BFIN.JK", "BGTG.JK", "BHIT.JK", "BIKA.JK", "BINA.JK", "BINO.JK", "BIPI.JK", "BIRD.JK", "BISI.JK", "BITO.JK",
    "BJBR.JK", "BJTM.JK", "BKDP.JK", "BKSL.JK", "BLTA.JK", "BLTZ.JK", "BLUE.JK", "BMAS.JK", "BMHS.JK", "BMRI.JK",
    "BMSR.JK", "BMTR.JK", "BNBA.JK", "BNGA.JK", "BNII.JK", "BNLI.JK", "BOBA.JK", "BOGA.JK", "BOLA.JK", "BOLT.JK",
    "BPTR.JK", "BRAM.JK", "BREN.JK", "BRIS.JK", "BRMS.JK", "BRNA.JK", "BSBK.JK", "BSDE.JK", "BSML.JK", "BSSR.JK",
    "BSWD.JK", "BTPS.JK", "BUAH.JK", "BUDI.JK", "BUKK.JK", "BULL.JK", "BUMI.JK", "BUVA.JK", "BVIC.JK", "BWPT.JK",
    "BYAN.JK", "CAKK.JK", "CAMP.JK", "CARS.JK", "CASA.JK", "CASH.JK", "CASS.JK", "CBRE.JK", "CBUT.JK", "CCSI.JK",
    "CEKA.JK", "CENT.JK", "CFIN.JK", "CGAS.JK", "CHEK.JK", "CINT.JK", "CITA.JK", "CITY.JK", "CLPI.JK", "CMNP.JK",
    "CMPP.JK", "CMRY.JK", "CNKO.JK", "CNTX.JK", "COCO.JK", "CPIN.JK", "CRAB.JK", "CSIS.JK", "CSMI.JK", "CSRA.JK",
    "CTBN.JK", "CTRA.JK", "CUAN.JK", "DADA.JK", "DATA.JK", "DANA.JK", "DEAL.JK", "DEWI.JK", "DFAM.JK", "DGIK.JK",
    "DGNS.JK", "DIDX.JK", "DIRA.JK", "DMMX.JK", "DNAR.JK", "DOID.JK", "DPNS.JK", "DRMA.JK", "DSFI.JK", "DSNG.JK",
    "DSSA.JK", "DUCK.JK", "DWGL.JK", "EAST.JK", "ECII.JK", "EDGE.JK", "EDIN.JK", "EKAD.JK", "ELIT.JK", "ELSA.JK",
    "ELPI.JK", "EMDE.JK", "ENAK.JK", "ENRG.JK", "ENZO.JK", "EPAC.JK", "EPMT.JK", "ERAA.JK", "ERTX.JK", "ESIP.JK",
    "ESSA.JK", "ESTA.JK", "ESTI.JK", "ETWA.JK", "EXCL.JK", "FAPA.JK", "FASW.JK", "FILM.JK", "FIMP.JK", "FIRE.JK",
    "FISH.JK", "FPNI.JK", "FREN.JK", "FUTR.JK", "FWCT.JK", "GAMA.JK", "GATE.JK", "GBKA.JK", "GEMA.JK", "GEMS.JK",
    "GGRM.JK", "GGRP.JK", "GHON.JK", "GIAA.JK", "GJTL.JK", "GLVA.JK", "GMFI.JK", "GMTD.JK", "GOLD.JK", "GOLF.JK",
    "GOOD.JK", "GPRA.JK", "GPSO.JK", "GRPH.JK", "GTBO.JK", "GTSI.JK", "GULA.JK", "GZCO.JK", "HADE.JK", "HAIS.JK",
    "HALO.JK", "HATM.JK", "HDIT.JK", "HEAL.JK", "HELI.JK", "HERO.JK", "HEXA.JK", "HITS.JK", "HKMU.JK", "HMSP.JK",
    "HOKI.JK", "HOME.JK", "HOMI.JK", "HOPE.JK", "HRME.JK", "HRTA.JK", "IATA.JK", "IBFN.JK", "IBOS.JK", "ICBP.JK",
    "ICON.JK", "IDEA.JK", "IDPR.JK", "IFII.JK", "IFSH.JK", "IGAR.JK", "IIKF.JK", "IMAS.JK", "IMJS.JK", "IMPC.JK",
    "INCO.JK", "INDF.JK", "INDS.JK", "INKP.JK", "INPC.JK", "INPP.JK", "INPS.JK", "INRU.JK", "INTA.JK", "INTD.JK",
    "INTP.JK", "IOSP.JK", "IPCC.JK", "IPCM.JK", "IPEH.JK", "IPOL.JK", "IPPE.JK", "ISAT.JK", "ISSP.JK", "ITMA.JK",
    "ITMG.JK", "JATI.JK", "JAWA.JK", "JAYA.JK", "JECC.JK", "JGLE.JK", "JKON.JK", "JMAS.JK", "JPFA.JK", "JSMR.JK",
    "JSPT.JK", "JTPE.JK", "KAEF.JK", "KARW.JK", "KAYU.JK", "KEEN.JK", "KEIS.JK", "KELN.JK", "KDTN.JK", "KEJU.JK",
    "KICI.JK", "KIJA.JK", "KINO.JK", "KJEN.JK", "KKGI.JK", "KLBF.JK", "KMDS.JK", "KOBX.JK", "KOIN.JK", "KOKA.JK",
    "KONI.JK", "KOPI.JK", "KOTA.JK", "KPIG.JK", "KRAK.JK", "LABS.JK", "LAJU.JK", "LAND.JK", "LAPD.JK", "LCKM.JK",
    "LEAD.JK", "LFLO.JK", "LIFE.JK", "LINK.JK", "LION.JK", "LMPI.JK", "LMSH.JK", "LPCK.JK", "LPGI.JK", "LPIN.JK",
    "LPPF.JK", "LPPS.JK", "LPTA.JK", "LRNA.JK", "LSIP.JK", "LUCK.JK", "LUCY.JK", "MABA.JK", "MAGP.JK", "MAIN.JK",
    "MAMI.JK", "MAPA.JK", "MAPI.JK", "MARI.JK", "MARK.JK", "MASB.JK", "MAYA.JK", "MBAP.JK", "MBMA.JK", "MBSS.JK",
    "MBTO.JK", "MCAS.JK", "MDKA.JK", "MEDC.JK", "MEGA.JK", "MENN.JK", "MERK.JK", "META.JK", "MFMI.JK", "MGLV.JK",
    "MICE.JK", "MIDI.JK", "MIKA.JK", "MINA.JK", "MIRA.JK", "MITI.JK", "MKNT.JK", "MKPI.JK", "MLIA.JK", "MLPL.JK",
    "MLPT.JK", "MMIX.JK", "MMLP.JK", "MNCN.JK", "MOLI.JK", "MPPA.JK", "MPXL.JK", "MRAT.JK", "MREI.JK", "MSIN.JK",
    "MSKY.JK", "MTDL.JK", "MTEL.JK", "MTMH.JK", "MTSM.JK", "MUTU.JK", "MYOH.JK", "NANO.JK", "NICK.JK", "NELY.JK",
    "NEMI.JK", "NEST.JK", "NFCX.JK", "NINE.JK", "NLIQ.JK", "NOBU.JK", "NPGF.JK", "NSSS.JK", "NUSA.JK", "NZIA.JK",
    "OASA.JK", "OBMD.JK", "OCAP.JK", "OKAS.JK", "OLIV.JK", "OMRE.JK", "PADA.JK", "PADI.JK", "PALM.JK", "PAMG.JK",
    "PANI.JK", "PARA.JK", "PATK.JK", "PBLE.JK", "PBID.JK", "PBRX.JK", "PDES.JK", "PEHA.JK", "PEVE.JK", "PGAS.JK",
    "PGEO.JK", "PGLI.JK", "PGUN.JK", "PICO.JK", "PJAA.JK", "PKPK.JK", "PLAS.JK", "PLIN.JK", "PMJS.JK", "PNBN.JK",
    "PNBS.JK", "PNGO.JK", "PNIN.JK", "PNSE.JK", "POLA.JK", "POLI.JK", "POLL.JK", "POLY.JK", "POOL.JK", "PORT.JK",
    "POSA.JK", "POWR.JK", "PPRO.JK", "PRAS.JK", "PSAB.JK", "PSDN.JK", "PSGO.JK", "PSSI.JK", "PTBA.JK", "PTDU.JK",
    "PUDP.JK", "PURA.JK", "PURE.JK", "PWON.JK", "PYFA.JK", "PZZA.JK", "RAAM.JK", "RAJA.JK", "RANC.JK", "RBMS.JK",
    "RDTX.JK", "REAL.JK", "RELF.JK", "RICY.JK", "RIGS.JK", "RISE.JK", "RMKE.JK", "ROCK.JK", "ROTI.JK", "RUIS.JK",
    "RUNS.JK", "SAFE.JK", "SAGE.JK", "SAID.JK", "SAME.JK", "SAMF.JK", "SAPX.JK", "SATU.JK", "SBAT.JK", "SBMA.JK",
    "SCCO.JK", "SCMA.JK", "SCNP.JK", "SCPI.JK", "SDPC.JK", "SDRA.JK", "SEMA.JK", "SGER.JK", "SGRO.JK", "SHIP.JK",
    "SICO.JK", "SIDO.JK", "SILO.JK", "SIMA.JK", "SIMP.JK", "SKLT.JK", "SKRN.JK", "SKYB.JK", "SMIK.JK", "SMIL.JK",
    "SMKM.JK", "SMMA.JK", "SMMT.JK", "SMRA.JK", "SMRU.JK", "SMSM.JK", "SNLK.JK", "SOCI.JK", "SOFA.JK", "SONA.JK",
    "SPMA.JK", "SPTO.JK", "SQMI.JK", "SRAJ.JK", "SRTG.JK", "SSIA.JK", "SOSS.JK", "SSTM.JK", "STAA.JK", "STAR.JK",
    "STRK.JK", "STTP.JK", "SULI.JK", "SUNI.JK", "SUPR.JK", "SURE.JK", "SURI.JK", "SWID.JK", "TALF.JK", "TAMA.JK",
    "TAMU.JK", "TAPG.JK", "TARA.JK", "TAXI.JK", "TBMS.JK", "TCPI.JK", "TEBE.JK", "TECH.JK", "TEGH.JK", "TELE.JK",
    "TFAS.JK", "TGKA.JK", "TIFA.JK", "TINS.JK", "TIRA.JK", "TIRT.JK", "TKIM.JK", "TLKM.JK", "TMAS.JK", "TMPO.JK",
    "TOBA.JK", "TOOL.JK", "TOWR.JK", "TPIA.JK", "TPMA.JK", "TRAM.JK", "TRIN.JK", "TRIS.JK", "TRJA.JK", "TRON.JK",
    "TRUK.JK", "TSPC.JK", "TUGU.JK", "TYRE.JK", "UANG.JK", "ULTJ.JK", "UNIC.JK", "UNIQ.JK", "UNIT.JK", "UNTR.JK",
    "UNVR.JK", "URBN.JK", "UVCR.JK", "VAST.JK", "VERN.JK", "VICO.JK", "VINS.JK", "VISI.JK", "VKTR.JK", "VRNA.JK",
    "WAPO.JK", "WEHA.JK", "WGSH.JK", "WIFI.JK", "WIIM.JK", "WINS.JK", "WIRG.JK", "WMPP.JK", "WTON.JK", "XASI.JK",
    "XBIO.JK", "XBNI.JK", "XBNP.JK", "XISC.JK", "XIJI.JK", "XIPI.JK", "XLBF.JK", "XOID.JK", "XPLN.JK", "YELO.JK",
    "YPAS.JK", "YUAN.JK", "ZATA.JK", "ZBRA.JK", "ZINC.JK", "ZYRX.JK"
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

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        res = requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=10)
        if res.status_code == 200:
            return True, "Sinyal berhasil dikirim ke Telegram!"
        return False, f"Gagal mengirim: {res.text}"
    except Exception as e:
        return False, f"Error koneksi: {str(e)}"

@st.cache_data(ttl=1800)
def scan_issi_stocks(tickers_tuple, strategy_mode, modal_trading, risk_pct, sl_mult, tp_mult):
    results = []
    progress_bar = st.progress(0)
    total = len(tickers_tuple)
    max_risk_rp = modal_trading * (risk_pct / 100.0)

    for i, ticker in enumerate(tickers_tuple):
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period="6mo") # Menggunakan 6 bulan agar lebih cepat & stabil di HP
            if len(df) < 20:
                progress_bar.progress((i + 1) / total)
                continue

            df = calculate_indicators(df)
            latest = df.iloc[-1]
            prev = df.iloc[-2]
            pct_change = ((latest['Close'] - prev['Close']) / prev['Close']) * 100

            entry_price = round_idx_tick(latest['Close'])
            sl_price = max(50, round_idx_tick(entry_price - (sl_mult * latest.get('ATR', entry_price * 0.05))))
            tp_price = round_idx_tick(entry_price + (tp_mult * latest.get('ATR', entry_price * 0.05))))

            risk_per_share = max(1, entry_price - sl_price)
            rr_ratio = round(max(0, tp_price - entry_price) / risk_per_share, 2)
            suggested_lots = max(1, int((max_risk_rp / risk_per_share) // 100))
            if (suggested_lots * 100 * entry_price) > modal_trading:
                suggested_lots = max(0, int(modal_trading // (100 * entry_price)))

            # Safe fetch fundamentals
            try:
                info = stock.info
                per = info.get('trailingPE', np.nan)
                pbv = info.get('priceToBook', np.nan)
                roe = info.get('returnOnEquity', np.nan)
                if pd.notna(roe):
                    roe = roe * 100
            except Exception:
                per, pbv, roe = np.nan, np.nan, np.nan

            rvol_val = latest.get('RVOL', 1.0)
            if pd.isna(rvol_val):
                rvol_val = 1.0
            rsi_val = latest.get('RSI', 50.0)
            if pd.isna(rsi_val):
                rsi_val = 50.0
            ema20_val = latest.get('EMA20', latest['Close'])
            sma50_val = latest.get('SMA50', latest['Close'])
            macd_val = latest.get('MACD', 0.0)
            signal_val = latest.get('Signal', 0.0)

            row_data = {
                'Kode': ticker.replace(".JK", ""),
                'Harga': entry_price,
                'Perubahan (%)': round(pct_change, 2),
                'Stop Loss': sl_price,
                'Target Profit': tp_price,
                'Risk/Reward': rr_ratio,
                'Saran Lot': suggested_lots,
                'RVOL (x)': round(rvol_val, 2),
                'RSI (14)': round(rsi_val, 1),
                'EMA20': round(ema20_val, 0),
                'SMA50': round(sma50_val, 0),
                'MACD': round(macd_val, 2),
                'Signal': round(signal_val, 2),
                'PER (x)': round(per, 2) if pd.notna(per) else None,
                'PBV (x)': round(pbv, 2) if pd.notna(pbv) else None,
                'ROE (%)': round(roe, 2) if pd.notna(roe) else None,
                'Close': latest['Close']
            }

            rec, score, reason = generate_recommendation(row_data)
            row_data['Rekomendasi'] = rec
            row_data['Skor'] = score
            row_data['Alasan Sinyal'] = reason

            # Evaluasi Strategi
            if strategy_mode == "Semua Saham ISSI":
                results.append(row_data)
            elif strategy_mode == "Swing Trading (Uptrend + Momentum)":
                if row_data['Close'] > row_data['EMA20'] and 40 <= row_data['RSI (14)'] <= 68 and row_data['MACD'] > row_data['Signal']:
                    results.append(row_data)
            elif strategy_mode == "Bandarmologi / Volume Spike":
                if row_data['RVOL (x)'] >= 1.5 and pct_change > 0:
                    results.append(row_data)
            elif strategy_mode == "Value Investing Syariah (Murah & Sehat)":
                if (pd.notna(per) and 0 < per <= 15) and (pd.notna(pbv) and pbv <= 1.5):
                    results.append(row_data)
            elif strategy_mode == "BSJP (Beli Sore Jual Pagi)":
                if pct_change >= 2.0 and row_data['RVOL (x)'] >= 1.3 and row_data['Close'] > row_data['EMA20']:
                    results.append(row_data)
        except Exception:
            pass
        progress_bar.progress((i + 1) / total)

    progress_bar.empty()
    return pd.DataFrame(results)

# ---------------------------------------------------------
# TAMPILAN UTAMA
# ---------------------------------------------------------
ihsg_price, ihsg_chg, ihsg_pct = get_ihsg_data()
col_title, col_ihsg = st.columns([3, 1])
with col_title:
    st.title("🕌 ISSI Pro Stock Screener")
    st.caption("Penyaring Saham Syariah BEI + Kalkulator Manajemen Risiko ATR + Alert Telegram")
with col_ihsg:
    st.metric("📊 IHSG", f"{ihsg_price:,.2f}", f"{ihsg_chg:+.2f} ({ihsg_pct:+.2f}%)")

st.divider()

st.subheader("⚙️ Panel Kontrol & Pengaturan Strategi")
c_menu, c_strat = st.columns(2)
with c_menu:
    menu = st.selectbox("Pilih Halaman Utama:", ["🔍 Screener & Trading Plan", "📈 Analisis Chart & SL/TP", "📚 Kamus Rumus", "📂 Daftar Saham ISSI"])
with c_strat:
    strategy = st.selectbox("Pilih Strategi Screener:", [
        "Semua Saham ISSI", "Swing Trading (Uptrend + Momentum)",
        "Bandarmologi / Volume Spike", "Value Investing Syariah (Murah & Sehat)", "BSJP (Beli Sore Jual Pagi)"
    ])

with st.expander("🎛️ Pengaturan Lanjutan (Manajemen Risiko & Filter)", expanded=False):
    r1, r2, r3 = st.columns(3)
    with r1:
        modal_trading = st.number_input("Modal Trading (Rp)", min_value=100000, value=10000000, step=1000000)
        risk_pct = st.slider("Risiko / Trade (%)", 0.5, 5.0, 2.0, step=0.5)
    with r2:
        sl_mult = st.slider("Stop Loss (x ATR)", 1.0, 3.0, 1.5, step=0.5)
        tp_mult = st.slider("Take Profit (x ATR)", 1.5, 6.0, 3.0, step=0.5)
    with r3:
        min_price = st.number_input("Harga Minimal (Rp)", min_value=0, value=0, step=50) # Default 0 agar tidak memblokir saham murah
        max_rsi = st.slider("Maksimal RSI (14)", 20, 100, 100) # Default 100 agar aman
        only_buy = st.checkbox("Hanya Sinyal BUY / STRONG BUY", value=False)

with st.expander("📲 Pengaturan Bot Telegram", expanded=False):
    t1, t2 = st.columns(2)
    with t1:
        tg_token = st.text_input("Telegram Bot Token", type="password")
    with t2:
        tg_chat_id = st.text_input("Telegram Chat ID")

# Tombol Refresh Utama
if st.button("🔄 Refresh Data Pasar & Jalankan Screener", use_container_width=True, type="primary"):
    st.cache_data.clear()
    st.rerun()

st.divider()

if 'issi_list' not in st.session_state:
    st.session_state['issi_list'] = EXCEL_ISSI_TICKERS

# ---------------------------------------------------------
# ISI KONTEN MENU HALAMAN
# ---------------------------------------------------------
if menu == "🔍 Screener & Trading Plan":
    # Agar lebih cepat di HP saat pengujian pertama, opsi scan bisa dibatasi sebagian atau penuh
    df_screen = scan_issi_stocks(tuple(st.session_state['issi_list']), strategy, modal_trading, risk_pct, sl_mult, tp_mult)
    
    if not df_screen.empty:
        df_filtered = df_screen[(df_screen['Harga'] >= min_price) & (df_screen['RSI (14)'] <= max_rsi)]
        if only_buy:
            df_filtered = df_filtered[df_filtered['Rekomendasi'].str.contains("BUY")]
        df_filtered = df_filtered.sort_values(by="Skor", ascending=False)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Saham Lolos", f"{len(df_filtered)} Emiten")
        m2.metric("Sinyal Strong Buy", f"{len(df_filtered[df_filtered['Rekomendasi'] == '🟢 STRONG BUY'])} Emiten")
        m3.metric("Batas Risiko / Trade", f"Rp {int(modal_trading * (risk_pct/100)):,}")
        m4.metric("Rata-rata R/R Ratio", f"1 : {df_filtered['Risk/Reward'].mean():.2f}" if len(df_filtered) > 0 else "-")
        
        st.markdown("---")
        col_sub, col_tg = st.columns([3, 1])
        with col_sub:
            st.subheader(f"📋 Hasil Screening & Trading Plan: {strategy}")
        with col_tg:
            if st.button("📲 Kirim Sinyal ke Telegram", use_container_width=True):
                ok, status_msg = send_telegram_alert(tg_token, tg_chat_id, df_filtered, strategy)
                if ok:
                    st.success(status_msg)
                else:
                    st.error(status_msg)
        
        display_cols = ['Kode', 'Rekomendasi', 'Harga', 'Perubahan (%)', 'Stop Loss', 'Target Profit', 'Risk/Reward', 'Saran Lot', 'RVOL (x)', 'RSI (14)', 'PER (x)', 'PBV (x)', 'Alasan Sinyal']
        st.dataframe(df_filtered[display_cols], use_container_width=True, hide_index=True)
        
        csv = df_filtered[display_cols].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Hasil Trading Plan (CSV)",
            data=csv,
            file_name=f"trading_plan_issi_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("Data saham kosong atau gagal ditarik dari server. Silakan klik tombol 'Refresh Data Pasar & Jalankan Screener' di atas.")

elif menu == "📈 Analisis Chart & SL/TP":
    st.subheader("📈 Grafik Teknikal Interaktif & Level Otomatis")
    clean_tickers = [t.replace(".JK", "") for t in st.session_state['issi_list']]
    selected_stock = st.selectbox("Pilih Kode Saham ISSI:", clean_tickers)
    
    if selected_stock:
        df_chart = calculate_indicators(yf.Ticker(f"{selected_stock}.JK").history(period="6mo"))
        if not df_chart.empty:
            last_row = df_chart.iloc[-1]
            entry_p = round_idx_tick(last_row['Close'])
            sl_p = max(50, round_idx_tick(entry_p - (sl_mult * last_row.get('ATR', entry_p*0.05))))
            tp_p = round_idx_tick(entry_p + (tp_mult * last_row.get('ATR', entry_p*0.05)))
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Harga Acuan Entry", f"Rp {entry_p:,}")
            c2.metric("Target Profit (TP)", f"Rp {tp_p:,}")
            c3.metric("Batas Stop Loss (SL)", f"Rp {sl_p:,}")
            
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=df_chart.index, open=df_chart['Open'], high=df_chart['High'], low=df_chart['Low'], close=df_chart['Close'], name="Harga"))
            fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['EMA20'], line=dict(color='#00E5FF', width=1.5), name="EMA 20"))
            fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['SMA50'], line=dict(color='#FFAB00', width=1.5), name="SMA 50"))
            fig.add_hline(y=tp_p, line_dash="dash", line_color="#00E676", annotation_text=f"TP: Rp {tp_p:,}")
            fig.add_hline(y=sl_p, line_dash="dash", line_color="#FF5252", annotation_text=f"SL: Rp {sl_p:,}")
            fig.update_layout(template="plotly_dark", height=500, xaxis_rangeslider_visible=False, title=f"Visualisasi Trading Plan {selected_stock}")
            st.plotly_chart(fig, use_container_width=True)

elif menu == "📚 Kamus Rumus":
    st.subheader("📚 Penjelasan Rumus & Strategi Kuantitatif")
    st.markdown("""
    * **Trend Following (EMA 20 & SMA 50):** Menguji kepastian arah tren jangka pendek dan menengah.
    * **Momentum (RSI 14 & MACD):** Mendeteksi area pantulan sehat dan persilangan garis MACD.
    * **Bandarmologi (RVOL):** Memantau lonjakan volume transaksi harian terhadap rata-rata 20 hari ($\ge 1.5\text{x}$).
    * **Manajemen Risiko ATR:** Mengukur volatilitas harga secara dinamis untuk menentukan jarak *Stop Loss* dan *Take Profit*.
    """)

elif menu == "📂 Daftar Saham ISSI":
    st.subheader("📂 Daftar Lengkap Emiten Syariah ISSI (574+ Saham)")
    st.write(f"Total emiten aktif yang tersimpan dalam sistem: **{len(st.session_state['issi_list'])} emiten**")
    
    df_list_view = pd.DataFrame({"No": range(1, len(st.session_state['issi_list'])+1), "Kode Saham": st.session_state['issi_list']})
    st.dataframe(df_list_view, use_container_width=True, hide_index=True)
