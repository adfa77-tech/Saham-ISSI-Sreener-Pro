import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
        background-color: #161B22;
        border: 1px solid #30363D;
        padding: 15px;
        border-radius: 10px;
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

def flatten_df(df):
    """Menangani format MultiIndex dari yfinance versi baru agar chart dan rumus tidak error."""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df.loc[:, ~df.columns.duplicated()]

@st.cache_data(ttl=600)
def get_ihsg_data():
    try:
        hist = yf.download("^JKSE", period="5d", progress=False)
        hist = flatten_df(hist)
        if len(hist) >= 2:
            last_close = float(hist['Close'].iloc[-1])
            prev_close = float(hist['Close'].iloc[-2])
            change = last_close - prev_close
            pct_change = (change / prev_close) * 100
            return last_close, change, pct_change
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
    rs = gain / loss.replace(0, np.nan)
    df['RSI'] = 100 - (100 / (1 + rs))
    df['RSI'] = df['RSI'].fillna(50)

    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    df['Vol_MA20'] = df['Volume'].rolling(window=20).mean()
    df['RVOL'] = df['Volume'] / df['Vol_MA20'].replace(0, np.nan)
    df['RVOL'] = df['RVOL'].fillna(1.0)

    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    true_range = np.max(pd.concat([high_low, high_close, low_close], axis=1), axis=1)
    df['ATR'] = true_range.ewm(alpha=1/14, adjust=False).mean()
    return df

def generate_recommendation(row):
