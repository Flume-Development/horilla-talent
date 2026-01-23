from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.db.models import Q, ProtectedError

from pms.models import (
    Period,
    KeyResult,
    Objective,
    EmployeeObjective,
    EmployeeKeyResult,
    Comment,
    QuestionTemplate,
    Question,
    QuestionOptions,
    Feedback,
    Answer,
    AnonymousFeedback,
    Meetings,
    MeetingsAnswer,
    BonusPointSetting,
    EmployeeBonusPoint,
    KeyResultFeedback,
)
from employee.models import Employee
from pms.filters import (
    ObjectiveFilter,
    EmployeeObjectiveFilter,
    KeyResultFilter,
    FeedbackFilter,
    MeetingsFilter,
    AnonymousFeedbackFilter,
    BonusPointSettingFilter,
    EmployeeBonusPointFilter,
)

from horilla_api.api_serializers.pms.serializers import (
    PeriodSerializer,
    KeyResultSerializer,
    ObjectiveSerializer,
    EmployeeObjectiveSerializer,
    EmployeeKeyResultSerializer,
    CommentSerializer,
    QuestionTemplateSerializer,
    QuestionSerializer,
    QuestionOptionsSerializer,
    FeedbackSerializer,
    AnswerSerializer,
    AnonymousFeedbackSerializer,
    MeetingsSerializer,
    MeetingsAnswerSerializer,
    BonusPointSettingSerializer,
    EmployeeBonusPointSerializer,
    KeyResultFeedbackSerializer,
)
from horilla_api.api_decorators.base.decorators import permission_required


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination for API responses"""
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


# ============ Period API Views ============
class PeriodListAPIView(APIView):
    """List all periods"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        paginator = StandardResultsSetPagination()
        periods = Period.objects.all()
        page = paginator.paginate_queryset(periods, request)
        serializer = PeriodSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class PeriodAPIView(APIView):
    """Create, retrieve, update, or delete a period"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                period = Period.objects.get(id=pk)
                serializer = PeriodSerializer(period)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Period.DoesNotExist:
                return Response(
                    {"error": "Period not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            {"error": "Period ID required"}, status=status.HTTP_400_BAD_REQUEST
        )

    @method_decorator(permission_required("pms.add_period"))
    def post(self, request):
        serializer = PeriodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(permission_required("pms.change_period"))
    def put(self, request, pk):
        try:
            period = Period.objects.get(id=pk)
            serializer = PeriodSerializer(period, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Period.DoesNotExist:
            return Response(
                {"error": "Period not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @method_decorator(permission_required("pms.delete_period"))
    def delete(self, request, pk):
        try:
            period = Period.objects.get(id=pk)
            period.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Period.DoesNotExist:
            return Response(
                {"error": "Period not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except ProtectedError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ============ KeyResult API Views ============
class KeyResultListAPIView(APIView):
    """List all key results with filtering"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = KeyResultFilter

    def get(self, request):
        paginator = StandardResultsSetPagination()
        key_results = KeyResult.objects.all()

        # Apply filters
        filterset = KeyResultFilter(request.GET, queryset=key_results)
        key_results = filterset.qs

        page = paginator.paginate_queryset(key_results, request)
        serializer = KeyResultSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class KeyResultAPIView(APIView):
    """Create, retrieve, update, or delete a key result"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                kr = KeyResult.objects.get(id=pk)
                serializer = KeyResultSerializer(kr)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except KeyResult.DoesNotExist:
                return Response(
                    {"error": "Key Result not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            {"error": "Key Result ID required"}, status=status.HTTP_400_BAD_REQUEST
        )

    @method_decorator(permission_required("pms.add_keyresult"))
    def post(self, request):
        serializer = KeyResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(permission_required("pms.change_keyresult"))
    def put(self, request, pk):
        try:
            kr = KeyResult.objects.get(id=pk)
            serializer = KeyResultSerializer(kr, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyResult.DoesNotExist:
            return Response(
                {"error": "Key Result not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @method_decorator(permission_required("pms.delete_keyresult"))
    def delete(self, request, pk):
        try:
            kr = KeyResult.objects.get(id=pk)
            kr.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except KeyResult.DoesNotExist:
            return Response(
                {"error": "Key Result not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except ProtectedError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ============ Objective API Views ============
class ObjectiveListAPIView(APIView):
    """List all objectives with filtering"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ObjectiveFilter

    def get(self, request):
        paginator = StandardResultsSetPagination()
        objectives = Objective.objects.all()

        # Apply filters
        filterset = ObjectiveFilter(request.GET, queryset=objectives)
        objectives = filterset.qs

        page = paginator.paginate_queryset(objectives, request)
        serializer = ObjectiveSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ObjectiveAPIView(APIView):
    """Create, retrieve, update, or delete an objective"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                objective = Objective.objects.get(id=pk)
                serializer = ObjectiveSerializer(objective)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Objective.DoesNotExist:
                return Response(
                    {"error": "Objective not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            {"error": "Objective ID required"}, status=status.HTTP_400_BAD_REQUEST
        )

    @method_decorator(permission_required("pms.add_objective"))
    def post(self, request):
        serializer = ObjectiveSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            # Handle ManyToMany relationships
            if "manager_ids" in request.data:
                obj.managers.set(request.data["manager_ids"])
            if "assignee_ids" in request.data:
                obj.assignees.set(request.data["assignee_ids"])
            if "key_result_ids" in request.data:
                obj.key_result_id.set(request.data["key_result_ids"])
            return Response(ObjectiveSerializer(obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(permission_required("pms.change_objective"))
    def put(self, request, pk):
        try:
            objective = Objective.objects.get(id=pk)
            serializer = ObjectiveSerializer(objective, data=request.data, partial=True)
            if serializer.is_valid():
                obj = serializer.save()
                # Handle ManyToMany relationships
                if "manager_ids" in request.data:
                    obj.managers.set(request.data["manager_ids"])
                if "assignee_ids" in request.data:
                    obj.assignees.set(request.data["assignee_ids"])
                if "key_result_ids" in request.data:
                    obj.key_result_id.set(request.data["key_result_ids"])
                return Response(ObjectiveSerializer(obj).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Objective.DoesNotExist:
            return Response(
                {"error": "Objective not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @method_decorator(permission_required("pms.delete_objective"))
    def delete(self, request, pk):
        try:
            objective = Objective.objects.get(id=pk)
            objective.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Objective.DoesNotExist:
            return Response(
                {"error": "Objective not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except ProtectedError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ObjectiveArchiveAPIView(APIView):
    """Archive an objective"""
    permission_classes = [IsAuthenticated]

    @method_decorator(permission_required("pms.change_objective"))
    def post(self, request, pk):
        try:
            objective = Objective.objects.get(id=pk)
            objective.archive = True
            objective.save()
            return Response(ObjectiveSerializer(objective).data, status=status.HTTP_200_OK)
        except Objective.DoesNotExist:
            return Response(
                {"error": "Objective not found"}, status=status.HTTP_404_NOT_FOUND
            )


# ============ Employee Objective API Views ============
class EmployeeObjectiveListAPIView(APIView):
    """List all employee objectives with filtering"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeObjectiveFilter

    def get(self, request):
        paginator = StandardResultsSetPagination()
        user = request.user
        employee_objectives = EmployeeObjective.objects.all()

        # Filter by user's own objectives or subordinates' if manager
        if not user.has_perm("pms.view_employeeobjective"):
            employee_objectives = employee_objectives.filter(
                Q(employee_id=user.employee_get)
                | Q(objective_id__managers=user.employee_get)
            ).distinct()

        # Apply filters
        filterset = EmployeeObjectiveFilter(request.GET, queryset=employee_objectives)
        employee_objectives = filterset.qs

        page = paginator.paginate_queryset(employee_objectives, request)
        serializer = EmployeeObjectiveSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class EmployeeObjectiveAPIView(APIView):
    """Create, retrieve, update, or delete an employee objective"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                emp_obj = EmployeeObjective.objects.get(id=pk)
                serializer = EmployeeObjectiveSerializer(emp_obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except EmployeeObjective.DoesNotExist:
                return Response(
                    {"error": "Employee Objective not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(
            {"error": "Employee Objective ID required"}, status=status.HTTP_400_BAD_REQUEST
        )

    @method_decorator(permission_required("pms.add_employeeobjective"))
    def post(self, request):
        serializer = EmployeeObjectiveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(permission_required("pms.change_employeeobjective"))
    def put(self, request, pk):
        try:
            emp_obj = EmployeeObjective.objects.get(id=pk)
            serializer = EmployeeObjectiveSerializer(emp_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EmployeeObjective.DoesNotExist:
            return Response(
                {"error": "Employee Objective not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @method_decorator(permission_required("pms.delete_employeeobjective"))
    def delete(self, request, pk):
        try:
            emp_obj = EmployeeObjective.objects.get(id=pk)
            emp_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EmployeeObjective.DoesNotExist:
            return Response(
                {"error": "Employee Objective not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ProtectedError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeObjectiveStatusUpdateAPIView(APIView):
    """Update status of an employee objective"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            emp_obj = EmployeeObjective.objects.get(id=pk)
            status_value = request.data.get("status")
            if not status_value:
                return Response(
                    {"error": "Status is required"}, status=status.HTTP_400_BAD_REQUEST
                )
            emp_obj.status = status_value
            emp_obj.save()
            return Response(EmployeeObjectiveSerializer(emp_obj).data, status=status.HTTP_200_OK)
        except EmployeeObjective.DoesNotExist:
            return Response(
                {"error": "Employee Objective not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


# ============ Employee Key Result API Views ============
class EmployeeKeyResultListAPIView(APIView):
    """List all employee key results"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        paginator = StandardResultsSetPagination()
        user = request.user
        employee_key_results = EmployeeKeyResult.objects.all()

        # Filter by user's own KRs or subordinates' if manager
        if not user.has_perm("pms.view_employeekeyresult"):
            employee_key_results = employee_key_results.filter(
                employee_objective_id__employee_id=user.employee_get
            )

        page = paginator.paginate_queryset(employee_key_results, request)
        serializer = EmployeeKeyResultSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class EmployeeKeyResultAPIView(APIView):
    """Create, retrieve, update, or delete an employee key result"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                emp_kr = EmployeeKeyResult.objects.get(id=pk)
                serializer = EmployeeKeyResultSerializer(emp_kr)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except EmployeeKeyResult.DoesNotExist:
                return Response(
                    {"error": "Employee Key Result not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(
            {"error": "Employee Key Result ID required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @method_decorator(permission_required("pms.add_employeekeyresult"))
    def post(self, request):
        serializer = EmployeeKeyResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(permission_required("pms.change_employeekeyresult"))
    def put(self, request, pk):
        try:
            emp_kr = EmployeeKeyResult.objects.get(id=pk)
            serializer = EmployeeKeyResultSerializer(emp_kr, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EmployeeKeyResult.DoesNotExist:
            return Response(
                {"error": "Employee Key Result not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @method_decorator(permission_required("pms.delete_employeekeyresult"))
    def delete(self, request, pk):
        try:
            emp_kr = EmployeeKeyResult.objects.get(id=pk)
            emp_kr.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EmployeeKeyResult.DoesNotExist:
            return Response(
                {"error": "Employee Key Result not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class EmployeeKeyResultProgressUpdateAPIView(APIView):
    """Update progress of an employee key result"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            emp_kr = EmployeeKeyResult.objects.get(id=pk)
            current_value = request.data.get("current_value")
            if current_value is None:
                return Response(
                    {"error": "current_value is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            emp_kr.current_value = current_value
            emp_kr.save()
            return Response(
                EmployeeKeyResultSerializer(emp_kr).data, status=status.HTTP_200_OK
            )
        except EmployeeKeyResult.DoesNotExist:
            return Response(
                {"error": "Employee Key Result not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


# ============ Comment API Views ============
class CommentListAPIView(APIView):
    """List all comments for an employee objective"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        emp_obj_id = request.query_params.get("employee_objective_id")
        if not emp_obj_id:
            return Response(
                {"error": "employee_objective_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        comments = Comment.objects.filter(employee_objective_id=emp_obj_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentAPIView(APIView):
    """Create, retrieve, update, or delete a comment"""
    permission_classes = [IsAuthenticated]

    @method_decorator(permission_required("pms.add_comment"))
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            # Set the employee as the current user
            comment = serializer.save(employee_id=request.user.employee_get)
            return Response(
                CommentSerializer(comment).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(permission_required("pms.delete_comment"))
    def delete(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response(
                {"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
            )


# ============ QuestionTemplate API Views ============
class QuestionTemplateListAPIView(APIView):
    """List all question templates"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        paginator = StandardResultsSetPagination()
        templates = QuestionTemplate.objects.all()
        page = paginator.paginate_queryset(templates, request)
        serializer = QuestionTemplateSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class QuestionTemplateAPIView(APIView):
    """Create, retrieve, update, or delete a question template"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                template = QuestionTemplate.objects.get(id=pk)
                serializer = QuestionTemplateSerializer(template)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except QuestionTemplate.DoesNotExist:
                return Response(
                    {"error": "Question Template not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(
            {"error": "Question Template ID required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @method_decorator(permission_required("pms.add_questiontemplate"))
    def post(self, request):
        serializer = QuestionTemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(permission_required("pms.change_questiontemplate"))
    def put(self, request, pk):
        try:
            template = QuestionTemplate.objects.get(id=pk)
            serializer = QuestionTemplateSerializer(template, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except QuestionTemplate.DoesNotExist:
            return Response(
                {"error": "Question Template not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @method_decorator(permission_required("pms.delete_questiontemplate"))
    def delete(self, request, pk):
        try:
            template = QuestionTemplate.objects.get(id=pk)
            template.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except QuestionTemplate.DoesNotExist:
            return Response(
                {"error": "Question Template not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


# ============ Question API Views ============
class QuestionListAPIView(APIView):
    """List all questions for a template"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        template_id = request.query_params.get("template_id")
        if not template_id:
            return Response(
                {"error": "template_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        questions = Question.objects.filter(template_id=template_id).order_by("ordering")
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionAPIView(APIView):
    """Create, retrieve, update, or delete a question"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                question = Question.objects.get(id=pk)
                serializer = QuestionSerializer(question)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Question.DoesNotExist:
                return Response(
                    {"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            {"error": "Question ID required"}, status=status.HTTP_400_BAD_REQUEST
        )

    @method_decorator(permission_required("pms.add_question"))
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(permission_required("pms.change_question"))
    def put(self, request, pk):
        try:
            question = Question.objects.get(id=pk)
            serializer = QuestionSerializer(question, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Question.DoesNotExist:
            return Response(
                {"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @method_decorator(permission_required("pms.delete_question"))
    def delete(self, request, pk):
        try:
            question = Question.objects.get(id=pk)
            question.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Question.DoesNotExist:
            return Response(
                {"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND
            )


# ============ Feedback API Views ============
class FeedbackListAPIView(APIView):
    """List all feedback cycles with filtering"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FeedbackFilter

    def get(self, request):
        paginator = StandardResultsSetPagination()
        user = request.user
        feedback_list = Feedback.objects.all()

        # Filter by user's feedback or their subordinates' if manager
        if not user.has_perm("pms.view_feedback"):
            feedback_list = feedback_list.filter(
                Q(employee_id=user.employee_get)
                | Q(manager_id=user.employee_get)
                | Q(colleague_id=user.employee_get)
                | Q(subordinate_id=user.employee_get)
                | Q(others_id=user.employee_get)
            ).distinct()

        # Apply filters
        filterset = FeedbackFilter(request.GET, queryset=feedback_list)
        feedback_list = filterset.qs

        page = paginator.paginate_queryset(feedback_list, request)
        serializer = FeedbackSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class FeedbackAPIView(APIView):
    """Create, retrieve, update, or delete feedback"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                feedback = Feedback.objects.get(id=pk)
                serializer = FeedbackSerializer(feedback)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Feedback.DoesNotExist:
                return Response(
                    {"error": "Feedback not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            {"error": "Feedback ID required"}, status=status.HTTP_400_BAD_REQUEST
        )

    @method_decorator(permission_required("pms.add_feedback"))
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            feedback = serializer.save()
            # Handle ManyToMany relationships
            if "colleague_ids" in request.data:
                feedback.colleague_id.set(request.data["colleague_ids"])
            if "subordinate_ids" in request.data:
                feedback.subordinate_id.set(request.data["subordinate_ids"])
            if "others_ids" in request.data:
                feedback.others_id.set(request.data["others_ids"])
            return Response(
                FeedbackSerializer(feedback).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(permission_required("pms.change_feedback"))
    def put(self, request, pk):
        try:
            feedback = Feedback.objects.get(id=pk)
            serializer = FeedbackSerializer(feedback, data=request.data, partial=True)
            if serializer.is_valid():
                fb = serializer.save()
                # Handle ManyToMany relationships
                if "colleague_ids" in request.data:
                    fb.colleague_id.set(request.data["colleague_ids"])
                if "subordinate_ids" in request.data:
                    fb.subordinate_id.set(request.data["subordinate_ids"])
                if "others_ids" in request.data:
                    fb.others_id.set(request.data["others_ids"])
                return Response(FeedbackSerializer(fb).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Feedback.DoesNotExist:
            return Response(
                {"error": "Feedback not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @method_decorator(permission_required("pms.delete_feedback"))
    def delete(self, request, pk):
        try:
            feedback = Feedback.objects.get(id=pk)
            feedback.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Feedback.DoesNotExist:
            return Response(
                {"error": "Feedback not found"}, status=status.HTTP_404_NOT_FOUND
            )


class FeedbackArchiveAPIView(APIView):
    """Archive a feedback cycle"""
    permission_classes = [IsAuthenticated]

    @method_decorator(permission_required("pms.change_feedback"))
    def post(self, request, pk):
        try:
            feedback = Feedback.objects.get(id=pk)
            feedback.archive = True
            feedback.save()
            return Response(FeedbackSerializer(feedback).data, status=status.HTTP_200_OK)
        except Feedback.DoesNotExist:
            return Response(
                {"error": "Feedback not found"}, status=status.HTTP_404_NOT_FOUND
            )


class FeedbackAnswerSubmitAPIView(APIView):
    """Submit answers to a feedback"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            feedback = Feedback.objects.get(id=pk)
            answers = request.data.get("answers", [])
            employee = request.user.employee_get

            # Delete existing answers from this employee for this feedback
            Answer.objects.filter(feedback_id=feedback, employee_id=employee).delete()

            # Create new answers
            for answer_data in answers:
                answer = Answer.objects.create(
                    feedback_id=feedback,
                    employee_id=employee,
                    question_id_id=answer_data.get("question_id"),
                    answer=answer_data.get("answer"),
                )

            return Response(
                {"message": "Answers submitted successfully"}, status=status.HTTP_201_CREATED
            )
        except Feedback.DoesNotExist:
            return Response(
                {"error": "Feedback not found"}, status=status.HTTP_404_NOT_FOUND
            )


class FeedbackAnswersViewAPIView(APIView):
    """View all answers for a feedback"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            feedback = Feedback.objects.get(id=pk)
            answers = Answer.objects.filter(feedback_id=feedback)
            serializer = AnswerSerializer(answers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Feedback.DoesNotExist:
            return Response(
                {"error": "Feedback not found"}, status=status.HTTP_404_NOT_FOUND
            )


# ============ Meetings API Views ============
class MeetingsListAPIView(APIView):
    """List all meetings with filtering"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MeetingsFilter

    def get(self, request):
        paginator = StandardResultsSetPagination()
        user = request.user
        meetings = Meetings.objects.all()

        # Filter by user's meetings
        if not user.has_perm("pms.view_meetings"):
            meetings = meetings.filter(
                Q(employee_id=user.employee_get) | Q(manager=user.employee_get)
            ).distinct()

        # Apply filters
        filterset = MeetingsFilter(request.GET, queryset=meetings)
        meetings = filterset.qs

        page = paginator.paginate_queryset(meetings, request)
        serializer = MeetingsSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class MeetingsAPIView(APIView):
    """Create, retrieve, update, or delete a meeting"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                meeting = Meetings.objects.get(id=pk)
                serializer = MeetingsSerializer(meeting)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Meetings.DoesNotExist:
                return Response(
                    {"error": "Meeting not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            {"error": "Meeting ID required"}, status=status.HTTP_400_BAD_REQUEST
        )

    @method_decorator(permission_required("pms.add_meetings"))
    def post(self, request):
        serializer = MeetingsSerializer(data=request.data)
        if serializer.is_valid():
            meeting = serializer.save()
            # Handle ManyToMany relationships
            if "employee_ids" in request.data:
                meeting.employee_id.set(request.data["employee_ids"])
            if "manager_ids" in request.data:
                meeting.manager.set(request.data["manager_ids"])
            if "answer_employee_ids" in request.data:
                meeting.answer_employees.set(request.data["answer_employee_ids"])
            return Response(
                MeetingsSerializer(meeting).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(permission_required("pms.change_meetings"))
    def put(self, request, pk):
        try:
            meeting = Meetings.objects.get(id=pk)
            serializer = MeetingsSerializer(meeting, data=request.data, partial=True)
            if serializer.is_valid():
                mtg = serializer.save()
                # Handle ManyToMany relationships
                if "employee_ids" in request.data:
                    mtg.employee_id.set(request.data["employee_ids"])
                if "manager_ids" in request.data:
                    mtg.manager.set(request.data["manager_ids"])
                if "answer_employee_ids" in request.data:
                    mtg.answer_employees.set(request.data["answer_employee_ids"])
                return Response(MeetingsSerializer(mtg).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Meetings.DoesNotExist:
            return Response(
                {"error": "Meeting not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @method_decorator(permission_required("pms.delete_meetings"))
    def delete(self, request, pk):
        try:
            meeting = Meetings.objects.get(id=pk)
            meeting.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Meetings.DoesNotExist:
            return Response(
                {"error": "Meeting not found"}, status=status.HTTP_404_NOT_FOUND
            )


class MeetingAnswersViewAPIView(APIView):
    """View all answers for a meeting"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            meeting = Meetings.objects.get(id=pk)
            answers = MeetingsAnswer.objects.filter(meeting_id=meeting)
            serializer = MeetingsAnswerSerializer(answers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Meetings.DoesNotExist:
            return Response(
                {"error": "Meeting not found"}, status=status.HTTP_404_NOT_FOUND
            )


class MeetingAnswerSubmitAPIView(APIView):
    """Submit answers to a meeting"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            meeting = Meetings.objects.get(id=pk)
            answers = request.data.get("answers", [])
            employee = request.user.employee_get

            # Delete existing answers from this employee for this meeting
            MeetingsAnswer.objects.filter(meeting_id=meeting, employee_id=employee).delete()

            # Create new answers
            for answer_data in answers:
                answer = MeetingsAnswer.objects.create(
                    meeting_id=meeting,
                    employee_id=employee,
                    question_id_id=answer_data.get("question_id"),
                    answer=answer_data.get("answer"),
                )

            return Response(
                {"message": "Answers submitted successfully"}, status=status.HTTP_201_CREATED
            )
        except Meetings.DoesNotExist:
            return Response(
                {"error": "Meeting not found"}, status=status.HTTP_404_NOT_FOUND
            )


# ============ Anonymous Feedback API Views ============
class AnonymousFeedbackListAPIView(APIView):
    """List all anonymous feedback with filtering"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnonymousFeedbackFilter

    def get(self, request):
        paginator = StandardResultsSetPagination()
        feedback = AnonymousFeedback.objects.all()

        # Apply filters
        filterset = AnonymousFeedbackFilter(request.GET, queryset=feedback)
        feedback = filterset.qs

        page = paginator.paginate_queryset(feedback, request)
        serializer = AnonymousFeedbackSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class AnonymousFeedbackAPIView(APIView):
    """Create, retrieve, update, or delete anonymous feedback"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                feedback = AnonymousFeedback.objects.get(id=pk)
                serializer = AnonymousFeedbackSerializer(feedback)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except AnonymousFeedback.DoesNotExist:
                return Response(
                    {"error": "Anonymous Feedback not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(
            {"error": "Anonymous Feedback ID required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @method_decorator(permission_required("pms.add_anonymousfeedback"))
    def post(self, request):
        serializer = AnonymousFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(permission_required("pms.change_anonymousfeedback"))
    def put(self, request, pk):
        try:
            feedback = AnonymousFeedback.objects.get(id=pk)
            serializer = AnonymousFeedbackSerializer(feedback, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AnonymousFeedback.DoesNotExist:
            return Response(
                {"error": "Anonymous Feedback not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @method_decorator(permission_required("pms.delete_anonymousfeedback"))
    def delete(self, request, pk):
        try:
            feedback = AnonymousFeedback.objects.get(id=pk)
            feedback.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AnonymousFeedback.DoesNotExist:
            return Response(
                {"error": "Anonymous Feedback not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


# ============ Bonus Point API Views ============
class BonusPointSettingListAPIView(APIView):
    """List all bonus point settings with filtering"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BonusPointSettingFilter

    def get(self, request):
        paginator = StandardResultsSetPagination()
        settings = BonusPointSetting.objects.all()

        # Apply filters
        filterset = BonusPointSettingFilter(request.GET, queryset=settings)
        settings = filterset.qs

        page = paginator.paginate_queryset(settings, request)
        serializer = BonusPointSettingSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class BonusPointSettingAPIView(APIView):
    """Create, retrieve, update, or delete a bonus point setting"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                setting = BonusPointSetting.objects.get(id=pk)
                serializer = BonusPointSettingSerializer(setting)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except BonusPointSetting.DoesNotExist:
                return Response(
                    {"error": "Bonus Point Setting not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(
            {"error": "Bonus Point Setting ID required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @method_decorator(permission_required("pms.add_bonuspointsetting"))
    def post(self, request):
        serializer = BonusPointSettingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(permission_required("pms.change_bonuspointsetting"))
    def put(self, request, pk):
        try:
            setting = BonusPointSetting.objects.get(id=pk)
            serializer = BonusPointSettingSerializer(setting, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BonusPointSetting.DoesNotExist:
            return Response(
                {"error": "Bonus Point Setting not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @method_decorator(permission_required("pms.delete_bonuspointsetting"))
    def delete(self, request, pk):
        try:
            setting = BonusPointSetting.objects.get(id=pk)
            setting.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BonusPointSetting.DoesNotExist:
            return Response(
                {"error": "Bonus Point Setting not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class EmployeeBonusPointListAPIView(APIView):
    """List all employee bonus points with filtering"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeBonusPointFilter

    def get(self, request):
        paginator = StandardResultsSetPagination()
        bonus_points = EmployeeBonusPoint.objects.all()

        # Apply filters
        filterset = EmployeeBonusPointFilter(request.GET, queryset=bonus_points)
        bonus_points = filterset.qs

        page = paginator.paginate_queryset(bonus_points, request)
        serializer = EmployeeBonusPointSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class EmployeeBonusPointAPIView(APIView):
    """Create, retrieve, update, or delete an employee bonus point"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                bonus_point = EmployeeBonusPoint.objects.get(id=pk)
                serializer = EmployeeBonusPointSerializer(bonus_point)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except EmployeeBonusPoint.DoesNotExist:
                return Response(
                    {"error": "Employee Bonus Point not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(
            {"error": "Employee Bonus Point ID required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @method_decorator(permission_required("pms.add_employeebonuspoint"))
    def post(self, request):
        serializer = EmployeeBonusPointSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(permission_required("pms.change_employeebonuspoint"))
    def put(self, request, pk):
        try:
            bonus_point = EmployeeBonusPoint.objects.get(id=pk)
            serializer = EmployeeBonusPointSerializer(bonus_point, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EmployeeBonusPoint.DoesNotExist:
            return Response(
                {"error": "Employee Bonus Point not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @method_decorator(permission_required("pms.delete_employeebonuspoint"))
    def delete(self, request, pk):
        try:
            bonus_point = EmployeeBonusPoint.objects.get(id=pk)
            bonus_point.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EmployeeBonusPoint.DoesNotExist:
            return Response(
                {"error": "Employee Bonus Point not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


# ============ Dashboard API View ============
class DashboardStatsAPIView(APIView):
    """Get PMS dashboard statistics"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        employee = user.employee_get

        # Get objective stats
        my_objectives = EmployeeObjective.objects.filter(employee_id=employee)
        objective_stats = {
            "total": my_objectives.count(),
            "on_track": my_objectives.filter(status="On Track").count(),
            "behind": my_objectives.filter(status="Behind").count(),
            "at_risk": my_objectives.filter(status="At Risk").count(),
            "closed": my_objectives.filter(status="Closed").count(),
            "not_started": my_objectives.filter(status="Not Started").count(),
        }

        # Get feedback stats
        my_feedback = Feedback.objects.filter(
            Q(employee_id=employee)
            | Q(manager_id=employee)
            | Q(colleague_id=employee)
            | Q(subordinate_id=employee)
            | Q(others_id=employee)
        ).distinct()
        feedback_stats = {
            "total": my_feedback.count(),
            "on_track": my_feedback.filter(status="On Track").count(),
            "behind": my_feedback.filter(status="Behind").count(),
            "at_risk": my_feedback.filter(status="At Risk").count(),
            "closed": my_feedback.filter(status="Closed").count(),
            "not_started": my_feedback.filter(status="Not Started").count(),
        }

        # Get meeting stats
        my_meetings = Meetings.objects.filter(
            Q(employee_id=employee) | Q(manager=employee)
        ).distinct()

        # Calculate average progress
        avg_progress = 0
        if my_objectives.exists():
            total_progress = sum(obj.progress_percentage for obj in my_objectives)
            avg_progress = total_progress / my_objectives.count()

        return Response(
            {
                "objectives": objective_stats,
                "feedback": feedback_stats,
                "meetings_count": my_meetings.count(),
                "average_progress": round(avg_progress, 2),
            },
            status=status.HTTP_200_OK,
        )
