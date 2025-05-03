import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Heading,
  Text,
  Progress,
  Button,
  Spinner,
  Alert,
  AlertIcon,
  VStack,
  Center,
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import SwipeableCity from '../components/SwipeableCity';
import { City, Vote } from '../types';
import { getCitiesForEvaluation, voteCity } from '../services/api';

const MIN_CITIES_TO_EVALUATE = 5;

const Onboarding: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  
  const [cities, setCities] = useState<City[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [evaluatedCount, setEvaluatedCount] = useState(0);
  const [votingComplete, setVotingComplete] = useState(false);

  useEffect(() => {
    // Redirect if not authenticated
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    const fetchCities = async () => {
      try {
        setLoading(true);
        const data = await getCitiesForEvaluation(MIN_CITIES_TO_EVALUATE);
        setCities(data);
      } catch (err: any) {
        setError('Failed to load cities. Please try again.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchCities();
  }, [isAuthenticated, navigate]);

  const handleSwipe = async (liked: boolean) => {
    if (currentIndex >= cities.length) return;

    const currentCity = cities[currentIndex];
    
    try {
      // Send vote to API
      const voteValue: Vote = {
        city: currentCity.name,
        value: liked ? 1 : 0
      };
      
      await voteCity(voteValue);
      
      // Update state
      const newEvaluatedCount = evaluatedCount + 1;
      setEvaluatedCount(newEvaluatedCount);
      setCurrentIndex(prev => prev + 1);
      
      // Check if we've finished the minimum required evaluations
      if (newEvaluatedCount >= MIN_CITIES_TO_EVALUATE) {
        setVotingComplete(true);
      }
    } catch (err: any) {
      setError('Failed to register your vote. Please try again.');
      console.error(err);
    }
  };

  const handleFinish = () => {
    navigate('/dashboard');
  };

  const currentProgress = (evaluatedCount / MIN_CITIES_TO_EVALUATE) * 100;
  
  return (
    <Container maxW="md" py={8}>
      <VStack spacing={6} align="center">
        <Heading as="h1" size="lg" color="primary.600" textAlign="center">
          Let's Get to Know Your Preferences
        </Heading>

        <Text textAlign="center">
          Swipe right to like or left to dislike these cities.
          We'll use your choices to recommend destinations for you and your friends.
        </Text>

        {error && (
          <Alert status="error" w="100%" borderRadius="md">
            <AlertIcon />
            {error}
          </Alert>
        )}

        <Box 
          p={4} 
          borderWidth={1} 
          borderRadius="lg" 
          boxShadow="lg" 
          w="100%"
          bg="white"
        >
          <VStack spacing={4} align="stretch">
            <Box w="100%">
              <Text fontSize="sm" textAlign="right" color="gray.500" mb={1}>
                {evaluatedCount} of {MIN_CITIES_TO_EVALUATE} cities evaluated
              </Text>
              <Progress
                value={Math.min(currentProgress, 100)}
                size="sm"
                colorScheme="primary"
                borderRadius="full"
              />
            </Box>

            {loading ? (
              <Center p={16}>
                <Spinner size="xl" />
              </Center>
            ) : cities.length === 0 ? (
              <Text textAlign="center" p={8}>
                No cities available for evaluation. Please try again later.
              </Text>
            ) : votingComplete || currentIndex >= cities.length ? (
              <Center flexDirection="column" p={8}>
                <Heading size="md" color="primary.600" mb={4}>
                  Great job!
                </Heading>
                <Text textAlign="center" mb={6}>
                  You've completed the city evaluation. Now we can give you personalized recommendations!
                </Text>
                <Button
                  colorScheme="primary"
                  size="lg"
                  onClick={handleFinish}
                >
                  Go to Dashboard
                </Button>
              </Center>
            ) : (
              <Box h="450px" position="relative" w="100%">
                 {/* Key is important here to force re-render/reset of SwipeableCity when city changes */}
                <SwipeableCity
                  key={cities[currentIndex].name} 
                  city={cities[currentIndex]}
                  onSwipe={handleSwipe}
                />
              </Box>
            )}
          </VStack>
        </Box>

        <Text fontSize="sm" color="gray.500" textAlign="center">
          Swipe right to like, left to dislike, or use the buttons on the card.
        </Text>
      </VStack>
    </Container>
  );
};

export default Onboarding; 