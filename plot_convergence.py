import pandas as pd
import matplotlib.pyplot as plt
plt.style.use(['./general.mplstyle', './double_column.mplstyle'])
import seaborn as sns
sns.reset_orig()



d = pd.read_csv('extraction_data.txt')

p1 = sns.relplot(data = d[d.path.str.endswith('70') & (d.freq > 0.2) & (d.f > 0.1)],
                 x = 'freq', y = 'pct_im',
                 row = "sigb", col = "f",
                 hue = "nh",
                 legend = "full",
                 kind = "line",
                 style = "period",
                 height = 1.24,
                 facet_kws = {"margin_titles": True})

p2 = sns.relplot(data = d[d.path.str.endswith('70') & (d.freq > 0.2) & (d.f > 0.1)],
                 x = 'freq', y = 'pct_re',
                 row = "sigb", col = "f",
                 hue = "nh",
                 legend = "full",
                 kind = "line",
                 style = "period",
                 height = 1.24,
                 facet_kws = {"margin_titles": True})

for p in [p1, p2]:
    p.set_xlabels('Freq. (THz)')
    p.set_ylabels('Error (%)')
    p.legend.texts[0].set_text('Harmonics')
    p.legend.texts[11].set_text('Period')


p1.figure.savefig("convergence_70_im.png")
p2.figure.savefig("convergence_70_re.png")
