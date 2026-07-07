import { authMode } from "./config";
import type { AuthProvider, AuthUser } from "./types";
const STORAGE_KEY = "internbase.auth.user";
class MockAuthProvider implements AuthProvider {
  getSession(): AuthUser | null {
    if (typeof window === "undefined") return null;
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? (JSON.parse(raw) as AuthUser) : null;
  }
  async signIn(): Promise<AuthUser> {
    const user: AuthUser = { id: 1, email: "dev@internbase.local" };
    if (typeof window !== "undefined") {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(user));
    }
    return user;
  }
  async signOut(): Promise<void> {
    if (typeof window !== "undefined") {
      localStorage.removeItem(STORAGE_KEY);
    }
  }
}
class CognitoAuthProvider implements AuthProvider {
  getSession(): AuthUser | null {
    throw new Error("Cognito provider not implemented yet.");
  }
  async signIn(): Promise<AuthUser> {
    throw new Error("Cognito provider not implemented yet.");
  }
  async signOut(): Promise<void> {
    throw new Error("Cognito provider not implemented yet.");
  }
}
export function getAuthProvider(): AuthProvider {
  return authMode === "cognito"
    ? new CognitoAuthProvider()
    : new MockAuthProvider();
}