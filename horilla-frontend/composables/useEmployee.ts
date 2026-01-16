import { ref, computed } from 'vue';
import { apiClient } from '~/utils/api-client';

export interface EmployeeData {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  profile_image?: string;
  date_of_birth?: string;
  gender?: string;
  address?: string;
  city?: string;
  state?: string;
  country?: string;
  zip_code?: string;
  company?: number;
  [key: string]: any;
}

export interface EmployeeWorkInfo {
  id: number;
  employee_id: number;
  department?: string;
  job_position?: string;
  reporting_manager?: string;
  shift?: string;
  work_type?: string;
  company?: number;
  [key: string]: any;
}

export const useEmployee = () => {
  const employees = ref<EmployeeData[]>([]);
  const currentEmployee = ref<EmployeeData | null>(null);
  const employeeWorkInfo = ref<EmployeeWorkInfo | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const getEmployees = async (page = 1, limit = 10) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await apiClient.get<{
        results: EmployeeData[];
        count: number;
      }>('/employee/list/employees/', {
        params: { page, limit },
      });

      employees.value = response.results;
      return response;
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const getEmployeeById = async (id: number) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await apiClient.get<EmployeeData>(
        `/employee/employees/${id}/`
      );
      currentEmployee.value = response;
      return response;
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const getEmployeeWorkInfo = async (employeeId: number) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await apiClient.get<EmployeeWorkInfo>(
        `/employee/employee-work-information/${employeeId}/`
      );
      employeeWorkInfo.value = response;
      return response;
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const createEmployee = async (data: Partial<EmployeeData>) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await apiClient.post<EmployeeData>(
        '/employee/employees/',
        data
      );
      return response;
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const updateEmployee = async (id: number, data: Partial<EmployeeData>) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await apiClient.put<EmployeeData>(
        `/employee/employees/${id}/`,
        data
      );
      currentEmployee.value = response;
      return response;
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const deleteEmployee = async (id: number) => {
    isLoading.value = true;
    error.value = null;

    try {
      await apiClient.delete(`/employee/employees/${id}/`);
      employees.value = employees.value.filter((emp) => emp.id !== id);
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    // State
    employees,
    currentEmployee,
    employeeWorkInfo,
    isLoading,
    error,

    // Methods
    getEmployees,
    getEmployeeById,
    getEmployeeWorkInfo,
    createEmployee,
    updateEmployee,
    deleteEmployee,
  };
};
