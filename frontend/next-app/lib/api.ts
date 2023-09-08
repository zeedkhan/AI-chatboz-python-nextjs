"use client"

import { useEffect, useState } from 'react';
import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';

interface ApiResponse {
  data: any;
  error: string | null;
}

interface ApiHook {
  data: any;
  error: string | null;
  isLoading: boolean;
  fetch: (method: HttpMethod, endpoint: string, data?: {}) => Promise<void>;
}

const useApi = (): ApiHook => {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [token, setToken] = useState<string | null>(null);

  const baseUrl = "http://backend:8000"; // Set your base URL here

  const getToken = async () => {
    try {
      const headers = {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      };
      const response = await axios.get(`${baseUrl}/token/`, {
        headers,
        withCredentials: true,
      });

      if (!response.data) {
        throw new Error('Unauthorized');
      }

      setToken(response.data.access_token);
    } catch (error) {
      setError('Error fetching token');
    }
  };

  const request = async (method: HttpMethod, endpoint: string, requestData?: {}): Promise<ApiResponse> => {
    if (!token) {
      await getToken();
    }

    const headers = {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    };

    const config: AxiosRequestConfig = {
      method,
      headers,
      withCredentials: true,
      data: requestData,
    };

    try {
      const response: AxiosResponse = await axios(`${baseUrl}${endpoint}`, config);
      return {
        data: response.data,
        error: null,
      };
    } catch (error) {
      return { data: null, error: 'An error occurred while making the request' };
    }
  };

  const fetch = async (method: HttpMethod, endpoint: string, data?: {}): Promise<void> => {
    setIsLoading(true);
    const response = await request(method, endpoint, data);
    setData(response.data);
    setError(response.error);
    setIsLoading(false);
  };

  return {
    data,
    error,
    isLoading,
    fetch,
  };
};

export default useApi;
