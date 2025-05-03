import React, { useState } from 'react';
import {
  Container,
  Box,
  Heading,
  Text,
  Input,
  Button,
  Link as ChakraLink,
  FormControl,
  FormLabel,
  FormErrorMessage,
  Spinner,
  Alert,
  AlertIcon,
  VStack,
  Center,
} from '@chakra-ui/react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { UserCreate } from '../types';

const Register: React.FC = () => {
  const { register, loading, error } = useAuth();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState<UserCreate & { confirmPassword: string }>({
    email: '',
    username: '',
    password: '',
    confirmPassword: ''
  });
  
  const [formErrors, setFormErrors] = useState({
    email: '',
    username: '',
    password: '',
    confirmPassword: ''
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const validateForm = (): boolean => {
    let valid = true;
    const errors = {
      email: '',
      username: '',
      password: '',
      confirmPassword: ''
    };

    // Email validation
    if (!formData.email) {
      errors.email = 'Email is required';
      valid = false;
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'Email is invalid';
      valid = false;
    }

    // Username validation
    if (!formData.username) {
      errors.username = 'Username is required';
      valid = false;
    } else if (formData.username.length < 3) {
      errors.username = 'Username must be at least 3 characters';
      valid = false;
    }

    // Password validation
    if (!formData.password) {
      errors.password = 'Password is required';
      valid = false;
    } else if (formData.password.length < 6) {
      errors.password = 'Password must be at least 6 characters';
      valid = false;
    }

    // Confirm password validation
    if (formData.password !== formData.confirmPassword) {
      errors.confirmPassword = 'Passwords do not match';
      valid = false;
    }

    setFormErrors(errors);
    return valid;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (validateForm()) {
      const { confirmPassword, ...userData } = formData;
      try {
        await register(userData);
        navigate('/onboarding');
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
              Create an Account
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
                    name="email"
                    type="email"
                    placeholder="Enter your email"
                    value={formData.email}
                    onChange={handleInputChange}
                  />
                  <FormErrorMessage>{formErrors.email}</FormErrorMessage>
                </FormControl>

                <FormControl isInvalid={!!formErrors.username} isDisabled={loading}>
                  <FormLabel htmlFor="username">Username</FormLabel>
                  <Input
                    id="username"
                    name="username"
                    placeholder="Choose a username"
                    value={formData.username}
                    onChange={handleInputChange}
                  />
                  <FormErrorMessage>{formErrors.username}</FormErrorMessage>
                </FormControl>

                <FormControl isInvalid={!!formErrors.password} isDisabled={loading}>
                  <FormLabel htmlFor="password">Password</FormLabel>
                  <Input
                    id="password"
                    name="password"
                    type="password"
                    placeholder="Create a password (min. 6 characters)"
                    value={formData.password}
                    onChange={handleInputChange}
                  />
                  <FormErrorMessage>{formErrors.password}</FormErrorMessage>
                </FormControl>

                <FormControl isInvalid={!!formErrors.confirmPassword} isDisabled={loading}>
                  <FormLabel htmlFor="confirmPassword">Confirm Password</FormLabel>
                  <Input
                    id="confirmPassword"
                    name="confirmPassword"
                    type="password"
                    placeholder="Confirm your password"
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                  />
                  <FormErrorMessage>{formErrors.confirmPassword}</FormErrorMessage>
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
                  Sign Up
                </Button>
                
                <Text textAlign="center" pt={2}>
                  <ChakraLink as={RouterLink} to="/login" color="primary.600">
                    {"Already have an account? Sign In"}
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

export default Register; 