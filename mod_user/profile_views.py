from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from mod_user.utils import check_validation_code


@api_view(["POST"])
def change_password_with_code(request:Request):
    data=request.data
    result = check_validation_code(data)
    if not result.get("success"):
        return Response({"message":result.get("message")}, status=result.get("status"))

    user_code = result.get("message")
    # return a temporary token for changing password
    return Response({})