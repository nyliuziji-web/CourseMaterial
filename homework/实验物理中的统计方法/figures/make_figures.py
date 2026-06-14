from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Arc
from scipy import stats, optimize

FIG = Path(__file__).resolve().parent
FIG.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(20260611)

def save(name):
    plt.tight_layout()
    plt.savefig(FIG / name, dpi=220, bbox_inches='tight')
    plt.close()

# 3.1 Uniform histogram
x = rng.random(10000)
plt.figure(figsize=(5.8,3.6))
plt.hist(x, bins=100, range=(0,1), histtype='step', linewidth=1.2)
plt.axhline(100, linestyle='--', linewidth=1.0)
plt.xlabel('x')
plt.ylabel('counts per bin')
plt.title('Uniform random numbers, N=10000, 100 bins')
save('fig_03_01_uniform.png')

# 3.2 Multinomial bin count and scatter
reps=10000
counts = rng.multinomial(100, [0.2]*5, size=reps)
plt.figure(figsize=(5.8,3.6))
vals=np.arange(5,36)
plt.hist(counts[:,2], bins=np.arange(4.5,35.6,1), density=True, alpha=0.55, label='MC')
pmf=stats.binom.pmf(vals, 100, 0.2)
plt.plot(vals, pmf, marker='o', linewidth=1.0, label='Binom(100,0.2)')
plt.xlabel('$n_3$')
plt.ylabel('probability')
plt.title('Distribution of one bin count')
plt.legend()
save('fig_03_02_bin_count.png')
plt.figure(figsize=(4.5,4.2))
plt.scatter(counts[:800,0], counts[:800,1], s=10, alpha=0.45)
plt.xlabel('$n_1$')
plt.ylabel('$n_2$')
plt.title(f'Multinomial counts, corr={np.corrcoef(counts[:,0],counts[:,1])[0,1]:.3f}')
save('fig_03_02_scatter.png')

# 3.3 Sawtooth distribution
N=30000
r=rng.random(N)
x_inv=np.sqrt(r)
# rejection
xs=[]
while len(xs)<N:
    cand=rng.random(N)
    u=rng.random(N)
    accepted=cand[u<cand]
    xs.extend(accepted.tolist())
x_rej=np.array(xs[:N])
grid=np.linspace(0,1,200)
plt.figure(figsize=(5.8,3.6))
plt.hist(x_inv, bins=60, range=(0,1), density=True, histtype='step', label='inverse transform')
plt.hist(x_rej, bins=60, range=(0,1), density=True, histtype='step', label='rejection')
plt.plot(grid, 2*grid, linewidth=1.2, label='$f(x)=2x$')
plt.xlabel('x')
plt.ylabel('density')
plt.title('Sawtooth density generation')
plt.legend()
save('fig_03_03_sawtooth.png')

# 3.4 CLT sums
plt.figure(figsize=(5.8,3.6))
for n in [1,2,4,12]:
    z=(rng.random((25000,n)).sum(axis=1)-n/2)/np.sqrt(n/12)
    # plot KDE-ish histogram line
    hist,bins=np.histogram(z,bins=90,range=(-4,4),density=True)
    centers=(bins[:-1]+bins[1:])/2
    plt.plot(centers,hist,linewidth=1.1,label=f'n={n}')
grid=np.linspace(-4,4,500)
plt.plot(grid, stats.norm.pdf(grid), linestyle='--', linewidth=1.1, label='N(0,1)')
plt.xlabel('z')
plt.ylabel('density')
plt.title('CLT generator based on sums of uniforms')
plt.legend()
save('fig_03_04_clt.png')

# 3.5 exGaussian cases
plt.figure(figsize=(5.8,3.6))
for tau,sigma,label in [(0.2,1.0,r'$\tau\ll\sigma$'),(1.0,0.5,r'$\tau=1,\sigma=0.5$'),(2.0,0.2,r'$\tau\gg\sigma$')]:
    y=rng.exponential(tau, size=50000)+rng.normal(0,sigma,size=50000)
    hist,bins=np.histogram(y,bins=120,range=(-3,7),density=True)
    centers=(bins[:-1]+bins[1:])/2
    plt.plot(centers,hist,linewidth=1.1,label=label)
plt.xlabel('y=t+x')
plt.ylabel('density')
plt.title('Exponential lifetime convolved with Gaussian error')
plt.legend()
save('fig_03_05_exgaussian.png')

# 3.6 Cauchy and sample means
x=rng.standard_cauchy(80000)
means=rng.standard_cauchy((80000,10)).mean(axis=1)
grid=np.linspace(-10,10,600)
plt.figure(figsize=(5.8,3.6))
plt.hist(x, bins=150, range=(-10,10), density=True, histtype='step', label='single Cauchy')
plt.hist(means, bins=150, range=(-10,10), density=True, histtype='step', label='mean of 10')
plt.plot(grid, stats.cauchy.pdf(grid), linestyle='--', linewidth=1.1, label='standard Cauchy')
plt.xlabel('x')
plt.ylabel('density')
plt.title('Cauchy sample mean has the same law')
plt.legend()
save('fig_03_06_cauchy_mean.png')

# 3.7 PMT schematic
plt.figure(figsize=(7,2.6))
ax=plt.gca(); ax.set_xlim(0,10); ax.set_ylim(0,3); ax.axis('off')
ax.add_patch(Rectangle((0.6,0.7),0.25,1.6,fill=False,linewidth=1.5))
ax.text(0.45,2.45,'photocathode',fontsize=8)
for i in range(6):
    x0=1.8+i*1.15
    ax.add_patch(Rectangle((x0,0.6+0.15*(i%2)),0.28,1.4,fill=False,linewidth=1.2))
    ax.text(x0-0.15,2.35,fr'$D_{i+1}$',fontsize=9)
ax.add_patch(Rectangle((9.0,0.8),0.35,1.2,fill=False,linewidth=1.5))
ax.text(8.75,2.35,'anode',fontsize=8)
for i in range(8):
    x1=0.0 if i==0 else 0.85+(i-1)*1.15
    x2=0.7 if i==0 else (1.8+(i-1)*1.15 if i<7 else 9.05)
    y1=1.5; y2=1.4+0.2*((i+1)%2)
    ax.add_patch(FancyArrowPatch((x1+0.15,y1),(x2,y2),arrowstyle='->',mutation_scale=10,linewidth=1.0))
ax.text(0.05,1.75,'photon',fontsize=8)
ax.text(3.0,0.25,'secondary emission cascade',fontsize=9)
save('fig_03_07_pmt_schematic.png')

def simulate_pmt(nu, M=20000):
    out=np.empty(M,dtype=int)
    for m in range(M):
        z=1
        for v in nu:
            z=rng.poisson(v*z)
            if z==0: break
        out[m]=z
    return out
out1=simulate_pmt([3]*6, 20000)
out2=simulate_pmt([6]+[3]*5, 20000)
plt.figure(figsize=(5.8,3.6))
plt.hist(out1,bins=50,range=(0,3000),density=True,histtype='step',label=r'$(3,3,3,3,3,3)$')
plt.hist(out2,bins=50,range=(0,4000),density=True,histtype='step',label=r'$(6,3,3,3,3,3)$')
plt.xlabel('$n_{out}$')
plt.ylabel('density')
plt.title('PMT output-electron distribution')
plt.legend()
save('fig_03_07_pmt_hist.png')

# 4.1 e/pi test
xgrid=np.linspace(-5,5,800)
plt.figure(figsize=(5.8,3.6))
plt.plot(xgrid, stats.norm.pdf(xgrid,0,1), label='electron: N(0,1)')
plt.plot(xgrid, stats.norm.pdf(xgrid,2,1), label='pion: N(2,1)')
plt.axvline(1, linestyle='--', linewidth=1.0, label='$t<1$ cut')
plt.axvline(-2.5153, linestyle=':', linewidth=1.0, label='95% purity cut')
plt.fill_between(xgrid,0,stats.norm.pdf(xgrid,0,1),where=xgrid<1,alpha=0.25)
plt.fill_between(xgrid,0,stats.norm.pdf(xgrid,2,1),where=xgrid<1,alpha=0.18)
plt.xlabel('t')
plt.ylabel('density')
plt.title('Electron/pion test statistic')
plt.legend(fontsize=8)
save('fig_04_01_e_pi_test.png')

# 4.3 Poisson tail
k=np.arange(0,25)
pmf=stats.poisson.pmf(k,3.9)
plt.figure(figsize=(5.8,3.6))
plt.bar(k,pmf,width=0.85)
plt.bar(k[k>=16],pmf[k>=16],width=0.85)
plt.axvline(16, linestyle='--', linewidth=1)
plt.xlabel('n')
plt.ylabel('P(n|3.9)')
plt.title('Poisson tail for observed n=16')
save('fig_04_03_poisson_tail.png')

# 4.4 data and chi2 contributions
xmin=np.arange(0,10,0.5); xmax=xmin+0.5; centers=(xmin+xmax)/2
obs=np.array([1,0,3,4,6,3,3,4,5,7,4,5,2,0,1,0,0,1,0,0])
th1=np.array([0.2,1.2,1.9,3.2,4.0,4.5,4.7,4.8,4.8,4.5,4.1,3.5,3.0,2.4,1.6,0.9,0.5,0.3,0.2,0.1])
th2=np.array([0.2,0.7,1.1,1.6,1.9,2.2,2.7,3.3,3.6,3.9,4.0,4.0,3.9,3.5,3.2,2.8,2.2,1.5,1.0,0.5])
plt.figure(figsize=(6.2,3.8))
plt.step(xmin, obs, where='post', label='data')
plt.plot(centers, th1, marker='o', linewidth=1, label='theory1')
plt.plot(centers, th2, marker='s', linewidth=1, label='theory2')
plt.xlabel('x')
plt.ylabel('counts / expected counts')
plt.title('Binned data and theory predictions')
plt.legend(fontsize=8)
save('fig_04_04_binned_data.png')
plt.figure(figsize=(6.2,3.8))
plt.bar(centers-0.12,(obs-th1)**2/th1,width=0.22,label='theory1')
plt.bar(centers+0.12,(obs-th2)**2/th2,width=0.22,label='theory2')
plt.xlabel('x bin center')
plt.ylabel('Pearson contribution')
plt.title(r'Bin-by-bin contributions to $\chi^2$')
plt.legend(fontsize=8)
save('fig_04_04_chi2_contrib.png')

# 4.5 Rutherford-Geiger data
m=np.arange(15)
nm=np.array([57,203,383,525,532,408,273,139,45,27,10,4,0,1,1])
ntot=nm.sum(); mean=(m*nm).sum()/ntot
pois=stats.poisson.pmf(m,mean)*ntot
plt.figure(figsize=(5.8,3.6))
plt.bar(m,nm,width=0.75,label='data')
plt.plot(m,pois,marker='o',linewidth=1.1,label=f'Poisson mean={mean:.3f}')
plt.xlabel('decays in interval')
plt.ylabel('number of intervals')
plt.title('Rutherford-Geiger alpha-decay counts')
plt.legend(fontsize=8)
save('fig_04_05_rutherford_poisson.png')

# 6.7 exponential MLE simulation
figdata={}
plt.figure(figsize=(5.8,3.6))
for n in [5,10,100]:
    samp=rng.exponential(1, size=(40000,n))
    tauhat=samp.mean(axis=1)
    lamhat=1/tauhat
    hist,bins=np.histogram(lamhat,bins=100,range=(0,3),density=True)
    centers=(bins[:-1]+bins[1:])/2
    plt.plot(centers,hist,linewidth=1.0,label=f'n={n}, mean={lamhat.mean():.3f}')
plt.axvline(1, linestyle='--', linewidth=1)
plt.xlabel(r'$\hat\lambda=1/\bar t$')
plt.ylabel('density')
plt.title('Bias of exponential-rate MLE')
plt.legend(fontsize=8)
save('fig_06_07_exp_mle.png')

# 6.11 Perrin schematic
plt.figure(figsize=(5.2,3.6))
ax=plt.gca(); ax.set_xlim(0,6); ax.set_ylim(0,5); ax.axis('off')
ax.add_patch(Rectangle((1.2,0.7),3.5,3.1,fill=False,linewidth=1.4))
for yy in [1.0,1.8,2.6,3.4]:
    ax.plot([1.2,4.7],[yy,yy],linestyle=':',linewidth=0.8)
    for xx in np.linspace(1.5,4.4,5):
        ax.add_patch(Circle((xx+rng.normal(0,0.05), yy+rng.normal(0,0.08)),0.04,fill=True))
ax.add_patch(FancyArrowPatch((5.2,0.8),(5.2,3.7),arrowstyle='<->',mutation_scale=12))
ax.text(5.35,2.2,'z',fontsize=10)
ax.add_patch(Rectangle((2.2,4.0),1.5,0.4,fill=False,linewidth=1.2))
ax.text(2.0,4.55,'microscope focus',fontsize=9)
ax.text(1.4,0.25,'suspension cell',fontsize=9)
save('fig_06_11_perrin_schematic.png')

# Perrin fit
z_um=np.array([0,6,12,18],dtype=float)
n=np.array([1880,940,530,305],dtype=float)
r_cm=0.52e-4; drho=0.063; g=980; T=293; R=8.32e7
z_cm=z_um*1e-4
C=4*np.pi*r_cm**3*drho*g/(3*T)
def nll(params):
    lognu0, logk = params
    nu0=np.exp(lognu0); k=np.exp(logk)
    nu=nu0*np.exp(-C*z_cm/k)
    return np.sum(nu-n*np.log(nu))
res=optimize.minimize(nll, [np.log(1845), np.log(1.2e-16)], method='Nelder-Mead')
nu0hat=np.exp(res.x[0]); khat=np.exp(res.x[1])
zz=np.linspace(0,18,200); zzcm=zz*1e-4; fit=nu0hat*np.exp(-C*zzcm/khat)
plt.figure(figsize=(5.8,3.6))
plt.errorbar(z_um,n,yerr=np.sqrt(n),fmt='o',label='data')
plt.plot(zz,fit,label=f'MLE fit, $N_A$={R/khat/1e23:.2f}e23')
plt.yscale('log')
plt.xlabel('z (micrometer)')
plt.ylabel('particle count')
plt.title('Perrin data: exponential height dependence')
plt.legend(fontsize=8)
save('fig_06_11_perrin_fit.png')

# 7.1 Galileo schematic and fit
plt.figure(figsize=(5.5,3.4))
ax=plt.gca(); ax.set_xlim(0,10); ax.set_ylim(0,5); ax.axis('off')
ax.plot([0.8,4.2],[4.1,2.7],linewidth=2)
ax.plot([4.2,5.2],[2.7,2.7],linewidth=2)
ax.add_patch(Circle((1.8,3.7),0.15))
ax.add_patch(FancyArrowPatch((5.2,2.7),(8.6,1.0),connectionstyle='arc3,rad=-0.25',arrowstyle='->',mutation_scale=12,linewidth=1.2))
ax.plot([4.2,4.2],[0.7,2.7],linestyle='--')
ax.plot([4.2,8.6],[0.7,0.7],linestyle='--')
ax.text(3.8,1.7,'h',fontsize=10); ax.text(6.2,0.35,'d',fontsize=10)
ax.text(0.8,4.35,'ramp',fontsize=9)
save('fig_07_01_galileo_schematic.png')
h=np.array([1000,828,800,600,300],float); d=np.array([1500,1340,1328,1172,800],float); sigma=15
alpha_sqrt=(d*np.sqrt(h)).sum()/h.sum()
# power fit
def chi_power(p):
    a,b=p
    return np.sum(((d-a*h**b)/sigma)**2)
res=optimize.minimize(chi_power,[47,0.5])
a_pow,b_pow=res.x
xx=np.linspace(0,1050,300)
plt.figure(figsize=(5.8,3.6))
plt.errorbar(h,d,yerr=sigma,fmt='o',label='data')
plt.plot(xx,alpha_sqrt*np.sqrt(xx),label=r'$\alpha\sqrt{h}$')
plt.plot(xx,a_pow*xx**b_pow,label=fr'$\alpha h^\beta$, $\beta={b_pow:.3f}$')
plt.xlabel('h (punti)')
plt.ylabel('d (punti)')
plt.title('Galileo data and fitted models')
plt.legend(fontsize=8)
save('fig_07_01_galileo_fit.png')

# 7.2 Ptolemy schematic and fit
plt.figure(figsize=(4.6,4.2))
ax=plt.gca(); ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2); ax.set_aspect('equal'); ax.axis('off')
ax.add_patch(Circle((0,0),1,fill=False,linewidth=1.2))
ax.plot([-1,1],[0,0],linewidth=1.4)
ax.text(0.75,0.08,'air',fontsize=9); ax.text(0.7,-0.18,'water',fontsize=9)
# incident and refracted rays
ang_i=np.deg2rad(55); ang_r=np.deg2rad(37)
ax.plot([0,-np.sin(ang_i)],[0,np.cos(ang_i)],linewidth=1.4)
ax.plot([0,np.sin(ang_r)],[0,-np.cos(ang_r)],linewidth=1.4)
ax.add_patch(Arc((0,0),0.6,0.6,theta1=90,theta2=90+55))
ax.add_patch(Arc((0,0),0.45,0.45,theta1=270-37,theta2=270))
ax.text(-0.55,0.38,r'$\theta_i$',fontsize=10)
ax.text(0.25,-0.38,r'$\theta_r$',fontsize=10)
save('fig_07_02_ptolemy_schematic.png')
ti=np.array([10,20,30,40,50,60,70,80],float); tr=np.array([8,15.5,22.5,29,35,40.5,45.5,50],float); sig=0.5
alpha=(ti*tr).sum()/(ti*ti).sum()
X=np.vstack([ti,-ti**2]).T
params=np.linalg.lstsq(X,tr,rcond=None)[0]
def chi_r(r):
    pred=np.degrees(np.arcsin(np.sin(np.radians(ti))/r))
    return np.sum(((tr-pred)/sig)**2)
res=optimize.minimize_scalar(chi_r,bounds=(1.01,2.5),method='bounded')
rhat=res.x
xx=np.linspace(0,85,300)
plt.figure(figsize=(5.8,3.6))
plt.errorbar(ti,tr,yerr=sig,fmt='o',label='data')
plt.plot(xx,alpha*xx,label='linear')
plt.plot(xx,params[0]*xx-params[1]*xx**2,label='Ptolemy quadratic')
plt.plot(xx,np.degrees(np.arcsin(np.sin(np.radians(xx))/rhat)),label=fr'Snell $r={rhat:.3f}$')
plt.xlabel('incident angle (deg)')
plt.ylabel('refracted angle (deg)')
plt.title('Ptolemy refraction data')
plt.legend(fontsize=8)
save('fig_07_02_ptolemy_fit.png')

# 8.1 decay schematic and density
plt.figure(figsize=(5.0,3.6))
ax=plt.gca(); ax.set_xlim(-1.3,1.5); ax.set_ylim(-1.1,1.1); ax.axis('off'); ax.set_aspect('equal')
ax.add_patch(FancyArrowPatch((-1.1,0),(1.2,0),arrowstyle='->',mutation_scale=12,linewidth=1.2))
ax.text(1.22,0.05,r'$\rho^0$ direction',fontsize=9)
ang=np.deg2rad(38)
ax.add_patch(FancyArrowPatch((0,0),(np.cos(ang),np.sin(ang)),arrowstyle='->',mutation_scale=12,linewidth=1.3))
ax.add_patch(FancyArrowPatch((0,0),(-np.cos(ang),-np.sin(ang)),arrowstyle='->',mutation_scale=12,linewidth=1.3))
ax.add_patch(Arc((0,0),0.55,0.55,theta1=0,theta2=38))
ax.text(0.43,0.16,r'$\theta$',fontsize=11); ax.text(0.85,0.72,r'$\pi^+$',fontsize=10); ax.text(-0.95,-0.75,r'$\pi^-$',fontsize=10)
save('fig_08_01_rho_decay_schematic.png')
xx=np.linspace(-1,1,500)
plt.figure(figsize=(5.8,3.6))
for eta in [-0.5,0,0.6,1.0]:
    f=0.5*(1-eta)+1.5*eta*xx**2
    plt.plot(xx,f,label=fr'$\eta={eta}$')
plt.xlabel(r'$x=\cos\theta$')
plt.ylabel('density')
plt.title(r'$\rho^0\to\pi^+\pi^-$ angular density')
plt.legend(fontsize=8)
save('fig_08_02_eta_density.png')

# 9.1 Gaussian confidence belt
sigma=1; alpha=beta=0.159; th=np.linspace(-3,3,300)
u=th+stats.norm.ppf(1-alpha)*sigma; v=th+stats.norm.ppf(beta)*sigma
plt.figure(figsize=(5.8,3.6))
plt.plot(th,u,label=r'$u_\alpha(\theta)$')
plt.plot(th,v,label=r'$v_\beta(\theta)$')
plt.fill_between(th,v,u,alpha=0.20)
plt.plot(th,th,linestyle='--',linewidth=1,label=r'$\hat\theta=\theta$')
plt.xlabel(r'$\theta$')
plt.ylabel(r'$\hat\theta$')
plt.title('Gaussian confidence belt')
plt.legend(fontsize=8)
save('fig_09_01_gaussian_belt.png')

# 9.2 exponential confidence belt
n=5; alpha=beta=0.159; xi=np.linspace(0,3,300)
qlo=stats.chi2.ppf(beta,2*n); qhi=stats.chi2.ppf(1-alpha,2*n)
ualpha=xi*qhi/(2*n); vbeta=xi*qlo/(2*n)
plt.figure(figsize=(5.8,3.6))
plt.plot(xi,ualpha,label=r'$u_\alpha(\xi)$')
plt.plot(xi,vbeta,label=r'$v_\beta(\xi)$')
plt.axhline(1.0,linestyle='--',linewidth=1,label=r'observed $\hat\xi=1$')
a=2*n*1/qhi; b=2*n*1/qlo
plt.axvline(a,linestyle=':',linewidth=1); plt.axvline(b,linestyle=':',linewidth=1)
plt.xlabel(r'$\xi$')
plt.ylabel(r'$\hat\xi$')
plt.title('Exponential mean confidence belt')
plt.legend(fontsize=8)
save('fig_09_02_exponential_belt.png')

# 9.7 detector geometry and transformed interval
plt.figure(figsize=(5.2,3.6))
ax=plt.gca(); ax.set_xlim(-0.5,5); ax.set_ylim(-0.3,2.3); ax.axis('off')
ax.plot([0,4.2],[0,0],linewidth=1.2); ax.plot([4.2,4.2],[0,1.8],linewidth=1.2)
ax.add_patch(FancyArrowPatch((0,0),(4.2,1.2),arrowstyle='->',mutation_scale=12,linewidth=1.3))
ax.plot([0,4.2],[0,1.2],linestyle='--',linewidth=0.8)
ax.add_patch(Arc((0,0),1.0,1.0,theta1=0,theta2=np.degrees(np.arctan(1.2/4.2))))
ax.text(0.62,0.14,r'$\theta$',fontsize=11); ax.text(2.0,-0.2,'d',fontsize=10); ax.text(4.35,0.8,'x',fontsize=10); ax.text(-0.2,-0.15,'vertex',fontsize=9)
save('fig_09_07_detector_schematic.png')
# transform interval plot
xmm=np.linspace(0,5,400); c=1000/np.sqrt(1000**2+xmm**2)
plt.figure(figsize=(5.8,3.6))
plt.plot(xmm,c)
plt.axvline(2,linestyle='--',linewidth=1,label='measured x')
plt.axvspan(1,3,alpha=0.18,label='68.3% x interval')
plt.xlabel('x (mm)')
plt.ylabel(r'$\cos\theta$')
plt.title(r'Transforming an $x$ interval into a $\cos\theta$ interval')
plt.legend(fontsize=8)
save('fig_09_07_cos_interval.png')

# 11.1 resolution function and 11.2 matrix / response
cgrid=np.linspace(0.99998,1.0,600)
a=1000; sig=1; xp=2
xpos=a*np.sqrt(np.maximum(1-cgrid**2,0))/cgrid
# single-branch x>=0 case
sc=stats.norm.pdf(xpos, loc=xp, scale=sig)*a/(cgrid**2*np.sqrt(np.maximum(1-cgrid**2,1e-30)))
plt.figure(figsize=(5.8,3.6))
plt.plot(cgrid,sc/sc.max())
plt.xlabel(r'$c=\cos\theta$')
plt.ylabel('relative density')
plt.title('Resolution function after nonlinear transformation')
save('fig_11_01_cos_resolution.png')
M=8
G=np.zeros((M,M))
for i in range(M):
    if i==0 or i==M-1: G[i,i]=1
    else: G[i,i]=2
    if i<M-1: G[i,i+1]=G[i+1,i]=-1
plt.figure(figsize=(4.6,4.0))
plt.imshow(G,origin='upper')
plt.colorbar(label='$G_{ij}$')
plt.title('First-difference Tikhonov matrix')
plt.xlabel('j'); plt.ylabel('i')
save('fig_11_02_tikhonov_matrix.png')
# response example
R=np.zeros((8,8))
for i in range(8):
    for j in range(8):
        R[i,j]=np.exp(-0.5*((i-j)/1.0)**2)
R=R/R.sum(axis=0,keepdims=True)
plt.figure(figsize=(4.6,4.0))
plt.imshow(R,origin='lower')
plt.colorbar(label='$R_{ij}$')
plt.xlabel('true bin j'); plt.ylabel('observed bin i')
plt.title('Example response matrix for unfolding')
save('fig_11_04_response_matrix.png')

print(f'Wrote figures to {FIG}') 
