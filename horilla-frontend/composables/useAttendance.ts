import { ref } from 'vue';
import { apiClient } from '~/utils/api-client';

export interface ClockActivity {
  id: number;
  employee_id: number;
  clock_in_time?: string;
  clock_out_time?: string;
  date: string;
  [key: string]: any;
}

export interface AttendanceRecord {
  id: number;
  employee_id: number;
  date: string;
  status: 'present' | 'absent' | 'half_day' | 'late';
  clock_in_time?: string;
  clock_out_time?: string;
  [key: string]: any;
}

export interface AttendanceRequest {
  id: number;
  employee_id: number;
  request_type: string;
  from_date: string;
  to_date: string;
  status: 'pending' | 'approved' | 'rejected';
  [key: string]: any;
}

export const useAttendance = () => {
  const attendance = ref<AttendanceRecord[]>([]);
  const currentAttendance = ref<AttendanceRecord | null>(null);
  const attendanceRequests = ref<AttendanceRequest[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const clockIn = async () => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await apiClient.post<ClockActivity>(
        '/attendance/clock-in/'
      );
      return response;
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const clockOut = async () => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await apiClient.post<ClockActivity>(
        '/attendance/clock-out/'
      );
      return response;
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const getAttendance = async (page = 1, limit = 10) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await apiClient.get<{
        results: AttendanceRecord[];
        count: number;
      }>('/attendance/attendance/', {
        params: { page, limit },
      });

      attendance.value = response.results;
      return response;
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const getMyAttendance = async () => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await apiClient.get<AttendanceRecord[]>(
        '/attendance/my-attendance/'
      );
      attendance.value = Array.isArray(response) ? response : [response];
      return response;
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const getTodayAttendance = async () => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await apiClient.get<AttendanceRecord[]>(
        '/attendance/today-attendance/'
      );
      return response;
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const submitAttendanceRequest = async (data: Partial<AttendanceRequest>) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await apiClient.post<AttendanceRequest>(
        '/attendance/attendance-request/',
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

  const getAttendanceRequests = async (page = 1, limit = 10) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await apiClient.get<{
        results: AttendanceRequest[];
        count: number;
      }>('/attendance/attendance-request/', {
        params: { page, limit },
      });

      attendanceRequests.value = response.results;
      return response;
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const approveAttendanceRequest = async (id: number) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await apiClient.post<AttendanceRequest>(
        `/attendance/attendance-request-approve/${id}/`
      );
      return response;
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    // State
    attendance,
    currentAttendance,
    attendanceRequests,
    isLoading,
    error,

    // Methods
    clockIn,
    clockOut,
    getAttendance,
    getMyAttendance,
    getTodayAttendance,
    submitAttendanceRequest,
    getAttendanceRequests,
    approveAttendanceRequest,
  };
};
