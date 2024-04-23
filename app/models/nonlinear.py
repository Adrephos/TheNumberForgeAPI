from pydantic import BaseModel


class Bisection(BaseModel):
    a: float
    b: float
    tol: float
    fx: str
    niter: int


class FixedPoint(BaseModel):
    x0: float
    tol: float
    fx: str
    gx: str
    niter: int


class FalsePosition(BaseModel):
    a: float
    b: float
    tol: float
    fx: str
    niter: int


class Newton(BaseModel):
    x0: float
    tol: float
    fx: str
    niter: int


class Secant(BaseModel):
    x0: float
    x1: float
    tol: float
    fx: str
    niter: int
