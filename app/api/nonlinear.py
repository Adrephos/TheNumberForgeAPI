from fastapi import APIRouter
import models.nonlinear as NonlinearModels
import services.nonlinear as NonlinearService
import models.response as response

router = APIRouter()


def columns_to_str(columns):
    return [[str(y) for y in x] for x in columns]


@router.post("/bisection")
def bisection(input_data: NonlinearModels.Bisection):
    try:
        result, table, error = NonlinearService.Bisection(
            input_data.a, input_data.b, input_data.tol,
            input_data.fx, input_data.niter
        )
        if error:
            return response.ResponseModel(None, False, error)

        data = {
            "result": result,
            "rows": table["rows"],
            "columns": columns_to_str(table["columns"]),
        }
        return response.ResponseModel(data, True, None)
    except Exception as e:
        return response.ResponseModel(None, False, str(e))
