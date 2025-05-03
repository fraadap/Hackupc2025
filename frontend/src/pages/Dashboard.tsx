import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Heading,
  Text,
  Grid,
  SimpleGrid,
  Button,
  Spinner,
  Alert,
  AlertIcon,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Center,
  Flex,
  VStack,
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import CityCard from '../components/CityCard';
import { City } from '../types';
import { getRecommendations, getCitiesForEvaluation, voteCity } from '../services/api';

const Dashboard: React.FC = () => {
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  
  const [recommendedCities, setRecommendedCities] = useState<City[]>([]);
  const [newCityToEvaluate, setNewCityToEvaluate] = useState<City | null>(null);
  const [loading, setLoading] = useState(true);
  const [evaluationLoading, setEvaluationLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [tabIndex, setTabIndex] = useState(0);

  useEffect(() => {
    // Redirect if not authenticated
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    const fetchRecommendations = async () => {
      try {
        setLoading(true);
        const data = await getRecommendations(10);
        setRecommendedCities(data);
      } catch (err: any) {
        setError('Failed to load recommendations. Please try again.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, [isAuthenticated, navigate]);

  const handleTabsChange = (index: number) => {
    setTabIndex(index);
  };

  const handleEvaluateMore = async () => {
    try {
      setEvaluationLoading(true);
      const cities = await getCitiesForEvaluation(1);
      if (cities.length > 0) {
        setNewCityToEvaluate(cities[0]);
        setTabIndex(1); // Switch to the evaluate tab
      } else {
        setError("No more cities to evaluate right now."); // Inform user if no cities
      }
    } catch (err: any) {
      setError('Failed to load a new city for evaluation. Please try again.');
      console.error(err);
    } finally {
      setEvaluationLoading(false);
    }
  };

  const handleVote = async (liked: boolean) => {
    if (!newCityToEvaluate) return;

    try {
      setEvaluationLoading(true);
      setError(null); // Clear previous errors
      
      // Submit vote
      await voteCity({
        city: newCityToEvaluate.name,
        value: liked ? 1 : 0
      });
      
      // Refresh recommendations after voting
      const newRecommendations = await getRecommendations(10);
      setRecommendedCities(newRecommendations);
      
      // Load a new city to evaluate immediately
      const cities = await getCitiesForEvaluation(1);
      if (cities.length > 0) {
        setNewCityToEvaluate(cities[0]);
      } else {
        setNewCityToEvaluate(null);
        setTabIndex(0); // Go back to recommendations if no more cities
        setError("You've evaluated all available cities!"); // Inform user
      }
    } catch (err: any) {
      setError('Failed to register your vote or fetch new data. Please try again.');
      console.error(err);
      setNewCityToEvaluate(null); // Clear city on error
      setTabIndex(0); // Go back to recommendations on error
    } finally {
      setEvaluationLoading(false);
    }
  };

  const handleGroupsNav = () => {
    navigate('/groups');
  };

  return (
    <Container maxW="container.lg" py={8}>
      <Flex 
        justifyContent="space-between" 
        alignItems="center" 
        mb={8}
        direction={{ base: 'column', md: 'row' }} // Stack on mobile
        gap={4}
      >
        <Box>
          <Heading as="h1" size="xl">
            Your Perfect Destinations
          </Heading>
          {user && (
            <Text color="gray.500">
              Welcome back, {user.username}!
            </Text>
          )}
        </Box>
        <Button 
          colorScheme="primary" 
          onClick={handleGroupsNav}
          size="lg"
        >
          Manage Groups
        </Button>
      </Flex>

      {error && (
        <Alert status="error" mb={6} borderRadius="md">
          <AlertIcon />
          {error}
        </Alert>
      )}

      <Box borderWidth="1px" borderRadius="lg" boxShadow="lg" bg="white">
        <Tabs index={tabIndex} onChange={handleTabsChange} isFitted variant="enclosed-colored" colorScheme="primary">
          <TabList borderTopRadius="lg">
            <Tab>Recommended Cities</Tab>
            <Tab isDisabled={!newCityToEvaluate && !evaluationLoading}>Evaluate More Cities</Tab>
          </TabList>
          <TabPanels>
            <TabPanel>
              {loading ? (
                <Center p={16}>
                  <Spinner size="xl" />
                </Center>
              ) : recommendedCities.length === 0 ? (
                <Center flexDirection="column" p={8}>
                  <Text mb={4}>
                    You don't have any recommendations yet. Let's evaluate some more cities!
                  </Text>
                  <Button
                    colorScheme="primary"
                    onClick={handleEvaluateMore}
                    isLoading={evaluationLoading}
                    spinner={<Spinner size="sm" />}
                  >
                    Evaluate Cities
                  </Button>
                </Center>
              ) : (
                <VStack spacing={6} align="stretch">
                  <SimpleGrid columns={{ base: 1, sm: 2, md: 3 }} spacing={6}>
                    {recommendedCities.map((city) => (
                      <CityCard key={city.name} city={city} />
                    ))}
                  </SimpleGrid>

                  <Center pt={4}>
                    <Button
                      variant="outline"
                      colorScheme="primary"
                      onClick={handleEvaluateMore}
                      isLoading={evaluationLoading}
                      spinner={<Spinner size="sm" />}
                    >
                      Evaluate More Cities
                    </Button>
                  </Center>
                </VStack>
              )}
            </TabPanel>

            <TabPanel>
              <Center p={4}>
                {evaluationLoading ? (
                  <Spinner size="xl" />
                ) : newCityToEvaluate ? (
                  <Box maxW="sm" w="100%">
                    <CityCard 
                      city={newCityToEvaluate} 
                      showActions 
                      onLike={() => handleVote(true)} 
                      onDislike={() => handleVote(false)} 
                    />
                    <Text color="gray.500" textAlign="center" mt={4} fontSize="sm">
                      Swipe right to like, left to dislike, or use the buttons.
                    </Text>
                  </Box>
                ) : (
                  <Text>
                    Click "Evaluate More Cities" on the Recommendations tab to get started.
                  </Text>
                )}
              </Center>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </Box>
    </Container>
  );
};

export default Dashboard; 