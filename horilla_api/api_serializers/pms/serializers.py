from rest_framework import serializers
from employee.models import Employee
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


# ============ Employee Serializer (Basic) ============
class BasicEmployeeSerializer(serializers.ModelSerializer):
    """Basic employee info for nested serialization"""
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_first_name",
            "employee_last_name",
            "email",
            "phone",
            "profile_image",
        ]

    def get_profile_image(self, obj):
        try:
            return obj.employee_work_info.first().employee_profile.url
        except:
            return None


# ============ Period Serializer ============
class PeriodSerializer(serializers.ModelSerializer):
    """Serializer for Period model"""

    class Meta:
        model = Period
        fields = [
            "id",
            "period_name",
            "start_date",
            "end_date",
            "company_id",
        ]


# ============ KeyResult Serializer ============
class KeyResultSerializer(serializers.ModelSerializer):
    """Serializer for KeyResult model"""

    class Meta:
        model = KeyResult
        fields = [
            "id",
            "title",
            "description",
            "progress_type",
            "target_value",
            "duration",
            "archive",
            "company_id",
        ]


# ============ Objective Serializer ============
class ObjectiveSerializer(serializers.ModelSerializer):
    """Serializer for Objective model"""
    managers = BasicEmployeeSerializer(many=True, read_only=True)
    assignees = BasicEmployeeSerializer(many=True, read_only=True)
    manager_ids = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), many=True, write_only=True, source="managers"
    )
    assignee_ids = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), many=True, write_only=True, source="assignees"
    )
    key_result_ids = serializers.PrimaryKeyRelatedField(
        queryset=KeyResult.objects.all(),
        many=True,
        write_only=True,
        source="key_result_id",
    )

    class Meta:
        model = Objective
        fields = [
            "id",
            "title",
            "description",
            "managers",
            "manager_ids",
            "assignees",
            "assignee_ids",
            "key_result_id",
            "key_result_ids",
            "duration_unit",
            "duration",
            "add_assignees",
            "archive",
            "self_employee_progress_update",
            "company_id",
        ]


# ============ Comment Serializer ============
class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    employee_id = BasicEmployeeSerializer(read_only=True)
    employee_id_write = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), write_only=True, source="employee_id"
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "comment",
            "employee_id",
            "employee_id_write",
            "employee_objective_id",
            "created_at",
        ]


# ============ EmployeeObjective Serializer ============
class EmployeeObjectiveSerializer(serializers.ModelSerializer):
    """Serializer for EmployeeObjective model"""
    objective_id = ObjectiveSerializer(read_only=True)
    employee_id = BasicEmployeeSerializer(read_only=True)
    comments = CommentSerializer(source="emp_objective", many=True, read_only=True)
    progress_percentage = serializers.ReadOnlyField()

    class Meta:
        model = EmployeeObjective
        fields = [
            "id",
            "objective",
            "objective_description",
            "objective_id",
            "employee_id",
            "start_date",
            "end_date",
            "status",
            "progress_percentage",
            "created_at",
            "updated_at",
            "archive",
            "comments",
        ]


# ============ EmployeeKeyResult Serializer ============
class EmployeeKeyResultSerializer(serializers.ModelSerializer):
    """Serializer for EmployeeKeyResult model"""
    key_result_id = KeyResultSerializer(read_only=True)
    employee_objective_id = serializers.StringRelatedField(read_only=True)
    progress_percentage = serializers.ReadOnlyField()

    class Meta:
        model = EmployeeKeyResult
        fields = [
            "id",
            "key_result",
            "key_result_description",
            "key_result_id",
            "employee_objective_id",
            "progress_type",
            "status",
            "start_value",
            "current_value",
            "target_value",
            "start_date",
            "end_date",
            "progress_percentage",
            "created_at",
            "updated_at",
        ]


# ============ QuestionOptions Serializer ============
class QuestionOptionsSerializer(serializers.ModelSerializer):
    """Serializer for QuestionOptions model"""

    class Meta:
        model = QuestionOptions
        fields = ["id", "option_a", "option_b", "option_c", "option_d"]


# ============ Question Serializer ============
class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model"""
    question_options = QuestionOptionsSerializer(read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "question",
            "title",
            "description",
            "points",
            "footer",
            "ordering",
            "question_type",
            "template_id",
            "question_options",
        ]


# ============ QuestionTemplate Serializer ============
class QuestionTemplateSerializer(serializers.ModelSerializer):
    """Serializer for QuestionTemplate model"""
    questions = QuestionSerializer(source="question", many=True, read_only=True)

    class Meta:
        model = QuestionTemplate
        fields = ["id", "question_template", "company_id", "questions"]


# ============ Answer Serializer ============
class AnswerSerializer(serializers.ModelSerializer):
    """Serializer for Answer model"""
    question_id = QuestionSerializer(read_only=True)
    employee_id = BasicEmployeeSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ["id", "answer", "question_id", "employee_id", "feedback_id"]


# ============ Feedback Serializer ============
class FeedbackSerializer(serializers.ModelSerializer):
    """Serializer for Feedback model"""
    manager_id = BasicEmployeeSerializer(read_only=True)
    employee_id = BasicEmployeeSerializer(read_only=True)
    colleague_id = BasicEmployeeSerializer(many=True, read_only=True)
    subordinate_id = BasicEmployeeSerializer(many=True, read_only=True)
    others_id = BasicEmployeeSerializer(many=True, read_only=True)
    question_template_id = QuestionTemplateSerializer(read_only=True)
    answers = AnswerSerializer(source="feedback_answer", many=True, read_only=True)

    # For write operations
    manager_id_write = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        write_only=True,
        required=False,
        source="manager_id",
    )
    employee_id_write = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), write_only=True, source="employee_id"
    )
    colleague_ids = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        many=True,
        write_only=True,
        source="colleague_id",
    )
    subordinate_ids = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        many=True,
        write_only=True,
        source="subordinate_id",
    )
    others_ids = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        many=True,
        write_only=True,
        source="others_id",
    )
    question_template_id_write = serializers.PrimaryKeyRelatedField(
        queryset=QuestionTemplate.objects.all(),
        write_only=True,
        source="question_template_id",
    )

    class Meta:
        model = Feedback
        fields = [
            "id",
            "review_cycle",
            "manager_id",
            "manager_id_write",
            "employee_id",
            "employee_id_write",
            "colleague_id",
            "colleague_ids",
            "subordinate_id",
            "subordinate_ids",
            "others_id",
            "others_ids",
            "question_template_id",
            "question_template_id_write",
            "status",
            "archive",
            "start_date",
            "end_date",
            "employee_key_results_id",
            "cyclic_feedback",
            "cyclic_feedback_days_count",
            "cyclic_feedback_period",
            "answers",
        ]


# ============ AnonymousFeedback Serializer ============
class AnonymousFeedbackSerializer(serializers.ModelSerializer):
    """Serializer for AnonymousFeedback model"""
    employee_id = BasicEmployeeSerializer(read_only=True)
    employee_id_write = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        write_only=True,
        required=False,
        source="employee_id",
    )

    class Meta:
        model = AnonymousFeedback
        fields = [
            "id",
            "feedback_subject",
            "based_on",
            "employee_id",
            "employee_id_write",
            "department_id",
            "job_position_id",
            "status",
            "created_at",
            "archive",
            "anonymous_feedback_id",
            "feedback_description",
        ]


# ============ MeetingsAnswer Serializer ============
class MeetingsAnswerSerializer(serializers.ModelSerializer):
    """Serializer for MeetingsAnswer model"""
    question_id = QuestionSerializer(read_only=True)
    employee_id = BasicEmployeeSerializer(read_only=True)

    class Meta:
        model = MeetingsAnswer
        fields = ["id", "answer", "question_id", "employee_id", "meeting_id"]


# ============ Meetings Serializer ============
class MeetingsSerializer(serializers.ModelSerializer):
    """Serializer for Meetings model"""
    employee_id = BasicEmployeeSerializer(many=True, read_only=True)
    manager = BasicEmployeeSerializer(many=True, read_only=True)
    answer_employees = BasicEmployeeSerializer(many=True, read_only=True)
    question_template = QuestionTemplateSerializer(read_only=True)
    answers = MeetingsAnswerSerializer(source="meeting_answer", many=True, read_only=True)

    # For write operations
    employee_ids = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), many=True, write_only=True, source="employee_id"
    )
    manager_ids = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), many=True, write_only=True, source="manager"
    )
    answer_employee_ids = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source="answer_employees",
    )
    question_template_write = serializers.PrimaryKeyRelatedField(
        queryset=QuestionTemplate.objects.all(),
        write_only=True,
        required=False,
        source="question_template",
    )

    class Meta:
        model = Meetings
        fields = [
            "id",
            "title",
            "date",
            "employee_id",
            "employee_ids",
            "manager",
            "manager_ids",
            "answer_employees",
            "answer_employee_ids",
            "question_template",
            "question_template_write",
            "response",
            "show_response",
            "company_id",
            "answers",
        ]


# ============ BonusPointSetting Serializer ============
class BonusPointSettingSerializer(serializers.ModelSerializer):
    """Serializer for BonusPointSetting model"""

    class Meta:
        model = BonusPointSetting
        fields = [
            "id",
            "model",
            "applicable_for",
            "bonus_for",
            "field_1",
            "conditions",
            "field_2",
            "points",
            "is_active",
        ]


# ============ EmployeeBonusPoint Serializer ============
class EmployeeBonusPointSerializer(serializers.ModelSerializer):
    """Serializer for EmployeeBonusPoint model"""
    employee_id = BasicEmployeeSerializer(read_only=True)

    class Meta:
        model = EmployeeBonusPoint
        fields = [
            "id",
            "employee_id",
            "bonus_point",
            "instance",
            "based_on",
            "bonus_point_id",
        ]


# ============ KeyResultFeedback Serializer ============
class KeyResultFeedbackSerializer(serializers.ModelSerializer):
    """Serializer for KeyResultFeedback model"""
    employee_id = BasicEmployeeSerializer(read_only=True)
    key_result_id = EmployeeKeyResultSerializer(read_only=True)

    class Meta:
        model = KeyResultFeedback
        fields = ["id", "feedback_id", "employee_id", "answer", "key_result_id"]
