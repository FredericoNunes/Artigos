"""

Authors: Chase Coleman, John Stachurski

"""
import numpy as np
import random
import quantecon as qe
from numba import jit


class Arellano_Economy:
    """
    Arellano 2008 deals with a small open economy whose government
    invests in foreign assets in order to smooth the consumption of
    domestic households. Domestic households receive a stochastic
    path of income.

    Parameters
    ----------
    β : float
        Time discounting parameter
    γ : float
        Risk-aversion parameter
    r : float
        int lending rate
    ρ : float
        Persistence in the income process
    η : float
        Standard deviation of the income process
    θ : float
        Probability of re-entering financial markets in each period
    ny : int
        Number of points in y grid
    nB : int
        Number of points in B grid
    tol : float
        Error tolerance in iteration
    maxit : int
        Maximum number of iterations
    """

    def __init__(self,
                 β=.953,         # time discount rate
                 γ=2.,           # risk aversion
                 r=0.017,        # international interest rate
                 ρ=.945,         # persistence in output
                 η=0.025,        # st dev of output shock
                 θ=0.282,        # prob of regaining access
                 ny=21,          # number of points in y grid
                 nB=251,         # number of points in B grid
                 tol=1e-8,       # error tolerance in iteration
                 maxit=10000,
                 ydefcost=0.94):

        # Save parameters
        self.β, self.γ, self.r = β, γ, r
        self.ρ, self.η, self.θ = ρ, η, θ
        self.ny, self.nB = ny, nB
        self.ydefcost  = ydefcost

        # Create grids and discretize Markov process
        self.Bgrid = np.linspace(-.45, .45, nB)
            ## Alteramos a dirscretização porque o rho (coefieciente de AR(1) se aproxima muito de 1)
            ## Era Markov Tauchen e passamos para o Rouwenhorsr
        # self.mc = qe.markov.tauchen(ρ, η, 3, ny)
        self.mc = qe.markov.approximation.rouwenhorst(ny, 0, η, ρ)


        self.ygrid = np.exp(self.mc.state_values)
        self.Py = self.mc.P

        # Output when in default
        ymean = np.mean(self.ygrid)
        self.def_y = np.minimum(self.ydefcost * ymean, self.ygrid)

        # Allocate memory
        self.Vd = np.zeros(ny)
        self.Vc = np.zeros((ny, nB))
        self.V = np.zeros((ny, nB))
        self.Q = np.ones((ny, nB)) * .95  # Initial guess for prices
        self.default_prob = np.empty((ny, nB))

        # Compute the value functions, prices, and default prob
        self.solve(tol=tol, maxit=maxit)
        # Compute the optimal savings policy conditional on no default
        self.compute_savings_policy()

    def solve(self, tol=1e-8, maxit=10000):
        # Iteration Stuff
        it = 0
        dist = 10.

        # Alloc memory to store next iterate of value function
        V_upd = np.zeros((self.ny, self.nB))

        # == Main loop == #
        while dist > tol and maxit > it:

            # Compute expectations for this iteration
            Vs = self.V, self.Vd, self.Vc
            EV, EVd, EVc = (self.Py @ v for v in Vs)

            # Run inner loop to update value functions Vc and Vd.
            # Note that Vc and Vd are updated in place.  Other objects
            # are not modified.
            _inner_loop(self.ygrid, self.def_y,
                        self.Bgrid, self.Vd, self.Vc,
                        EVc, EVd, EV, self.Q,
                        self.β, self.θ, self.γ)

            # Update prices
            Vd_compat = np.repeat(self.Vd, self.nB).reshape(self.ny, self.nB)
            default_states = Vd_compat > self.Vc
            self.default_prob[:, :] = self.Py @ default_states
            self.Q[:, :] = (1 - self.default_prob)/(1 + self.r)

            # Update main value function and distance
            V_upd[:, :] = np.maximum(self.Vc, Vd_compat)
            dist = np.max(np.abs(V_upd - self.V))
            self.V[:, :] = V_upd[:, :]

            it += 1
            if it % 25 == 0:
                print(f"Running iteration {it} with dist of {dist}")

        return None

    def compute_savings_policy(self):
        """
        Compute optimal savings B' conditional on not defaulting.
        The policy is recorded as an index value in Bgrid.
        """

        # Allocate memory
        self.next_B_index = np.empty((self.ny, self.nB))
        EV = self.Py @ self.V

        _compute_savings_policy(self.ygrid, self.Bgrid, self.Q, EV,
                                self.γ, self.β, self.next_B_index)

    def simulate(self, T, y_init=None, B_init=None):
        """
        Simulate time series for output, consumption, B'.
        """
        # Find index i such that Bgrid[i] is near 0
        zero_B_index = np.searchsorted(self.Bgrid, 0)

        if y_init is None:
            # Set to index near the mean of the ygrid
            y_init = np.searchsorted(self.ygrid, self.ygrid.mean())
        if B_init is None:
            B_init = zero_B_index
        # Start off not in default
        in_default = False

        y_sim_indices = self.mc.simulate_indices(T, init=y_init)
        B_sim_indices = np.empty(T, dtype=np.int64)
        B_sim_indices[0] = B_init
        q_sim = np.empty(T)
        c_sim = np.empty(T)
        in_default_series = np.zeros(T, dtype=np.int64)

        for t in range(T-1):
            yi, Bi = y_sim_indices[t], B_sim_indices[t]
            if not in_default:
                if self.Vc[yi, Bi] < self.Vd[yi]:
                    in_default = True
                    Bi_next = zero_B_index
                else:
                    new_index = self.next_B_index[yi, Bi]
                    Bi_next = new_index
            else:
                in_default_series[t] = 1
                Bi_next = zero_B_index
                if random.uniform(0, 1) < self.θ:
                    in_default = False
            B_sim_indices[t+1] = Bi_next
            q_sim[t] = self.Q[yi, int(Bi_next)]
            c_sim[t] = self.ygrid[yi] - self.Q[yi, int(Bi_next)]*self.Bgrid[int(Bi_next)] + self.Bgrid[int(Bi_next)-1]

        q_sim[-1] = q_sim[-2]  # Extrapolate for the last price
        return_vecs = (self.ygrid[y_sim_indices],
                       self.Bgrid[B_sim_indices],
                       q_sim,
                       c_sim,
                       in_default_series)

        return return_vecs


@jit(nopython=True)
def u(c, γ):
    return c**(1-γ)/(1-γ)


@jit(nopython=True)
def _inner_loop(ygrid, def_y, Bgrid, Vd, Vc, EVc,
                EVd, EV, qq, β, θ, γ):
    """
    This is a numba version of the inner loop of the solve in the
    Arellano class. It updates Vd and Vc in place.
    """
    ny, nB = len(ygrid), len(Bgrid)
    zero_ind = nB // 2  # Integer division
    for iy in range(ny):
        y = ygrid[iy]   # Pull out current y

        # Compute Vd
        Vd[iy] = u(def_y[iy], γ) + \
                β * (θ * EVc[iy, zero_ind] + (1 - θ) * EVd[iy])

        # Compute Vc
        for ib in range(nB):
            B = Bgrid[ib]  # Pull out current B

            current_max = -1e14
            for ib_next in range(nB):
                c = max(y - qq[iy, ib_next] * Bgrid[ib_next] + B, 1e-14)
                m = u(c, γ) + β * EV[iy, ib_next]
                if m > current_max:
                    current_max = m
            Vc[iy, ib] = current_max

    return None


@jit(nopython=True)
def _compute_savings_policy(ygrid, Bgrid, Q, EV, γ, β, next_B_index):
    # Compute best index in Bgrid given iy, ib
    ny, nB = len(ygrid), len(Bgrid)
    for iy in range(ny):
        y = ygrid[iy]
        for ib in range(nB):
            B = Bgrid[ib]
            current_max = -1e10
            for ib_next in range(nB):
                c = max(y - Q[iy, ib_next] * Bgrid[ib_next] + B, 1e-14)
                m = u(c, γ) + β * EV[iy, ib_next]
                if m > current_max:
                    current_max = m
                    current_max_index = ib_next
            next_B_index[iy, ib] = current_max_index

    #print(next_B_index)
    return None