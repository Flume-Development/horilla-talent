// ============ Employee Type ============
export interface BasicEmployee {
  id: number
  employee_first_name: string
  employee_last_name: string
  email: string
  phone?: string
  profile_image?: string
}

// ============ Period Type ============
export interface Period {
  id: number
  period_name: string
  start_date: string
  end_date: string
  company_id?: number[]
}

// ============ Key Result Type ============
export interface KeyResult {
  id: number
  title: string
  description: string
  progress_type: 'percentage' | 'number' | 'currency'
  target_value?: number
  duration?: number
  archive: boolean
  company_id?: number
}

// ============ Objective Type ============
export interface Objective {
  id: number
  title: string
  description: string
  managers: BasicEmployee[]
  assignees: BasicEmployee[]
  key_result_id: KeyResult[]
  duration_unit: 'days' | 'months' | 'years'
  duration: number
  add_assignees: boolean
  archive: boolean
  self_employee_progress_update: boolean
  company_id?: number
}

// ============ Employee Objective Type ============
export interface EmployeeObjective {
  id: number
  objective: string
  objective_description?: string
  objective_id: Objective
  employee_id: BasicEmployee
  start_date: string
  end_date: string
  status: ObjectiveStatus
  progress_percentage: number
  created_at: string
  updated_at: string
  archive: boolean
  comments?: Comment[]
}

export type ObjectiveStatus = 'On Track' | 'Behind' | 'At Risk' | 'Closed' | 'Not Started'

// ============ Employee Key Result Type ============
export interface EmployeeKeyResult {
  id: number
  key_result: string
  key_result_description?: string
  key_result_id: KeyResult
  employee_objective_id: EmployeeObjective
  progress_type: string
  status: ObjectiveStatus
  start_value: number
  current_value: number
  target_value: number
  start_date?: string
  end_date?: string
  progress_percentage: number
  created_at: string
  updated_at: string
}

// ============ Comment Type ============
export interface Comment {
  id: number
  comment: string
  employee_id: BasicEmployee
  employee_objective_id: number
  created_at: string
}

// ============ Question Types ============
export type QuestionType = '1' | '2' | '3' | '4' | '5'
// 1: Text, 2: Rating, 3: Boolean, 4: Multi-choices, 5: Likert

export interface QuestionOptions {
  id: number
  option_a?: string
  option_b?: string
  option_c?: string
  option_d?: string
}

export interface Question {
  id: number
  question: string
  title?: string
  description?: string
  points?: string
  footer?: string
  ordering: number
  question_type: QuestionType
  template_id: number
  question_options?: QuestionOptions
}

export interface QuestionTemplate {
  id: number
  question_template: string
  company_id?: number[]
  questions?: Question[]
}

// ============ Answer Type ============
export interface Answer {
  id: number
  answer: any
  question_id: Question
  employee_id: BasicEmployee
  feedback_id: number
}

// ============ Feedback Type ============
export interface Feedback {
  id: number
  review_cycle: string
  manager_id?: BasicEmployee
  employee_id: BasicEmployee
  colleague_id: BasicEmployee[]
  subordinate_id: BasicEmployee[]
  others_id: BasicEmployee[]
  question_template_id: QuestionTemplate
  status: ObjectiveStatus
  archive: boolean
  start_date: string
  end_date: string
  employee_key_results_id?: number[]
  cyclic_feedback: boolean
  cyclic_feedback_days_count?: number
  cyclic_feedback_period?: 'days' | 'months' | 'years'
  answers?: Answer[]
}

// ============ Anonymous Feedback Type ============
export interface AnonymousFeedback {
  id: number
  feedback_subject: string
  based_on: 'general' | 'employee' | 'department' | 'job_position'
  employee_id?: BasicEmployee
  department_id?: number
  job_position_id?: number
  status: ObjectiveStatus
  created_at: string
  archive: boolean
  anonymous_feedback_id: string
  feedback_description?: string
}

// ============ Meetings Types ============
export interface MeetingsAnswer {
  id: number
  answer: any
  question_id: Question
  employee_id: BasicEmployee
  meeting_id: number
}

export interface Meetings {
  id: number
  title: string
  date?: string
  employee_id: BasicEmployee[]
  manager: BasicEmployee[]
  answer_employees: BasicEmployee[]
  question_template?: QuestionTemplate
  response?: string
  show_response: boolean
  company_id?: number
  answers?: MeetingsAnswer[]
}

// ============ Bonus Points Types ============
export interface BonusPointSetting {
  id: number
  model: string
  applicable_for?: 'owner' | 'members' | 'managers'
  bonus_for: 'completed' | 'Closed'
  field_1?: string
  conditions?: '=' | '>' | '<' | '<=' | '>='
  field_2?: string
  points: number
  is_active: boolean
}

export interface EmployeeBonusPoint {
  id: number
  employee_id: BasicEmployee
  bonus_point: number
  instance?: string
  based_on: string
  bonus_point_id?: number
}

// ============ Dashboard Types ============
export interface DashboardStats {
  objectives: {
    total: number
    on_track: number
    behind: number
    at_risk: number
    closed: number
    not_started: number
  }
  feedback: {
    total: number
    on_track: number
    behind: number
    at_risk: number
    closed: number
    not_started: number
  }
  meetings_count: number
  average_progress: number
}
