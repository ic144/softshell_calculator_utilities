import matplotlib.pyplot as plt
import os
import pandas as pd
from func import RGP # van TUDelft
import matplotlib.gridspec as gridspec
from matplotlib.patches import Wedge
import re

folder = ''

def make_pdf(depth, drill, SL, SR, LT, RT, CM, listA, f, root):
    fig = plt.figure(figsize=(16, 8), tight_layout=True)  # dit is geen A4 (dat is 12, 8), maar ziet er wel mooi uit
    gs = gridspec.GridSpec(2, 3)
    gs01 = gs[0, 0].subgridspec(2, 1, height_ratios=[0.01, 1])

    # maak subplots in een grid
    plot_lb = fig.add_subplot(gs[0, 1])
    plot_rb = fig.add_subplot(gs[0, 2])
    plot_lo = fig.add_subplot(gs[1, 1], sharex=plot_lb)
    plot_ro = fig.add_subplot(gs[1, 2], sharex=plot_rb)
    table02 = fig.add_subplot(gs01[0, 0])
    circle_plot = fig.add_subplot(gs[1, 0])

    # maak 4 plots gelijk aan die uit het programma van TUD
    plot_lb.plot(depth, drill, 'b', label='drill')
    plot_lb.plot(depth, feed, 'brown', label='feed')
    plot_lb.plot(depth, feed_ma, 'c', label='feed_ma')
    plot_lb.axvline(x=LT, color='k', linestyle='--', label='LT,RT')
    plot_lb.axvline(x=RT, color='k', linestyle='--')

    plot_rb.plot(depth, drill, 'b', label='drill')
    plot_rb.axvline(x=SL[1]+LT, color='g', label='softshell')
    plot_rb.axvline(x=SR[1]+LT, color='g')
    plot_rb.axvline(x=LT, color='g')
    plot_rb.axvline(x=listA[-1], color='g')
    plot_rb.axvline(x=CM+LT, color='red', linestyle='--', label='centre')
    plot_rbbar = plot_rb.twinx()
    plot_rbbar.autoscale(False)
    plot_rbbar.set_yticks([])
    plot_rbbar.fill_between([LT, SL[1]+LT], 100, 0, where=[True, True], color='y', alpha=0.5)
    plot_rbbar.fill_between([SR[1]+LT, listA[-1]], 100, 0, where=[True, True], color='y', alpha=0.5)

    plot_lo.plot(listA, lista1, 'b', label='drill')
    plot_lo.plot(listA, lista2, 'orange', label='drill_ma')
    plot_lo.plot(listA, lista1h, 'y', label='IOMA')
    plot_lo.axvline(x=CM+LT, color='red', linestyle='--', label='centre')

    plot_ro.plot(listA, lista1, 'b', label='drill')
    plot_ro.axvline(x=CM+LT, color='red', linestyle='--', label='centre')
    plot_ro.axvline(x=SL[0]+LT, color='brown', label='Zone1 (20%)')
    plot_ro.axvline(x=SL[1]+LT, color='g', label='Zone2 (40%)')
    plot_ro.axvline(x=SL[2]+LT, color='orange', label='Zone3 (60%)')
#    plot_ro.axvline(x=SL[3]+LT, color='c', label='Zone4 (80%)')
    plot_ro.axvline(x=SR[0]+LT, color='brown')
    plot_ro.axvline(x=SR[1]+LT, color='g')
    plot_ro.axvline(x=SR[2]+LT, color='orange')
#    plot_ro.axvline(x=SR[3]+LT, color='c')
    plot_ro.axvline(x=LT, color='k', linestyle='--', label='LT,RT')
    plot_ro.axvline(x=RT, color='k', linestyle='--')

    # voor alle plots opmaak instellen
    for plotid in [plot_lb, plot_rb, plot_lo, plot_ro]:
        plotid.legend(loc='upper right')
        plotid.set_xlabel('Distance [mm]')
        plotid.set_ylabel('Amplitude [%]')

    # oude oplossing met volledig cirkel, maar alleen ingaand signaal
    if False:
            axis_lim = 175
            diam_paal = plt.Circle((0, 0), (RT-LT)/2, color='yellow', label='berekend')
            diam_gezond = plt.Circle((0, 0), (RT-LT - (SL[1]+RT-LT-SR[1]))/2, color='green', label='gezond')
            zone1 = plt.Circle((0, 0), CM-SL[0], fill=False, edgecolor='brown', label='Zone1 (20%)')
            zone2 = plt.Circle((0, 0), CM-SL[1], fill=False, edgecolor='g', label='Zone2 (40%)')
            zone3 = plt.Circle((0, 0), CM-SL[2], fill=False, edgecolor='orange', label='Zone3 (60%)')

            for elem in [diam_paal, diam_gezond, zone1, zone2, zone3]:
                    circle_plot.add_patch(elem)

            circle_plot.set_xbound(-axis_lim, axis_lim)
            circle_plot.set_ybound(-axis_lim, axis_lim)
            circle_plot.set_aspect('equal', adjustable='box')
            circle_plot.legend(loc='lower right')

    # maak twee kwart cirkels, links voor ingaand, rechts voor uitgaand
    axis_lim = 175
    diam_paal_l = Wedge((0,0), CM, 90, 180, color='yellow', label='berekend')
    diam_paal_r = Wedge((0,0), RT-(CM+LT), 0, 90, color='yellow', alpha=0.3)
    diam_gezond_l = Wedge((0,0), (CM-SL[1]), 90, 180, color='green', label='gezond')
    diam_gezond_r = Wedge((0,0), (SR[1]-CM), 0, 90, color='green', alpha=0.3)
    zone1L = Wedge((0,0), CM-SL[0], 90, 180, fill=False, edgecolor='brown', label='Zone1 (20%)')
    zone2L = Wedge((0,0), CM-SL[1], 90, 180, fill=False, edgecolor='black', label='Zone2 (40%)')
    zone3L = Wedge((0,0), CM-SL[2], 90, 180, fill=False, edgecolor='orange', label='Zone3 (60%)')
    zone1R = Wedge((0,0), SR[0]-CM, 0, 90, fill=False, edgecolor='brown', linestyle='--')
    zone2R = Wedge((0,0), SR[1]-CM, 0, 90, fill=False, edgecolor='black', linestyle='--')
    zone3R = Wedge((0,0), SR[2]-CM, 0, 90, fill=False, edgecolor='orange', linestyle='--')

    for elem in [diam_paal_l, diam_paal_r, diam_gezond_l, diam_gezond_r, zone1L, zone2L, zone3L, zone1R, zone2R, zone3R]:
            circle_plot.add_patch(elem)

    # voeg een verticale lijn toe om in- en uitgaand te scheiden
    circle_plot.axvline(x=0, color='grey')

    # doe de opmaak van de cirkel plot
    circle_plot.set_xbound(-axis_lim, axis_lim)
    circle_plot.set_ybound(0, axis_lim)
    circle_plot.set_aspect('equal', adjustable='box')
    circle_plot.legend(loc='upper right')

    # maak een tabel met overzicht met kengetallen
    try:
        # de standaard naamgeving van 2024
        # en de variant voor DCG0301
        rakcode, rakdeel, paalnummer, metingnummer = re.findall(r'([A-Z]{3}\d{4})_?(.*)?_(P\d\.\d+)_?(B?M{1,2}\d{1,3})', f)[0]
    except:
        # naamgeving voor de testrakken
        rakcode, paalnummer, metingnummer = re.findall(r'([A-Z]{3}\d{4})-(P\d\.\d+)-(BM[A-C])', f)[0]
        # rakcode, paalnummer, metingnummer = re.findall(r'(NMS_ZB)_(P\d\.\d+)_(BM\d{1,3})', f)[0]  # speciaal geval van Timothy
        rakdeel = None

    table = {
        "Uitvoering meting": "Nebest",
        "Datum meting": "?",
        "Rakcode": rakcode,
        "Rakdeel": rakdeel,
        "Paalnummer": paalnummer,
        "Nummer meting": metingnummer,
        "Soft shell calculator versie": "8-12-2021",
        "Start signaal": f'{round(LT, 1)} mm',
        "Eind signaal": f'{round(RT, 1)} mm',
        "Paaldiameter berekend": f'{round(RT-LT, 1)} mm',
        "Paaldiameter gemeten": "? mm",
        "Zachte schil ingaand": f'{round(SL[1], 1)} mm',
        "Zachte schil uitgaand": f'{round(RT-LT-SR[1], 1)} mm',
        "Totale afname": f'{round(SL[1]+RT-LT-SR[1], 1)} mm',
        "Gezonde diameter kop o.b.v. IML": f'{round(RT-LT - (SL[1]+RT-LT-SR[1]), 1)} mm'
    }

    values = [[k, v] for k, v in table.items()]

    test = table02.table(cellText=values)
    test.auto_set_font_size(False)
    test.set_fontsize(9)
    table02.axis('off')
    plt.suptitle(f)
    plt.savefig(f'{root}/{f.replace(".rgp", ".pdf")}')
    plt.close('all')

    print(f)


# maak een lege output tabel
output = pd.DataFrame()

# itereer mappen en bestanden
for root, dirs, files in os.walk(folder):
    # maak een lijst waar al een pdf van is
    pdfs = [f for f in files if f.lower().endswith('.pdf')]
    # maak een lijst van rgp bestanden
    rgp_files = [f for f in files if f.lower().endswith('.rgp')]

    # bepaal wat er al in een tabel staat, die niet nog een keer doen
    if os.path.isfile(f'{root}/iml-rpd_verzamel_{root[-7:]}.csv'):
        oudeTabel = pd.read_csv(f'{root}/iml-rpd_verzamel_{root[-7:]}.csv', index_col=0, sep=';', decimal=',')
        rgp_files = [f for f in rgp_files if f not in oudeTabel.index]
    else:
        oudeTabel = []

    for f in rgp_files:
        try:
            # lees sowieso alle bestanden in voor de tabel met samenvatting
            depth, drill, feed, feed_ma, LT, RT, BM, lista0, lista1, lista2, CM, lista1h, SL, SR, lista1h1, lista1h2, listA = RGP(f'{root}/{f}')
            output.loc[f, 'Left soft shell'] = round(SL[1], 1)
            output.loc[f, 'Right soft shell'] = round(RT-LT-SR[1], 1)
            output.loc[f, 'Left threshold'] = round(LT, 1)
            output.loc[f, 'Right threshold'] = round(RT, 1)
            output.loc[f, 'Berekende diameter'] = round(RT-LT, 1)

            # als er al een plot is, dan geen nieuwe maken
            if f.replace('rgp', 'pdf') not in pdfs:
                make_pdf(depth, drill, SL, SR, LT, RT, CM, listA, f, root)

        # als er iets mis, dan wordt een lege regel naar de tabel geschreven
        except Exception as e:
            print(f, e)
            output.loc[f, 'Left soft shell'] = None
            output.loc[f, 'Right soft shell'] = None
            output.loc[f, 'Left threshold'] = None
            output.loc[f, 'Right threshold'] = None
            output.loc[f, 'Berekende diameter'] = None

    # voor je naar een nieuwe map gaat opslaan en een lege tabel maken
    # behalve als je in de bovenste map zit
    if not root.endswith('IML - RGB Data') and len(files) > 0:
        if os.path.isfile(f'{root}/iml-rpd_verzamel_{root[-7:]}.csv'):
             output = pd.concat([output, oudeTabel])
        # schrijf de data weg
        output.to_csv(f'{root}/iml-rpd_verzamel_{root[-7:]}.csv', sep=';', decimal=',')
        # maak een lege tabel
        output = pd.DataFrame()

# TODO: paaldiameters toevoegen uit duikdata