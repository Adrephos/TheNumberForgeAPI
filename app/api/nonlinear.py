from fastapi import APIRouter
import models.nonlinear as NonlinearModels
import services.nonlinear as NonlinearService
import models.response as response

router = APIRouter()


@router.post("/bisection")
def bisection(input_data: NonlinearModels.Bisection):
    try:
        result, table, error = NonlinearService.Bisection(
            input_data.a, input_data.b, input_data.fx,
            input_data.tol, input_data.niter, input_data.relativeError
        )
        if error:
            return response.ResponseModel(None, False, error)

        data = {
            "root": result,
            "columns": table["columns"],
            "rows": table["rows"],
        }
        return response.ResponseModel(data, True, None)
    except Exception as e:
        return response.ResponseModel(None, False, str(e))


@router.post("/fixed_point")
def fixed_point(input_data: NonlinearModels.FixedPoint):
    try:
        result, table, error = NonlinearService.Fixed_point(
            input_data.x0, input_data.fx, input_data.gx,
            input_data.tol, input_data.niter, input_data.relativeError
        )
        if error:
            return response.ResponseModel(None, False, error)

        data = {
            "root": result,
            "columns": table["columns"],
            "rows": table["rows"],
        }
        return response.ResponseModel(data, True, None)
    except Exception as e:
        return response.ResponseModel(None, False, str(e))


@router.post("/false_position")
def false_position(input_data: NonlinearModels.FalsePosition):
    try:
        result, table, error = NonlinearService.False_position(
            input_data.a, input_data.b, input_data.fx,
            input_data.tol, input_data.niter, input_data.relativeError
        )
        if error:
            return response.ResponseModel(None, False, error)

        data = {
            "root": result,
            "columns": table["columns"],
            "rows": table["rows"],
        }
        return response.ResponseModel(data, True, None)
    except Exception as e:
        return response.ResponseModel(None, False, str(e))


@router.post("/newton")
def newton(input_data: NonlinearModels.Newton):
    try:
        result, table, error = NonlinearService.Newton(
            input_data.x0, input_data.fx, input_data.tol,
            input_data.niter, input_data.relativeError
        )
        if error:
            return response.ResponseModel(None, False, error)

        data = {
            "root": result,
            "columns": table["columns"],
            "rows": table["rows"],
        }
        return response.ResponseModel(data, True, None)
    except Exception as e:
        return response.ResponseModel(None, False, str(e))


@router.post("/secant")
def secant(input_data: NonlinearModels.Secant):
    try:
        result, table, error = NonlinearService.Secant(
            input_data.x0, input_data.x1, input_data.fx,
            input_data.tol, input_data.niter, input_data.relativeError
        )
        if error:
            return response.ResponseModel(None, False, error)

        data = {
            "root": result,
            "columns": table["columns"],
            "rows": table["rows"],
        }
        return response.ResponseModel(data, True, None)
    except Exception as e:
        return response.ResponseModel(None, False, str(e))
