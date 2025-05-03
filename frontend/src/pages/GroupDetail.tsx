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
  Divider,
  List,
  ListItem,
  Avatar,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  FormControl,
  FormLabel,
  Select,
  Input,
  Tag,
  VStack,
  HStack,
  Flex,
  Center,
  Wrap, // Use Wrap for tag rendering
  WrapItem,
  useToast,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  Badge,
} from '@chakra-ui/react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import CityCard from '../components/CityCard';
import { City, Flight, Group, FlightSearch, CityCategory } from '../types';
import {
  getGroupRecommendations,
  getUserGroups,
  getFlightCompanies,
  searchFlights,
  getCities,
} from '../services/api';

const GroupDetail: React.FC = () => {
  const { groupId } = useParams<{ groupId: string }>();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const toast = useToast();
  
  const [tabIndex, setTabIndex] = useState(0);
  const [group, setGroup] = useState<Group | null>(null);
  const [recommendedCities, setRecommendedCities] = useState<City[]>([]);
  const [flights, setFlights] = useState<Flight[]>([]);
  const [flightCompanies, setFlightCompanies] = useState<string[]>([]);
  const [cityList, setCityList] = useState<string[]>([]);
  
  const [loading, setLoading] = useState(true);
  const [flightsLoading, setFlightsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [flightError, setFlightError] = useState<string | null>(null);

  const [selectedCity, setSelectedCity] = useState<City | null>(null);
  const { isOpen: isModalOpen, onOpen: onModalOpen, onClose: onModalClose } = useDisclosure();

  const [flightSearch, setFlightSearch] = useState<FlightSearch>({
    departure_city: '',
    min_date: '2025-05-10', // Keep default dates
    max_date: '2025-05-15',
    max_budget: undefined,
    companies: []
  });

  useEffect(() => {
    // Redirect if not authenticated
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    const fetchData = async () => {
      if (!groupId) return;
      
      try {
        setLoading(true);
        setError(null);
        const groupIdNum = parseInt(groupId, 10);
        
        if (isNaN(groupIdNum)) {
          setError('Invalid Group ID.');
          return;
        }
        
        // Fetch the groups to find the specified one
        const userGroups = await getUserGroups();
        const foundGroup = userGroups.find(g => g.code === groupIdNum);
        
        if (!foundGroup) {
          setError('Group not found or you do not have access to it.');
          return;
        }
        
        setGroup(foundGroup);
        
        // Fetch recommendations for this group
        const recommendations = await getGroupRecommendations(groupIdNum);
        setRecommendedCities(recommendations);
        
        // Fetch additional data for flight search
        const companies = await getFlightCompanies();
        setFlightCompanies(companies);
        
        const cities = await getCities();
        setCityList(cities);
        
        // Set default departure city if list is not empty
        if (cities.length > 0 && !flightSearch.departure_city) {
          setFlightSearch(prev => ({ ...prev, departure_city: cities[0] }));
        }

      } catch (err: any) {
        setError('Failed to load group data. Please try again.');
        console.error(err);
        toast({ title: 'Error Loading Data', description: 'Could not fetch group details.', status: 'error', duration: 5000, isClosable: true });
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [groupId, isAuthenticated, navigate, toast]); // Add toast to dependency array

  const handleTabsChange = (index: number) => {
    setTabIndex(index);
  };

  const handleFlightSearchChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFlightSearch(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Specific handler for multi-select
  const handleCompanyChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const options = e.target.options;
    const value: string[] = [];
    for (let i = 0, l = options.length; i < l; i++) {
      if (options[i].selected) {
        value.push(options[i].value);
      }
    }
    setFlightSearch(prev => ({ ...prev, companies: value }));
  };

  const handleBudgetChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const budget = e.target.value ? parseFloat(e.target.value) : undefined;
    setFlightSearch(prev => ({
      ...prev,
      max_budget: budget
    }));
  };

  const handleSearchFlights = async () => {
    if (!flightSearch.departure_city) {
      setFlightError('Please select a departure city');
      toast({ title: 'Missing Departure City', description: 'Please select a city to fly from.', status: 'warning', duration: 3000, isClosable: true });
      return;
    }

    try {
      setFlightsLoading(true);
      setFlightError(null);
      const results = await searchFlights(flightSearch);
      setFlights(results);
      
      if (results.length > 0) {
        toast({ title: 'Flights Found', description: `Found ${results.length} flight options.`, status: 'success', duration: 3000, isClosable: true });
        setTabIndex(1); // Switch to flights tab only if results found
      } else {
        toast({ title: 'No Flights Found', description: 'Try adjusting your search criteria.', status: 'info', duration: 3000, isClosable: true });
      }
    } catch (err: any) {
      const errorMessage = 'Failed to search for flights. Please try again.';
      setFlightError(errorMessage);
      toast({ title: 'Flight Search Error', description: errorMessage, status: 'error', duration: 5000, isClosable: true });
      console.error(err);
    } finally {
      setFlightsLoading(false);
    }
  };

  const formatFlightTime = (dateTimeStr: string) => {
    try {
      const date = new Date(dateTimeStr);
      if (isNaN(date.getTime())) return "Invalid Date";
      return new Intl.DateTimeFormat('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false, // Use 24-hour format
      }).format(date);
    } catch { 
      return "Invalid Date";
    }
  };

  const formatDuration = (minutes: number) => {
    if (isNaN(minutes)) return "N/A";
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
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

  // Handle potential loading state more gracefully
  if (loading) {
    return (
      <Container maxW="container.lg" py={8}>
        <Center>
          <Spinner size="xl" />
        </Center>
      </Container>
    );
  }

  // Handle error state
  if (error) {
    return (
      <Container maxW="container.lg" py={8}>
        <Alert status="error" borderRadius="md">
          <AlertIcon />
          {error}
        </Alert>
        <Center mt={6}>
           <Button onClick={() => navigate('/groups')} variant="outline">
             Back to Groups
           </Button>
         </Center>
      </Container>
    );
  }

  // Handle case where group is not found after loading
  if (!group) {
     return (
      <Container maxW="container.lg" py={8}>
        <Alert status="warning" borderRadius="md">
          <AlertIcon />
          Group data could not be loaded or found.
        </Alert>
         <Center mt={6}>
           <Button onClick={() => navigate('/groups')} variant="outline">
             Back to Groups
           </Button>
         </Center>
      </Container>
    );
  }

  return (
    <Container maxW="container.lg" py={8}>
      <Flex 
        justifyContent="space-between" 
        alignItems="center" 
        mb={8}
        direction={{ base: 'column', md: 'row' }}
        gap={4}
      >
        <Box>
          <Heading as="h1" size="xl">
            Group #{group.code}
          </Heading>
          <Text color="gray.500">
            {group.members.length} member{group.members.length !== 1 ? 's' : ''}
          </Text>
        </Box>
        <Button 
          variant="outline" 
          onClick={() => navigate('/groups')}
          size="lg"
        >
          Back to Groups
        </Button>
      </Flex>

      <Box borderWidth="1px" borderRadius="lg" boxShadow="lg" p={6} mb={8} bg="white">
        <Heading as="h2" size="lg" mb={4}>
          Members
        </Heading>
        <List spacing={3}>
          {group.members.map((member) => (
            <ListItem key={member} display="flex" alignItems="center">
              <Avatar name={member} size="sm" mr={3} />
              <Text>{member}</Text>
            </ListItem>
          ))}
        </List>
      </Box>

      <Box borderWidth="1px" borderRadius="lg" boxShadow="lg" bg="white">
        <Tabs index={tabIndex} onChange={handleTabsChange} isFitted variant="enclosed-colored" colorScheme="primary">
          <TabList borderTopRadius="lg">
            <Tab>Recommended Destinations</Tab>
            <Tab>Flight Search</Tab>
          </TabList>
          <TabPanels>
            {/* Recommendations Tab */}
            <TabPanel>
              <Box mb={8}>
                <Heading as="h3" size="lg" mb={2}>
                  Group Recommendations
                </Heading>
                <Text color="gray.600" mb={6}>
                  These destinations are recommended based on the preferences of all group members.
                </Text>

                {recommendedCities.length === 0 ? (
                  <Alert status="info" borderRadius="md">
                    <AlertIcon />
                    No recommendations available yet. Ensure group members have evaluated some cities.
                  </Alert>
                ) : (
                  <SimpleGrid columns={{ base: 1, sm: 2, md: 3 }} spacing={6}>
                    {recommendedCities.map((city) => (
                      <CityCard 
                        key={city.name} 
                        city={city} 
                        onClick={() => handleCardClick(city)} 
                      />
                    ))}
                  </SimpleGrid>
                )}
              </Box>

              <Divider my={8} />

              {/* Flight Search Form (Simplified for this tab) */}
              <Box>
                <Heading as="h3" size="lg" mb={4}>
                  Quick Flight Search
                </Heading>
                 <Button 
                   colorScheme="primary"
                   onClick={() => setTabIndex(1)} // Switch to flight tab
                   size="lg"
                 >
                  Go to Full Flight Search
                 </Button>
              </Box>
            </TabPanel>

            {/* Flight Search Tab */}
            <TabPanel>
              <Heading as="h3" size="lg" mb={6}>
                Search for Flights
              </Heading>

              {flightError && (
                <Alert status="error" mb={4} borderRadius="md">
                  <AlertIcon />
                  {flightError}
                </Alert>
              )}
              
              {/* Flight Search Form */}
              <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6} mb={6}>
                <FormControl isRequired>
                  <FormLabel htmlFor="departure_city">Departure City</FormLabel>
                  <Select
                    id="departure_city"
                    name="departure_city"
                    placeholder="Select departure city"
                    value={flightSearch.departure_city}
                    onChange={handleFlightSearchChange}
                  >
                    {cityList.map((city) => (
                      <option key={city} value={city}>
                        {city}
                      </option>
                    ))}
                  </Select>
                </FormControl>

                <FormControl>
                  <FormLabel htmlFor="companies">Airlines (Optional)</FormLabel>
                  <Select
                    id="companies"
                    name="companies"
                    placeholder="Any Airline"
                    multiple // Enable multi-select
                    value={flightSearch.companies || []} // Ensure value is always an array
                    onChange={handleCompanyChange} // Use specific handler
                    height="auto" // Adjust height for multi-select
                  >
                    {flightCompanies.map((company) => (
                      <option key={company} value={company}>
                        {company}
                      </option>
                    ))}
                  </Select>
                   <Wrap mt={2}>
                    {(flightSearch.companies || []).map((company) => (
                      <WrapItem key={company}>
                         <Tag size="md" variant="solid" colorScheme="blue">
                           {company}
                         </Tag>
                       </WrapItem>
                     ))}
                   </Wrap>
                </FormControl>

                <FormControl>
                  <FormLabel htmlFor="min_date">From Date</FormLabel>
                  <Input
                    id="min_date"
                    name="min_date"
                    type="date"
                    value={flightSearch.min_date}
                    onChange={handleFlightSearchChange}
                  />
                </FormControl>
                
                <FormControl>
                  <FormLabel htmlFor="max_date">To Date</FormLabel>
                  <Input
                    id="max_date"
                    name="max_date"
                    type="date"
                    value={flightSearch.max_date}
                    onChange={handleFlightSearchChange}
                  />
                </FormControl>
                
                <FormControl>
                  <FormLabel htmlFor="max_budget">Max Budget ($) (Optional)</FormLabel>
                  <Input
                    id="max_budget"
                    name="max_budget"
                    type="number"
                    placeholder="e.g., 500"
                    value={flightSearch.max_budget || ''}
                    onChange={handleBudgetChange}
                  />
                </FormControl>
              </SimpleGrid>
              
              <Button
                colorScheme="primary"
                onClick={handleSearchFlights}
                isLoading={flightsLoading}
                spinner={<Spinner size="sm" />}
                size="lg"
                mb={8}
              >
                Search Flights
              </Button>

              {/* Flight Results */}             
              <Heading as="h4" size="md" mb={4}>
                Flight Results
              </Heading>
              
              {flightsLoading ? (
                <Center p={8}>
                  <Spinner size="xl" />
                </Center>
              ) : flights.length === 0 ? (
                <Alert status="info" borderRadius="md">
                  <AlertIcon />
                  No flights found matching your criteria. Try adjusting your search.
                </Alert>
              ) : (
                <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
                  {flights.slice(0,10).map((flight) => (
                    <Box key={flight.code} borderWidth="1px" borderRadius="lg" p={4} boxShadow="sm">
                      <Flex justifyContent="space-between" mb={2}>
                        <Heading size="sm">{flight.depCity} → {flight.arrCity}</Heading>
                        <Text fontWeight="bold" color="primary.600">
                          ${flight.cost.toFixed(2)}
                        </Text>
                      </Flex>
                      
                      <Flex justifyContent="space-between" mb={2} fontSize="sm">
                        <Text>{formatFlightTime(flight.depTime)}</Text>
                        <Text color="gray.500">{formatDuration(flight.timeDuration)}</Text>
                      </Flex>
                      
                      <Divider my={3} />
                      
                      <SimpleGrid columns={2} spacing={2} fontSize="sm">
                        <Box>
                          <Text color="gray.500">Airline</Text>
                          <Text>{flight.company}</Text>
                        </Box>
                        <Box>
                          <Text color="gray.500">Aircraft</Text>
                          <Text>{flight.planeModel}</Text>
                        </Box>
                        <Box>
                          <Text color="gray.500">Flight #</Text>
                          <Text>{flight.code}</Text>
                        </Box>
                        <Box>
                          <Text color="gray.500">Distance</Text>
                          <Text>{flight.distance.toFixed(0)} km</Text>
                        </Box>
                      </SimpleGrid>
                      <Flex mt={4} justifyContent="flex-end" gap={2}>
                        <Button size="sm" variant="ghost" colorScheme="blue">
                           Vote This Flight
                         </Button>
                         <Button size="sm" variant="ghost">
                           Share
                         </Button>
                      </Flex>
                    </Box>
                  ))}
                </SimpleGrid>
              )}
              
              <Center mt={8}>
                <Button
                  variant="outline"
                  onClick={() => setTabIndex(0)}
                >
                  Back to Recommendations
                </Button>
              </Center>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </Box>

      {/* --- City Detail Modal --- */}
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
      {/* --- End Modal --- */}

    </Container>
  );
};

export default GroupDetail; 
