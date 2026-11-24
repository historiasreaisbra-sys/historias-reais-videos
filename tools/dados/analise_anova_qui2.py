import pandas as pd, numpy as np
from scipy import stats
import statsmodels.formula.api as smf
import statsmodels.api as sm
import pingouin as pg

d = pd.read_csv('bilionarios_signos.csv')
d['wb'] = d.finalWorth / 1000  # US$ bilhões
d['logw'] = np.log10(d.wb)
out = []
p = lambda *a: out.append(' '.join(str(x) for x in a))

# ---------- ANOVA bruta ----------
m_raw = smf.ols('wb ~ C(signo)', d).fit()
a_raw = sm.stats.anova_lm(m_raw, typ=2)
p('ANOVA bruta\n', a_raw)
r = m_raw.resid
p('Resíduos brutos: assimetria', round(stats.skew(r), 2), 'curtose', round(stats.kurtosis(r), 1))
p('D Agostino normalidade p=', stats.normaltest(r).pvalue)
p('Levene (mediana) p=', stats.levene(*[g.wb for _, g in d.groupby('signo')], center='median').pvalue)

# ---------- ANOVA log ----------
m_log = smf.ols('logw ~ C(signo)', d).fit()
a_log = sm.stats.anova_lm(m_log, typ=2)
p('\nANOVA log10\n', a_log)
rl = m_log.resid
p('Resíduos log: assimetria', round(stats.skew(rl), 2), 'curtose', round(stats.kurtosis(rl), 2))
p('D Agostino p=', stats.normaltest(rl).pvalue)
p('Levene p=', stats.levene(*[g.logw for _, g in d.groupby('signo')], center='median').pvalue)
eta = a_log.sum_sq.iloc[0] / a_log.sum_sq.sum()
p('eta2 log =', round(eta, 4))
p('Welch ANOVA log\n', pg.welch_anova(d, dv='logw', between='signo'))
p('Kruskal-Wallis\n', pg.kruskal(d, dv='wb', between='signo'))
p('Games-Howell pares com p<0.05:')
gh = pg.pairwise_gameshowell(d, dv='logw', between='signo')
p(gh[gh.pval < 0.05][['A', 'B', 'pval']].to_string() if (gh.pval < 0.05).any() else 'nenhum')

# ---------- Qui-quadrado ----------
days = {'Áries':31,'Touro':31,'Gêmeos':32,'Câncer':31,'Leão':31,'Virgem':31,'Libra':30,'Escorpião':30,'Sagitário':30,'Capricórnio':29,'Peixes':30,'Aquário':30}
c = d.signo.value_counts()
e = np.array([days[k] for k in c.index]); e = e / e.sum() * c.sum()
chi = stats.chisquare(c.values, e)
res = (c.values - e) / np.sqrt(e)
crit = stats.norm.ppf(1 - 0.05 / 24)
chi_df = pd.DataFrame({'obs': c.values, 'esp': e.round(1), 'resid_pad': res.round(2)}, index=c.index)
p('\nQui-quadrado', chi, '\n', chi_df, '\ncorte Bonferroni |r|>', round(crit, 2))
p('Cramer V (aderência) =', round(np.sqrt(chi.statistic / (c.sum() * 11)), 3))

open('resultados.txt', 'w').write('\n'.join(out))
print('\n'.join(out))
d.to_pickle('d.pkl'); chi_df.to_pickle('chi.pkl')
pd.to_pickle((m_raw.resid, m_raw.fittedvalues, m_log.resid, m_log.fittedvalues, a_log, crit), 'm.pkl')
