import numpy as np
import pandas as pd
import seaborn as sns

df = pd.read_csv('final_energies-implicit.csv', index_col=0)
successful = df[df.successful == True]
unsuccessful_with_energies = df[df.successful == False][df.has_energies == True]

sns.set_context('paper', font_scale=0.9)
sns.set_style('white')
# figsize=(3.5, 5)
figsize=(3.5, 2.5)
# fig, (ax1, ax2) = sns.plt.subplots(2, 1, figsize=figsize)
fig, (ax2) = sns.plt.subplots(1, 1, figsize=figsize)

# sns.distplot(successful.final_energy, hist=False, kde=True, kde_kws={'shade': True, 'bw': 300}, color='k', ax=ax1, label='all')
print successful.final_energy.describe()

sns.distplot(successful[successful.seqid<35].final_energy, hist=False, kde=True, kde_kws={'shade': True, 'bw': 300}, label='0-35', ax=ax2)
sns.distplot(successful[successful.seqid>=35][successful.seqid<55].final_energy, hist=False, kde=True, kde_kws={'shade': True, 'bw': 300}, label='35-55', ax=ax2)
sns.distplot(successful[successful.seqid>=55].final_energy, hist=False, kde=True, kde_kws={'shade': True, 'bw': 300}, label='55-100', ax=ax2)
# ax1.legend()
ax2.legend()

# ax1.set_yticks([])
ax2.set_yticks([])

# ax1.set_xlim(-14000, -6000)
ax2.set_xlim(-14000, -6000)

# ax1.set_xlabel('Final potential energy (kT)')
ax2.set_xlabel('Final potential energy (kT)')

sns.plt.tight_layout()

sns.plt.savefig('energies.png', dpi=300)
sns.plt.savefig('energies.pdf', dpi=300)
