import { ref, computed } from 'vue';
import { apiClient } from '~/utils/api-client';

export interface ApiOptions {
  immediate?: boolean;
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  params?: Record<string, any>;
  data?: Record<string, any>;
}

export interface ApiState<T> {
  data: T | null;
  isLoading: boolean;
  error: string | null;
  isError: boolean;
}

export const useApi = <T = any>(
  url: string,
  options: ApiOptions = {}
) => {
  const {
    immediate = true,
    method = 'GET',
    params = {},
    data = {},
  } = options;

  const state = ref<ApiState<T>>({
    data: null,
    isLoading: false,
    error: null,
    isError: false,
  });

  const isLoading = computed(() => state.value.isLoading);
  const error = computed(() => state.value.error);
  const isError = computed(() => state.value.isError);
  const data = computed(() => state.value.data);

  const execute = async (apiOptions?: ApiOptions) => {
    const mergedOptions = { ...options, ...apiOptions };
    state.value.isLoading = true;
    state.value.error = null;
    state.value.isError = false;

    try {
      let response;

      switch (mergedOptions.method?.toUpperCase()) {
        case 'POST':
          response = await apiClient.post<T>(url, mergedOptions.data, {
            params: mergedOptions.params,
          });
          break;
        case 'PUT':
          response = await apiClient.put<T>(url, mergedOptions.data, {
            params: mergedOptions.params,
          });
          break;
        case 'PATCH':
          response = await apiClient.patch<T>(url, mergedOptions.data, {
            params: mergedOptions.params,
          });
          break;
        case 'DELETE':
          response = await apiClient.delete<T>(url, {
            params: mergedOptions.params,
          });
          break;
        default:
          response = await apiClient.get<T>(url, {
            params: mergedOptions.params,
          });
      }

      state.value.data = response;
      return response;
    } catch (err: any) {
      state.value.error = err.message || 'An error occurred';
      state.value.isError = true;
      throw err;
    } finally {
      state.value.isLoading = false;
    }
  };

  // Execute immediately if option is set
  if (immediate) {
    execute();
  }

  return {
    data,
    isLoading,
    error,
    isError,
    execute,
  };
};
