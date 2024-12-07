"""
C and C++ implementation of QPALM
"""
from __future__ import annotations
import numpy
import scipy.sparse
import typing
__all__ = ['Data', 'Info', 'Settings', 'Solution', 'Solver', 'build_time', 'debug']
class Data:
    A: scipy.sparse.csc_matrix
    Q: scipy.sparse.csc_matrix
    bmax: numpy.ndarray
    bmin: numpy.ndarray
    c: float
    q: numpy.ndarray
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, n: int, m: int) -> None:
        ...
    def _get_c_data_ptr(self) -> _QPALMData:
        """
        Return a pointer to the C data struct (of type ::QPALMData).
        """
class Info:
    DUAL_INFEASIBLE: typing.ClassVar[int] = -4
    DUAL_TERMINATED: typing.ClassVar[int] = 2
    ERROR: typing.ClassVar[int] = 0
    MAX_ITER_REACHED: typing.ClassVar[int] = -2
    PRIMAL_INFEASIBLE: typing.ClassVar[int] = -3
    SOLVED: typing.ClassVar[int] = 1
    TIME_LIMIT_REACHED: typing.ClassVar[int] = -5
    UNSOLVED: typing.ClassVar[int] = -10
    USER_CANCELLATION: typing.ClassVar[int] = -6
    dua2_res_norm: float
    dua_res_norm: float
    dual_objective: float
    iter: int
    iter_out: int
    objective: float
    pri_res_norm: float
    run_time: float
    setup_time: float
    solve_time: float
    status: str
    status_val: int
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class Settings:
    delta: float
    dual_objective_limit: float
    enable_dual_termination: int
    eps_abs: float
    eps_abs_in: float
    eps_dual_inf: float
    eps_prim_inf: float
    eps_rel: float
    eps_rel_in: float
    factorization_method: int
    gamma_init: float
    gamma_max: float
    gamma_upd: float
    inner_max_iter: int
    max_iter: int
    max_rank_update: int
    max_rank_update_fraction: float
    nonconvex: int
    ordering: int
    print_iter: int
    proximal: int
    reset_newton_iter: int
    rho: float
    scaling: int
    sigma_init: float
    sigma_max: float
    theta: float
    time_limit: float
    verbose: int
    warm_start: int
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class Solution:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @property
    def x(self) -> numpy.ndarray:
        ...
    @property
    def y(self) -> numpy.ndarray:
        ...
class Solver:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, data: Data, settings: Settings) -> None:
        ...
    def _get_c_work_ptr(self) -> _QPALMWorkspace:
        """
        Return a pointer to the C workspace struct (of type ::QPALMWorkspace).
        """
    def cancel(self) -> None:
        ...
    def solve(self, asynchronous: bool = True, suppress_interrupt: bool = False) -> None:
        ...
    def update_Q_A(self, Q_vals: numpy.ndarray, A_vals: numpy.ndarray) -> None:
        ...
    def update_bounds(self, bmin: numpy.ndarray | None = None, bmax: numpy.ndarray | None = None) -> None:
        ...
    def update_q(self, q: numpy.ndarray) -> None:
        ...
    def update_settings(self, settings: Settings) -> None:
        ...
    def warm_start(self, x: numpy.ndarray | None = None, y: numpy.ndarray | None = None) -> None:
        ...
    @property
    def dual_inf_certificate(self) -> numpy.ndarray:
        ...
    @property
    def info(self) -> Info:
        ...
    @property
    def prim_inf_certificate(self) -> numpy.ndarray:
        ...
    @property
    def solution(self) -> Solution:
        ...
class _QPALMData:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class _QPALMWorkspace:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
__version__: str = '1.2.4'
build_time: str = 'Nov 15 2024 - 13:10:19'
debug: bool = True
