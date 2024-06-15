import matplotlib.pyplot as plt
from matplotlib import ticker

import taxation_data as td


def color_mapper(tax_rate: float) -> str:
    if tax_rate == 0:
        return '#F9F9F9'
    elif tax_rate < 15:
        return '#D1E5F0'
    elif tax_rate < 30:
        return '#8EC4DE'
    elif tax_rate < 45:
        return '#3A93C3'
    else:
        return '#1065AB'


def money_formatter(value: float, _) -> str:
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

fig, ax = plt.subplots(figsize=(12, 8), layout="tight")
fig.suptitle('Income Tax Brackets: A Global Perspective', fontsize=20)
ax.set_title('Focused on income tax rates; does not account for deductions, joint filings, or special regimes. '
             'Top 15 countries by 2022 GDP', fontsize=12)

ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)
ax.spines.left.set_visible(False)
ax.spines.bottom.set_visible(False)

ax.margins(0, 0)
ax.invert_yaxis()
ax.yaxis.set_tick_params(pad=10)
ax.tick_params('y', length=0)

ax.set_xscale('symlog', linthresh=10000)
ax.set_xlabel('Annual Income in USD (Linear up to $10K, Logarithmic Beyond)', fontsize=12)
ax.xaxis.set_major_formatter(money_formatter)
ax.xaxis.set_major_locator(ticker.FixedLocator([0, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]))
ax.xaxis.set_tick_params(labelsize=12)
ax.xaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.5)

y_ticks = []
y_labels = []
country_bars = sorted(td.bar_data, key=lambda b: b.gdp, reverse=True)[:15]  # Top 15 countries by GDP
counter = 0
for bars in country_bars:
    bar_colors = bars.colors(color_mapper)
    labels = list(map(lambda x: f'{x}%', bars.tax_rates_labels))
    h_bars = ax.barh(counter, bars.widths, 0.7, bars.starts, color=bar_colors, edgecolor='white')
    ax.bar_label(h_bars, labels=labels, label_type='center', color='#000')
    y_ticks.append(counter)
    y_labels.append(f'{bars.country_name}')
    counter = counter + 1

ax.set_yticks(y_ticks, labels=y_labels, fontsize=12)
plt.show()
fig.savefig('tax_brackets.png')
