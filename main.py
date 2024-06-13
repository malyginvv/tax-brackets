import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker

import taxation_data as td


def color_mapper(tax_rate: float) -> str:
    if tax_rate < 0.01:
        return '#b7e2ff'
    elif tax_rate < 10:
        return '#9bc7e5'
    elif tax_rate < 20:
        return '#7fadcc'
    elif tax_rate < 30:
        return '#6493b3'
    elif tax_rate < 40:
        return '#487b9b'
    elif tax_rate < 50:
        return '#2b6384'
    else:
        return '#004c6d'


def money_formatter(value: float, pos) -> str:
    if value == 0:
        return '$0'
    unit = 'K'
    amount = value // 1000
    if value >= 1000000:
        unit = 'M'
        amount = value // 1000000
    return f'${amount:g}{unit}'


plt.rcParams["font.family"] = "sans-serif"
plt.rcParams['font.sans-serif'] = ['Tahoma', 'Lucida Grande', 'DejaVu Sans', 'Verdana']

fig, ax = plt.subplots(figsize=(14, 10), layout="constrained")
fig.suptitle('Income Tax Brackets: A Global Perspective', fontsize=20)
ax.set_title('Focused on income tax rates; does not account for deductions, joint filings, or special regimes')


ax.margins(0, 0)
ax.set_xbound(0, 1000000)
ax.set_xscale('log')
ax.set_xlabel('Annual Income in USD (Logarithmic Scale)')
ax.xaxis.set_major_formatter(money_formatter)
ax.xaxis.set_major_locator(ticker.FixedLocator([0, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]))
ax.xaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.5)

y_ticks = []
y_labels = []
bars = sorted(td.bars, key=lambda b: b.gdp)
for i, bar in enumerate(bars):
    colors = bar.colors(color_mapper)
    labels = list(map(lambda x: f'{x}', bar.tax_rates_labels))
    h_bars = ax.barh(i, bar.widths, 0.5, bar.starts, color=colors, edgecolor='white')
    ax.bar_label(h_bars, labels=labels, label_type='center', color='black')
    y_ticks.append(i)
    y_labels.append(f'{bar.country_name}')

ax.set_yticks(y_ticks, labels=y_labels)
plt.show()
