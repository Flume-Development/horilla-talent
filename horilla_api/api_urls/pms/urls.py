from django.urls import path
from horilla_api.api_views.pms.views import (
    # Period
    PeriodListAPIView,
    PeriodAPIView,
    # KeyResult
    KeyResultListAPIView,
    KeyResultAPIView,
    # Objective
    ObjectiveListAPIView,
    ObjectiveAPIView,
    ObjectiveArchiveAPIView,
    # Employee Objective
    EmployeeObjectiveListAPIView,
    EmployeeObjectiveAPIView,
    EmployeeObjectiveStatusUpdateAPIView,
    # Employee Key Result
    EmployeeKeyResultListAPIView,
    EmployeeKeyResultAPIView,
    EmployeeKeyResultProgressUpdateAPIView,
    # Comment
    CommentListAPIView,
    CommentAPIView,
    # QuestionTemplate
    QuestionTemplateListAPIView,
    QuestionTemplateAPIView,
    # Question
    QuestionListAPIView,
    QuestionAPIView,
    # Feedback
    FeedbackListAPIView,
    FeedbackAPIView,
    FeedbackArchiveAPIView,
    FeedbackAnswerSubmitAPIView,
    FeedbackAnswersViewAPIView,
    # Meetings
    MeetingsListAPIView,
    MeetingsAPIView,
    MeetingAnswersViewAPIView,
    MeetingAnswerSubmitAPIView,
    # Anonymous Feedback
    AnonymousFeedbackListAPIView,
    AnonymousFeedbackAPIView,
    # Bonus Points
    BonusPointSettingListAPIView,
    BonusPointSettingAPIView,
    EmployeeBonusPointListAPIView,
    EmployeeBonusPointAPIView,
    # Dashboard
    DashboardStatsAPIView,
)

urlpatterns = [
    # Period endpoints
    path("periods/", PeriodListAPIView.as_view(), name="period-list"),
    path("periods/<int:pk>/", PeriodAPIView.as_view(), name="period-detail"),
    # KeyResult endpoints
    path("key-results/", KeyResultListAPIView.as_view(), name="key-result-list"),
    path("key-results/<int:pk>/", KeyResultAPIView.as_view(), name="key-result-detail"),
    # Objective endpoints
    path("objectives/", ObjectiveListAPIView.as_view(), name="objective-list"),
    path("objectives/<int:pk>/", ObjectiveAPIView.as_view(), name="objective-detail"),
    path(
        "objectives/<int:pk>/archive/",
        ObjectiveArchiveAPIView.as_view(),
        name="objective-archive",
    ),
    # Employee Objective endpoints
    path(
        "employee-objectives/",
        EmployeeObjectiveListAPIView.as_view(),
        name="employee-objective-list",
    ),
    path(
        "employee-objectives/<int:pk>/",
        EmployeeObjectiveAPIView.as_view(),
        name="employee-objective-detail",
    ),
    path(
        "employee-objectives/<int:pk>/status/",
        EmployeeObjectiveStatusUpdateAPIView.as_view(),
        name="employee-objective-status-update",
    ),
    # Employee Key Result endpoints
    path(
        "employee-key-results/",
        EmployeeKeyResultListAPIView.as_view(),
        name="employee-key-result-list",
    ),
    path(
        "employee-key-results/<int:pk>/",
        EmployeeKeyResultAPIView.as_view(),
        name="employee-key-result-detail",
    ),
    path(
        "employee-key-results/<int:pk>/progress/",
        EmployeeKeyResultProgressUpdateAPIView.as_view(),
        name="employee-key-result-progress-update",
    ),
    # Comment endpoints
    path("comments/", CommentListAPIView.as_view(), name="comment-list"),
    path("comments/<int:pk>/", CommentAPIView.as_view(), name="comment-delete"),
    # QuestionTemplate endpoints
    path(
        "question-templates/",
        QuestionTemplateListAPIView.as_view(),
        name="question-template-list",
    ),
    path(
        "question-templates/<int:pk>/",
        QuestionTemplateAPIView.as_view(),
        name="question-template-detail",
    ),
    # Question endpoints
    path("questions/", QuestionListAPIView.as_view(), name="question-list"),
    path("questions/<int:pk>/", QuestionAPIView.as_view(), name="question-detail"),
    # Feedback endpoints
    path("feedback/", FeedbackListAPIView.as_view(), name="feedback-list"),
    path("feedback/<int:pk>/", FeedbackAPIView.as_view(), name="feedback-detail"),
    path(
        "feedback/<int:pk>/archive/",
        FeedbackArchiveAPIView.as_view(),
        name="feedback-archive",
    ),
    path(
        "feedback/<int:pk>/submit-answers/",
        FeedbackAnswerSubmitAPIView.as_view(),
        name="feedback-submit-answers",
    ),
    path(
        "feedback/<int:pk>/answers/",
        FeedbackAnswersViewAPIView.as_view(),
        name="feedback-answers-view",
    ),
    # Meetings endpoints
    path("meetings/", MeetingsListAPIView.as_view(), name="meetings-list"),
    path("meetings/<int:pk>/", MeetingsAPIView.as_view(), name="meetings-detail"),
    path(
        "meetings/<int:pk>/answers/",
        MeetingAnswersViewAPIView.as_view(),
        name="meeting-answers-view",
    ),
    path(
        "meetings/<int:pk>/submit-answers/",
        MeetingAnswerSubmitAPIView.as_view(),
        name="meeting-submit-answers",
    ),
    # Anonymous Feedback endpoints
    path(
        "anonymous-feedback/",
        AnonymousFeedbackListAPIView.as_view(),
        name="anonymous-feedback-list",
    ),
    path(
        "anonymous-feedback/<int:pk>/",
        AnonymousFeedbackAPIView.as_view(),
        name="anonymous-feedback-detail",
    ),
    # Bonus Point Settings endpoints
    path(
        "bonus-settings/",
        BonusPointSettingListAPIView.as_view(),
        name="bonus-setting-list",
    ),
    path(
        "bonus-settings/<int:pk>/",
        BonusPointSettingAPIView.as_view(),
        name="bonus-setting-detail",
    ),
    # Employee Bonus Points endpoints
    path(
        "employee-bonus-points/",
        EmployeeBonusPointListAPIView.as_view(),
        name="employee-bonus-point-list",
    ),
    path(
        "employee-bonus-points/<int:pk>/",
        EmployeeBonusPointAPIView.as_view(),
        name="employee-bonus-point-detail",
    ),
    # Dashboard endpoints
    path(
        "dashboard/stats/",
        DashboardStatsAPIView.as_view(),
        name="dashboard-stats",
    ),
]
