import matplotlib.pyplot as plt

import taxation_data as td


def color_mapper(tax_rate: float) -> str:
    if tax_rate < 0.01:
        return '#b7e2ff'
    if tax_rate < 10:
        return '#9bc7e5'
    if tax_rate < 20:
        return '#7fadcc'
    if tax_rate < 30:
        return '#6493b3'
    if tax_rate < 40:
        return '#487b9b'
    if tax_rate < 50:
        return '#2b6384'
    else:
        return '#004c6d'


fig, ax = plt.subplots(figsize=(12, 8))
# ax.xaxis.set_visible(False)
# ax.set_xlim(0, np.sum(data, axis=1).max())

for i, bar in enumerate(td.bars):
    colors = bar.colors(color_mapper)
    rects = ax.barh(i, bar.widths, 0.5, bar.starts, color=colors, edgecolor='white')
    ax.bar_label(rects, labels=bar.tax_rates, label_type='center', color='black')

# ax.barh([1, 1, 1], [10000, 44000, 86000], 0.5, [0, 10000, 44000], color=['#abc', '#ccc', '#edc'])
# ax.barh([2, 2, 2], [15000, 44000, 86000], 0.5, 0)
plt.show()
