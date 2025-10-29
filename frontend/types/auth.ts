
export interface User {
  email: string;
  token: string;
  username?:string
}

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  registerUser: (username: string, email: string, password: string) => Promise<void>;
  loading: boolean
}