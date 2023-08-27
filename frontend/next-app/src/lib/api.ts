// api.ts

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE'; // Add other methods as needed

interface ApiResponse {
  data: any;
  error: string | null;
}

class Api {
  private token: string | null = null;
  private baseUrl: string;

  constructor() {
    this.baseUrl = "http://localhost:8000"; // Set your base URL here
    this.getToken();
  }

  private async getToken() {
    try {
      const response = await fetch(`${this.baseUrl}/token/`, {
        mode: 'cors',
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error('Unauthorized');
      }

      const data = await response.json();
      this.token = data.access_token;
      console.log(data.access_token)
    } catch (error) {
      console.error('Error fetching token:', error);
    }
  }

  private async request(method: HttpMethod, endpoint: string, data?: any): Promise<ApiResponse> {
    if (!this.token) {
      return {
        data: null,
        error: "Unauthorized"
      }
    }

    const headers = {
      'Authorization': `Bearer ${this.token}`,
      'Content-Type': 'application/json'
    };
    
    const config: RequestInit = {
      method,
      headers,
      mode: 'cors',
      credentials: 'include'
    };

    if (data) {
      config.body = JSON.stringify(data);
    }

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, config);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const responseData = await response.json();
      return responseData;
    } catch (error) {
      console.error('Error making API request:', error);
      return { data: null, error: 'An error occurred while making the request' };
    }
  }

  async get(endpoint: string): Promise<ApiResponse> {
    return this.request('GET', endpoint);
  }

  async post(endpoint: string, data: any): Promise<ApiResponse> {
    return this.request('POST', endpoint, data);
  }

  async get_user(): Promise<ApiResponse> {
    return this.request('GET', '/user/');
  }

  async logout(): Promise<ApiResponse> {
    return this.request("GET", '/logout/')
  }

  // Add other methods like put() and delete() as needed
}

const API = new Api();
export default API;
