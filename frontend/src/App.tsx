import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ChakraProvider, extendTheme, Box, Spinner } from '@chakra-ui/react'; // Import ChakraProvider and extendTheme
import { AuthProvider, useAuth } from './contexts/AuthContext';

// Components
import Navbar from './components/Navbar';

// Pages
import Login from './pages/Login';
import Register from './pages/Register';
import Onboarding from './pages/Onboarding';
import Dashboard from './pages/Dashboard';
import Groups from './pages/Groups';
import GroupDetail from './pages/GroupDetail';

// Create Chakra theme (optional customization)
const theme = extendTheme({
  colors: {
    primary: {
      50: '#e3f2fd',
      100: '#bbdefb',
      200: '#90caf9',
      300: '#64b5f6',
      400: '#42a5f5',
      500: '#2196f3', // Primary blue from MUI example
      600: '#1e88e5',
      700: '#1976d2',
      800: '#1565c0',
      900: '#0d47a1',
    },
    secondary: {
      50: '#fff3e0',
      100: '#ffe0b2',
      200: '#ffcc80',
      300: '#ffb74d',
      400: '#ffa726',
      500: '#ff9800', // Secondary orange
      600: '#fb8c00',
      700: '#f57c00',
      800: '#ef6c00',
      900: '#e65100',
    },
  },
  components: {
    Button: {
      baseStyle: {
        borderRadius: 'md', // Corresponds to 8px in MUI example
        _focus: { boxShadow: 'outline' },
      },
    },
    Card: { // Recreating a basic Card style
      baseStyle: {
        borderRadius: 'lg', // Corresponds to 12px
        boxShadow: 'md',
        bg: 'white',
      },
    },
    Input: {
      defaultProps: {
        focusBorderColor: 'primary.500',
      },
    },
    Link: {
      baseStyle: {
        color: 'primary.600',
        _hover: { textDecoration: 'underline' },
      },
    },
    Container: {
      baseStyle: {
        maxW: 'container.lg',
      },
    }
  },
});

// Protected route component
interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    // Basic loading state with Chakra Spinner
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
        <Spinner size="xl" />
      </Box>
    );
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  return <>{children}</>;
};

const AppRoutes: React.FC = () => {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      
      {/* Protected routes */}
      <Route path="/onboarding" element={
        <ProtectedRoute>
          <Onboarding />
        </ProtectedRoute>
      } />
      
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <Dashboard />
        </ProtectedRoute>
      } />
      
      <Route path="/groups" element={
        <ProtectedRoute>
          <Groups />
        </ProtectedRoute>
      } />
      
      <Route path="/groups/:groupId" element={
        <ProtectedRoute>
          <GroupDetail />
        </ProtectedRoute>
      } />
      
      {/* Redirect root to dashboard if authenticated, otherwise to login */}
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      
      {/* Catch all route */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

const App: React.FC = () => {
  return (
    <ChakraProvider theme={theme}>
      <Router>
        <AuthProvider>
          <Navbar />
          <AppRoutes />
        </AuthProvider>
      </Router>
    </ChakraProvider>
  );
};

export default App; 