import math

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


# Amount of skipped ticks on log scale e.g. 3 means skip 10, 100, 1000 and start from 10000
__SKIP_LOGS = 3


def forward_scale(a):
    adjusted_a = np.where(a == 0, np.nan, a)
    log_values = np.log10(adjusted_a) - 3
    result = np.where(a > 0, log_values, 0)
    return result


def inverse_scale(a):
    return np.power(10, a + __SKIP_LOGS)


fig, ax = plt.subplots(figsize=(12, 8))
ax.set_title('Income tax brackets')
ax.set_xscale('function', functions=(forward_scale, inverse_scale))
ax.set_xlabel('Annual income, USD')
ax.xaxis.set_major_formatter(money_formatter)
ax.xaxis.set_major_locator(ticker.FixedLocator([0, 10000, 50000, 100000, 500000, 1000000]))
ax.xaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.25)

y_ticks = []
y_labels = []
for i, bar in enumerate(td.bars):
    colors = bar.colors(color_mapper)
    labels = list(map(lambda x: f'{x} %', bar.tax_rates))
    h_bars = ax.barh(i, bar.widths, 0.2, bar.starts, color=colors, edgecolor='white')
    ax.bar_label(h_bars, labels=labels, label_type='center', color='black')
    y_ticks.append(i)
    y_labels.append(f'{bar.country_name} ({bar.currency})')

ax.set_yticks(y_ticks, labels=y_labels)
plt.show()
