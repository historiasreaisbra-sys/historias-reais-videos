import pandas as pd, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

d = pd.read_pickle('d.pkl'); chi = pd.read_pickle('chi.pkl')
rr, fr, rl, fl, a_log, crit = pd.read_pickle('m.pkl')

# permutação da F (log)
rng = np.random.default_rng(1)
g = pd.factorize(d.signo)[0]; y = d.logw.values
def F(lab):
    gm = np.bincount(lab, y) / np.bincount(lab); n = np.bincount(lab)
    ssb = (n * (gm - y.mean())**2).sum(); ssw = ((y - gm[lab])**2).sum()
    return (ssb / 11) / (ssw / (len(y) - 12))
F0 = F(g); perm = np.array([F(rng.permutation(g)) for _ in range(10000)])
pperm = (perm >= F0).mean()
open('resultados.txt', 'a').write(f'\nPermutação F(log)={F0:.3f} p={pperm:.4f}\n')
print('perm', F0, pperm)

BLUE, ORANGE, INK, INK2, GRID, BG = '#2a78d6', '#eb6834', '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
plt.rcParams.update({'font.size': 12, 'axes.edgecolor': INK2, 'axes.labelcolor': INK, 'xtick.color': INK2,
                     'ytick.color': INK2, 'figure.facecolor': BG, 'axes.facecolor': BG,
                     'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True,
                     'grid.color': GRID, 'grid.linewidth': .8})

# ---- 1. Histograma ----
fig, ax = plt.subplots(2, 1, figsize=(8, 9))
ax[0].hist(d.wb, bins=60, color=BLUE, edgecolor=BG, linewidth=1)
med = d.wb.median()
ax[0].axvline(med, color=ORANGE, lw=2); ax[0].text(med + 4, ax[0].get_ylim()[1]*.85, f'mediana US$ {med:.1f} bi'.replace('.',','), color=INK)
ax[0].set_title('Patrimônio em escala normal: quase todos colados em US$ 1–5 bi', loc='left', fontsize=13, color=INK)
ax[0].set_xlabel('Patrimônio (US$ bilhões)'); ax[0].set_ylabel('Bilionários')
bins = np.logspace(0, np.log10(d.wb.max()), 40)
ax[1].hist(d.wb, bins=bins, color=BLUE, edgecolor=BG, linewidth=1); ax[1].set_xscale('log')
ax[1].axvline(med, color=ORANGE, lw=2); ax[1].text(med*1.1, ax[1].get_ylim()[1]*.85, f'mediana US$ {med:.1f} bi'.replace('.',','), color=INK)
ax[1].set_xticks([1, 2, 5, 10, 20, 50, 100, 200]); ax[1].set_xticklabels(['1', '2', '5', '10', '20', '50', '100', '200'])
ax[1].set_title('Mesma variável em escala log: ainda assimétrica (piso de US$ 1 bi)', loc='left', fontsize=13, color=INK)
ax[1].set_xlabel('Patrimônio (US$ bilhões, escala log)'); ax[1].set_ylabel('Bilionários')
fig.suptitle(f'Distribuição do patrimônio — Forbes 2023 (n = {len(d):,})'.replace(',', '.'), x=.02, ha='left', fontsize=15, weight='bold', color=INK)
fig.tight_layout(); fig.savefig('1_histograma.png', dpi=160); plt.close()

# ---- 2. Comparação ANOVA com medianas ----
order = d.groupby('signo').wb.median().sort_values().index.tolist()
fig, ax = plt.subplots(figsize=(8, 10))
data = [d.loc[d.signo == s, 'wb'] for s in order]
bp = ax.boxplot(data, vert=False, widths=.55, patch_artist=True, showfliers=True, whis=1.5,
                medianprops=dict(color=ORANGE, lw=2.5),
                boxprops=dict(facecolor='#cde2fb', edgecolor=BLUE, lw=1.2),
                whiskerprops=dict(color=BLUE), capprops=dict(color=BLUE),
                flierprops=dict(marker='o', ms=3, mfc=BLUE, mec='none', alpha=.35))
ax.set_xscale('log'); ax.set_xticks([1, 2, 5, 10, 20, 50, 100, 200]); ax.set_xticklabels(['1', '2', '5', '10', '20', '50', '100', '200'])
ax.set_yticklabels([f'{s} (n={len(x)})' for s, x in zip(order, data)])
gmed = d.wb.median(); ax.axvline(gmed, color=INK2, ls='--', lw=1.2)
for i, x in enumerate(data, 1):
    ax.text(330, i, f'{x.median():.1f}'.replace('.',','), va='center', ha='right', color=INK, fontsize=11, weight='bold')
ax.text(330, len(order) + .75, 'mediana\n(US$ bi)', ha='right', fontsize=10, color=INK2)
ax.set_xlim(.9, 340); ax.set_ylim(.4, len(order) + 1.3)
ax.set_xlabel('Patrimônio (US$ bilhões, escala log)')
Fv, pv = a_log.F.iloc[0], a_log['PR(>F)'].iloc[0]
ax.set_title(f'ANOVA (log): F = {Fv:.2f}, p = {pv:.2f}  •  permutação p = {pperm:.2f}\n'.replace('.',',') +
             f'Kruskal-Wallis p = 0,20  •  η² = 0,6%  — nenhuma diferença entre signos',
             loc='left', fontsize=11.5, color=INK2)
fig.suptitle('Patrimônio por signo: medianas praticamente iguais', x=.02, ha='left', fontsize=15, weight='bold', color=INK)
ax.text(gmed * 1.05, .55, f'mediana geral {gmed:.1f}'.replace('.',','), color=INK2, fontsize=10)
fig.tight_layout(); fig.savefig('2_anova_medianas.png', dpi=160); plt.close()

# ---- 3. Resíduos ----
fig, ax = plt.subplots(2, 2, figsize=(9, 9))
for a, r, t in [(ax[0, 0], rr, 'Q-Q resíduos — valor bruto'), (ax[0, 1], rl, 'Q-Q resíduos — log10')]:
    (osm, osr), (sl, ic, _) = stats.probplot(r, dist='norm')
    a.scatter(osm, osr, s=6, color=BLUE, alpha=.5); a.plot(osm, sl * osm + ic, color=ORANGE, lw=2)
    a.set_title(t, loc='left', fontsize=12, color=INK); a.set_xlabel('Quantil teórico'); a.set_ylabel('Resíduo')
ax[0, 0].text(-3.5, rr.max()*.8, f'assimetria {stats.skew(rr):.1f}\ncurtose {stats.kurtosis(rr):.0f}'.replace('.',','), color=INK)
ax[0, 1].text(-3.5, rl.max()*.8, f'assimetria {stats.skew(rl):.1f}\ncurtose {stats.kurtosis(rl):.1f}'.replace('.',','), color=INK)
jit = fl + rng.normal(0, .003, len(fl))
ax[1, 0].scatter(jit, rl, s=6, color=BLUE, alpha=.4); ax[1, 0].axhline(0, color=ORANGE, lw=2)
ax[1, 0].set_title('Resíduo × ajustado (log)\nLevene p = 0,91: variâncias iguais', loc='left', fontsize=12, color=INK)
ax[1, 0].set_xlabel('Média ajustada do signo (log10)'); ax[1, 0].set_ylabel('Resíduo')
ax[1, 1].hist(rl, bins=40, color=BLUE, edgecolor=BG)
ax[1, 1].set_title('Histograma dos resíduos (log)', loc='left', fontsize=12, color=INK); ax[1, 1].set_xlabel('Resíduo')
fig.suptitle('Diagnóstico dos resíduos da ANOVA', x=.02, ha='left', fontsize=15, weight='bold', color=INK)
fig.tight_layout(); fig.savefig('3_residuos.png', dpi=160); plt.close()

# ---- 4. Qui-quadrado ----
c = chi.sort_values('resid_pad')
fig, ax = plt.subplots(figsize=(8, 8))
ax.barh(c.index, c.resid_pad, color=[BLUE if v > 0 else '#86b6ef' for v in c.resid_pad], height=.6)
for lim in (crit, -crit): ax.axvline(lim, color=ORANGE, ls='--', lw=1.5)
ax.axvline(0, color=INK2, lw=1)
for i, (s, row) in enumerate(c.iterrows()):
    x = row.resid_pad; ax.text(x + (.08 if x >= 0 else -.08), i, f'{int(row.obs)} vs {row.esp:.0f}', va='center',
                               ha='left' if x >= 0 else 'right', fontsize=10, color=INK)
ax.text(crit - .05, len(c) - .3, 'limite de\nsignificância', ha='right', color=INK2, fontsize=10)
ax.set_xlim(-3.3, 3.3); ax.set_xlabel('Resíduo padronizado (observado − esperado) / √esperado')
ax.set_title('χ² = 11,98, gl = 11, p = 0,37  •  V de Cramér = 0,02\nRótulos: observado vs esperado', loc='left', fontsize=11.5, color=INK2)
fig.suptitle('Qui-quadrado: nenhum signo foge do esperado', x=.02, ha='left', fontsize=15, weight='bold', color=INK)
fig.tight_layout(); fig.savefig('4_qui_quadrado.png', dpi=160); plt.close()
