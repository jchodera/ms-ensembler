import numpy as np
import pandas as pd
import seaborn as sns
from ast import literal_eval

df = pd.read_csv('loopmodel_data.csv', converters={'missing_resi_spans': literal_eval})

successful = df[df.no_missing_residues == False][df.successful == True]
unsuccessful = df[df.no_missing_residues == False][df.successful == False]

print df.describe()
print successful.describe()
print unsuccessful.describe()

missing_resis_spans = np.array([x for sublist in df.missing_resi_spans for x in sublist])

# ====
# plot
# ====

palette = sns.color_palette()

sns.set_context('paper', font_scale=1)
sns.set_style('whitegrid')
figsize=(3.5, 4)
# sns.plt.figure(figsize=figsize)

# fig, (ax1, ax2) = sns.plt.subplots(2, 1, sharex=True, figsize=figsize)
fig, (ax1, ax2) = sns.plt.subplots(2, 1, figsize=figsize)

# bins = np.linspace(0, df.nmissing_resis.max(), 10)
bins1 = np.arange(0, df.nmissing_resis.max()+1, 1)
sns.distplot(df.nmissing_resis, kde=False, bins=bins1, label='all templates', ax=ax1, hist_kws={'alpha': 1.})
sns.distplot(unsuccessful.nmissing_resis, kde=False, bins=bins1, label='failed remodeling', ax=ax1, color=palette[2], hist_kws={'alpha': 1.})
# same with log y-axis:
# sns.distplot(df.nmissing_resis, kde=False, bins=bins1, label='all templates', hist_kws={'log': True}, rug=True, rug_kws={'height': 0.7, 'lw': 0.5}, ax=ax1)
# sns.distplot(unsuccessful.nmissing_resis, kde=False, bins=bins1, label='failed remodeling', hist_kws={'log': True}, color=palette[2], ax=ax1)
# sns.plt.ylim(0.8,10000)

ax1.legend()

# sns.distplot(successful.nmissing_resis, hist=False, kde=True, rug=True, label='successful',
#     rug_kws={'height': 0.002},
# )
# sns.distplot(unsuccessful.nmissing_resis, hist=False, kde=True, rug=True, label='unsuccessful', color='red',
#     # kde_kws={'bw': 2.5},
#     rug_kws={'height': 0.001},
# )

# sns.violinplot([successful.nmissing_resis, unsuccessful.nmissing_resis], inner='points',
#     inner_kws={'markersize': 5, 'marker': 'o'},
#     alpha=0.5,
# )
# sns.violinplot([successful.nmissing_resis, unsuccessful.nmissing_resis], inner='stick',
#     inner_kws={'width': 5},
#     alpha=0.5,
# )

# sns.distplot(missing_resis_spans, kde=True, hist=False, rug=True, color='k', kde_kws={'shade': True}, rug_kws={'lw': 0.5}, ax=ax2)
bins2 = np.arange(0, missing_resis_spans.max()+1, 1)
sns.distplot(missing_resis_spans-2, kde=False, hist=True, bins=bins2, color='gray', ax=ax2, hist_kws={'alpha': 1.})
# ax2.set_yticks([])

ax1.set_xlabel('Remodeled residues per template')
ax1.set_ylabel('Number of templates')
ax2.set_xlabel('Remodeled loop length')
ax2.set_ylabel('Number of loops')

ax1.set_xlim(0, 60)
ax2.set_xlim(0, 30)

ax1.grid()
ax2.grid()

sns.plt.tight_layout()

sns.plt.savefig('nmissing_resis_distributions.pdf')
sns.plt.savefig('nmissing_resis_distributions.png', dpi=300)
