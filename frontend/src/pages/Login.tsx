import React, { useState } from 'react';
import {
  Container,
  Box,
  Heading,
  Text,
  Input,
  Button,
  Link as ChakraLink, // Alias ChakraLink to avoid conflict with RouterLink
  FormControl,
  FormLabel,
  FormErrorMessage,
  Spinner,
  Alert,
  AlertIcon,
  VStack, // Vertical stack for layout
  Center,
} from '@chakra-ui/react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Login: React.FC = () => {
  const { login, loading, error } = useAuth();
  const navigate = useNavigate();
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [formErrors, setFormErrors] = useState({
    email: '',
    password: ''
  });

  const validateForm = (): boolean => {
    let valid = true;
    const errors = {
      email: '',
      password: ''
    };

    // Email validation
    if (!email) {
      errors.email = 'Email is required';
      valid = false;
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      errors.email = 'Email is invalid';
      valid = false;
    }

    // Password validation
    if (!password) {
      errors.password = 'Password is required';
      valid = false;
    }

    setFormErrors(errors);
    return valid;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (validateForm()) {
      try {
        await login(email, password);
        navigate('/dashboard');
      } catch (err) {
        // Error is handled in the auth context
      }
    }
  };

  return (
    <Container maxW="sm">
      <Center minH="calc(100vh - 80px)"> {/* Center content vertically */} 
        <VStack spacing={6} w="100%">
          <Heading as="h1" size="xl" color="primary.600">
            The Perfect Reunion
          </Heading>
          
          <Box 
            p={8} 
            borderWidth={1} 
            borderRadius="lg" 
            boxShadow="lg" 
            w="100%"
            bg="white"
          >
            <Heading as="h2" size="lg" mb={6} textAlign="center">
              Sign In
            </Heading>
            
            {error && (
              <Alert status="error" mb={4} borderRadius="md">
                <AlertIcon />
                {error}
              </Alert>
            )}
            
            <Box as="form" onSubmit={handleSubmit}>
              <VStack spacing={4}>
                <FormControl isInvalid={!!formErrors.email} isDisabled={loading}>
                  <FormLabel htmlFor="email">Email Address</FormLabel>
                  <Input
                    id="email"
                    type="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    autoFocus
                  />
                  <FormErrorMessage>{formErrors.email}</FormErrorMessage>
                </FormControl>

                <FormControl isInvalid={!!formErrors.password} isDisabled={loading}>
                  <FormLabel htmlFor="password">Password</FormLabel>
                  <Input
                    id="password"
                    type="password"
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                  <FormErrorMessage>{formErrors.password}</FormErrorMessage>
                </FormControl>

                <Button
                  type="submit"
                  colorScheme="primary"
                  width="full"
                  mt={4}
                  py={6} // Increase button height
                  isLoading={loading}
                  spinner={<Spinner size="sm" />}
                >
                  Sign In
                </Button>
                
                <Text textAlign="center" pt={2}>
                  <ChakraLink as={RouterLink} to="/register" color="primary.600">
                    {"Don't have an account? Sign Up"}
                  </ChakraLink>
                </Text>
              </VStack>
            </Box>
          </Box>
        </VStack>
      </Center>
    </Container>
  );
};

export default Login; 