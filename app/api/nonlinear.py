from fastapi import APIRouter, Response, status
import models.nonlinear as NonlinearModels
import services.nonlinear as NonlinearService
from models.response import ResponseModel

router = APIRouter()


@router.post("/bisection")
def bisection(input_data: NonlinearModels.Bisection, response: Response):
    try:
        result, table, error = NonlinearService.Bisection(
            input_data.a, input_data.b, input_data.fx,
            input_data.tol, input_data.niter, input_data.relativeError
        )
        if error:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ResponseModel(None, False, error)

        data = {"root": result}

        if table is None:
            return ResponseModel(data, True, None)

        data["columns"] = table["columns"]
        data["rows"] = table["rows"]

        return ResponseModel(data, True, None)
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ResponseModel(None, False, str(e))


@router.post("/fixed_point")
def fixed_point(input_data: NonlinearModels.FixedPoint, response: Response):
    try:
        result, table, error = NonlinearService.Fixed_point(
            input_data.x0, input_data.fx, input_data.gx,
            input_data.tol, input_data.niter, input_data.relativeError
        )
        if error:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ResponseModel(None, False, error)

        data = {"root": result}

        if table is None:
            return ResponseModel(data, True, None)

        data["columns"] = table["columns"]
        data["rows"] = table["rows"]

        return ResponseModel(data, True, None)
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ResponseModel(None, False, str(e))


@router.post("/false_position")
def false_position(input_data: NonlinearModels.FalsePosition, response: Response):
    try:
        result, table, error = NonlinearService.False_position(
            input_data.a, input_data.b, input_data.fx,
            input_data.tol, input_data.niter, input_data.relativeError
        )
        if error:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ResponseModel(None, False, error)

        data = {"root": result}

        if table is None:
            return ResponseModel(data, True, None)

        data["columns"] = table["columns"]
        data["rows"] = table["rows"]

        return ResponseModel(data, True, None)
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ResponseModel(None, False, str(e))


@router.post("/newton")
def newton(input_data: NonlinearModels.Newton, response: Response):
    try:
        result, table, error = NonlinearService.Newton(
            input_data.x0, input_data.fx, input_data.tol,
            input_data.niter, input_data.relativeError
        )
        if error:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ResponseModel(None, False, error)

        data = {"root": result}

        if table is None:
            return ResponseModel(data, True, None)

        data["columns"] = table["columns"]
        data["rows"] = table["rows"]

        return ResponseModel(data, True, None)
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ResponseModel(None, False, str(e))


@router.post("/secant")
def secant(input_data: NonlinearModels.Secant, response: Response):
    try:
        result, table, error = NonlinearService.Secant(
            input_data.x0, input_data.x1, input_data.fx,
            input_data.tol, input_data.niter, input_data.relativeError
        )
        if error:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ResponseModel(None, False, error)

        data = {"root": result}

        if table is None:
            return ResponseModel(data, True, None)

        data["columns"] = table["columns"]
        data["rows"] = table["rows"]

        return ResponseModel(data, True, None)
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ResponseModel(None, False, str(e))
