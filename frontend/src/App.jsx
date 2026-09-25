import { Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import AnalysePage from "./pages/AnalysePage";
import ResultPage from "./pages/ResultPage";
import HistoryPage from "./pages/HistoryPage";
import AboutPage from "./pages/AboutPage";

function RootRedirect() {
  const { isAuthenticated } = useAuth();
  return <Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />;
}

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<RootRedirect />} />
        <Route path="/login" element={<LoginPage />} />

        {/* About is reachable without signing in, matching the original build */}
        <Route element={<Layout />}>
          <Route path="/about" element={<AboutPage />} />
        </Route>

        <Route element={<ProtectedRoute />}>
          <Route element={<Layout />}>
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/analyse" element={<AnalysePage />} />
            <Route path="/result/:predictionId" element={<ResultPage />} />
            <Route path="/history" element={<HistoryPage />} />
          </Route>
        </Route>
      </Routes>
    </AuthProvider>
  );
}
