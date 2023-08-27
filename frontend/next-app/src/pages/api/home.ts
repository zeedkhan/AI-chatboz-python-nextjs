import type { NextApiRequest, NextApiResponse } from 'next'

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const token = fetch(`http://localhost:8000/token`)
    .then(response => response.json())
    .then(data => {
      const authToken = data.token; // Assuming your response structure has a 'token' field
      // Use the authToken in your subsequent requests
      
      return authToken
    })
    .catch(error => {
      console.error('Error fetching token:', error);
    });

    return token
}