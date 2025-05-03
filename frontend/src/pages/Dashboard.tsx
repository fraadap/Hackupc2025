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
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  List,
  ListItem,
  ListIcon,
  Badge,
  HStack,
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import CityCard from '../components/CityCard';
import SwipeableCity from '../components/SwipeableCity';
import { City, CityCategory } from '../types';
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
  const [selectedCity, setSelectedCity] = useState<City | null>(null);

  const { isOpen: isModalOpen, onOpen: onModalOpen, onClose: onModalClose } = useDisclosure();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    const fetchRecommendations = async () => {
      try {
        setLoading(true);
        const data = await getRecommendations(15);
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

  useEffect(() => {
    if (tabIndex === 1 && !newCityToEvaluate && !evaluationLoading) {
      handleLoadNextCity();
    }
  }, [tabIndex]);

  const handleTabsChange = (index: number) => {
    setTabIndex(index);
  };

  const handleLoadNextCity = async () => {
    try {
      setEvaluationLoading(true);
      setError(null);
      const cities = await getCitiesForEvaluation(1);
      if (cities.length > 0) {
        setNewCityToEvaluate(cities[0]);
      } else {
        setNewCityToEvaluate(null);
        setError("You've evaluated all available cities!"); 
        setTabIndex(0);
      }
    } catch (err: any) {
      setError('Failed to load a new city for evaluation. Please try again.');
      console.error(err);
      setNewCityToEvaluate(null); 
      setTabIndex(0); 
    } finally {
      setEvaluationLoading(false);
    }
  };

  const handleCityEvaluation = async (liked: boolean) => {
    if (!newCityToEvaluate) return;
    const cityNameToVote = newCityToEvaluate.name;
    handleLoadNextCity(); 
    
    try {
      await voteCity({
        city: cityNameToVote,
        value: liked ? 1 : 0
      });
      
      const newRecommendations = await getRecommendations(15);
      setRecommendedCities(newRecommendations);

    } catch (err: any) {
      console.error('Failed background vote/recommendation update:', err);
    }
  };

  const handleGroupsNav = () => {
    navigate('/groups');
  };

  const handleCardClick = (city: City) => {
    const sortedCity = {
      ...city,
      categories: [...(city.categories || [])].sort((a, b) => b.value - a.value),
    };
    setSelectedCity(sortedCity);
    onModalOpen();
  };

  const renderSortedCategories = (categories: CityCategory[]) => {
    if (!categories || categories.length === 0) {
      return <Text>No category details available.</Text>;
    }
    return (
      <VStack spacing={4} align="stretch">
        {categories.map((cat) => (
          <Box 
            key={cat.category} 
            p={3} 
            borderWidth="1px" 
            borderRadius="md" 
            borderColor="gray.200"
            bg="gray.50"
          >
            <HStack justify="space-between" mb={1}>
              <Text as="span" fontWeight="bold" fontSize="lg">
                {cat.category}
              </Text>
              <Badge 
                colorScheme={cat.value > 7 ? 'green' : cat.value < 4 ? 'red' : 'yellow'} 
                px={3}
                py={1}
                borderRadius="full"
                fontSize="sm"
              >
                {cat.value}/10
              </Badge>
            </HStack>
            <Text fontSize="md" color="gray.700">{cat.descr}</Text> 
          </Box>
        ))}
      </VStack>
    );
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
            <Tab>Evaluate More Cities</Tab>
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
                    onClick={handleLoadNextCity}
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
                      <CityCard 
                        key={city.name} 
                        city={city} 
                        onClick={() => handleCardClick(city)}
                      />
                    ))}
                  </SimpleGrid>

                  <Center pt={4}>
                    <Button
                      variant="outline"
                      colorScheme="primary"
                      onClick={handleLoadNextCity}
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
              <Center p={4} minH="450px">
                {evaluationLoading && !newCityToEvaluate ? (
                  <Spinner size="xl" />
                ) : newCityToEvaluate ? (
                  <Box maxW="sm" w="100%" h="400px">
                    <SwipeableCity 
                      key={newCityToEvaluate.name}
                      city={newCityToEvaluate} 
                      onSwipe={handleCityEvaluation}
                      loading={false}
                      onClick={() => handleCardClick(newCityToEvaluate)}
                    />
                    <Text color="gray.500" textAlign="center" mt={4} fontSize="sm">
                      Swipe right to like, left to dislike, or use the buttons.
                    </Text>
                  </Box>
                ) : (
                  <Center flexDirection="column" p={8}>
                    <Text mb={4} textAlign="center">
                      {error || "Ready to evaluate more cities? Click the button below to start."}
                  </Text>
                    <Button
                      colorScheme="primary"
                      onClick={handleLoadNextCity}
                      isLoading={evaluationLoading}
                      spinner={<Spinner size="sm" />}
                    >
                      {error ? "Try Again" : "Load a City to Evaluate"}
                    </Button>
                  </Center>
                )}
              </Center>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </Box>

      {selectedCity && (
        <Modal isOpen={isModalOpen} onClose={onModalClose} size="xl" scrollBehavior="inside" isCentered>
          <ModalOverlay bg="blackAlpha.600"/>
          <ModalContent mx={4}>
            <ModalHeader borderBottomWidth="1px" pb={3}>{selectedCity.name} - Details</ModalHeader>
            <ModalCloseButton />
            <ModalBody py={5}>
              {renderSortedCategories(selectedCity.categories)}
            </ModalBody>
            <ModalFooter borderTopWidth="1px" pt={3}>
              <Button colorScheme="primary" onClick={onModalClose}>
                Close
              </Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
      )}
    </Container>
  );
};

export default Dashboard; 