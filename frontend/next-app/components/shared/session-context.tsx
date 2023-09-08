// apiContext.tsx
import React, { createContext, useContext } from "react";
import ApiV3 from "@/lib/api-v3";

const ApiContext = createContext<ApiV3 | undefined>(undefined);

interface ApiProviderProps {
  api: ApiV3;
  children: React.ReactNode; // Define the children prop
}

export const ApiProvider: React.FC<ApiProviderProps> = ({ api, children }) => {
  return <ApiContext.Provider value={api}>{children}</ApiContext.Provider>;
};

export const useApi = () => {
  const api = useContext(ApiContext);
  if (!api) {
    throw new Error("useApi must be used within an ApiProvider");
  }
  return api;
};

