import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Heading,
  Text,
  SimpleGrid, // Use SimpleGrid for responsive layout
  Button,
  Spinner,
  Alert,
  AlertIcon,
  Input,
  Divider,
  List,
  ListItem,
  Tag,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
  FormControl,
  FormLabel,
  FormErrorMessage,
  VStack,
  HStack,
  Flex,
  useToast, // Use toast for feedback
  Center, // Add Center import
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Group } from '../types';
import { getUserGroups, createGroup, joinGroup } from '../services/api';

const Groups: React.FC = () => {
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const toast = useToast();
  
  const [groups, setGroups] = useState<Group[]>([]);
  const [loading, setLoading] = useState(true);
  const [joinLoading, setJoinLoading] = useState(false);
  const [createLoading, setCreateLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [joinError, setJoinError] = useState<string | null>(null);
  const [createError, setCreateError] = useState<string | null>(null);
  const [joinCode, setJoinCode] = useState('');
  
  const { isOpen: isCreateOpen, onOpen: onCreateOpen, onClose: onCreateClose } = useDisclosure();

  useEffect(() => {
    // Redirect if not authenticated
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    const fetchGroups = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await getUserGroups();
        setGroups(data);
      } catch (err: any) {
        setError('Failed to load your groups. Please try again.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchGroups();
  }, [isAuthenticated, navigate]);

  const handleJoinGroup = async (e: React.FormEvent) => {
    e.preventDefault();
    setJoinError(null);
    
    if (!joinCode.trim()) {
      setJoinError('Please enter a group code');
      return;
    }

    // Parse the code to integer
    const codeNumber = parseInt(joinCode, 10);
    if (isNaN(codeNumber)) {
      setJoinError('Please enter a valid group code (numbers only)');
      return;
    }

    try {
      setJoinLoading(true);
      const newGroup = await joinGroup(codeNumber);
      setGroups([...groups, newGroup]);
      setJoinCode('');
      toast({ 
        title: 'Group Joined', 
        description: `Successfully joined group #${newGroup.code}`, 
        status: 'success', 
        duration: 3000, 
        isClosable: true 
      });
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to join group. Please check the code and try again.';
      setJoinError(errorMessage);
      toast({ title: 'Join Error', description: errorMessage, status: 'error', duration: 5000, isClosable: true });
      console.error(err);
    } finally {
      setJoinLoading(false);
    }
  };

  const handleCreateGroup = async () => {
    setCreateError(null);
    try {
      setCreateLoading(true);
      const newGroup = await createGroup({});
      setGroups([...groups, newGroup]);
      onCreateClose();
      toast({ 
        title: 'Group Created', 
        description: `Group #${newGroup.code} created. Share this code with friends!`, 
        status: 'success', 
        duration: 5000, 
        isClosable: true 
      });
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to create group. Please try again.';
      setCreateError(errorMessage);
      toast({ title: 'Create Error', description: errorMessage, status: 'error', duration: 5000, isClosable: true });
      console.error(err);
    } finally {
      setCreateLoading(false);
    }
  };

  const handleViewGroup = (group: Group) => {
    navigate(`/groups/${group.code}`);
  };

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
            Your Groups
          </Heading>
          {user && (
            <Text color="gray.500">
              Create or join groups to plan your perfect reunion
            </Text>
          )}
        </Box>
        <HStack spacing={4}>
          <Button 
            colorScheme="primary" 
            onClick={onCreateOpen}
            size="lg"
          >
            Create New Group
          </Button>
          <Button 
            variant="outline" 
            onClick={() => navigate('/dashboard')}
            size="lg"
          >
            Back to Dashboard
          </Button>
        </HStack>
      </Flex>

      {error && (
        <Alert status="error" mb={6} borderRadius="md">
          <AlertIcon />
          {error}
        </Alert>
      )}

      <SimpleGrid columns={{ base: 1, md: 2 }} spacing={8}>
        {/* Your Groups Section */}
        <Box borderWidth="1px" borderRadius="lg" boxShadow="lg" p={6} bg="white">
          <Heading as="h2" size="lg" mb={4}>
            Your Groups
          </Heading>
          
          {loading ? (
            <Center p={8}>
              <Spinner size="xl" />
            </Center>
          ) : groups.length === 0 ? (
            <Center p={6}>
              <Text color="gray.500">
                You're not part of any groups yet. Create or join one!
              </Text>
            </Center>
          ) : (
            <List spacing={3}>
              {groups.map((group, index) => (
                <React.Fragment key={group.code}>
                  <ListItem 
                    display="flex"
                    justifyContent="space-between"
                    alignItems="center"
                    py={3}
                  >
                    <VStack align="start" spacing={1}>
                      <HStack>
                        <Heading size="md">Group #{group.code}</Heading>
                        <Tag size="sm" colorScheme="blue" variant="outline">
                          {group.members.length} member{group.members.length !== 1 ? 's' : ''}
                        </Tag>
                      </HStack>
                      <Text fontSize="sm" color="gray.500">
                        Members: {group.members.join(', ')}
                      </Text>
                    </VStack>
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => handleViewGroup(group)}
                    >
                      View Details
                    </Button>
                  </ListItem>
                  {index < groups.length - 1 && <Divider />} 
                </React.Fragment>
              ))}
            </List>
          )}
        </Box>

        {/* Join Group Section */}
        <Box borderWidth="1px" borderRadius="lg" boxShadow="lg" p={6} bg="white">
          <Heading as="h2" size="lg" mb={6}>
            Join a Group
          </Heading>
          
          <Box as="form" onSubmit={handleJoinGroup}>
            <VStack spacing={4}>
              <FormControl isInvalid={!!joinError} isDisabled={joinLoading}>
                <FormLabel htmlFor="joinCode">Group Code</FormLabel>
                <Input
                  id="joinCode"
                  placeholder="Enter group code"
                  value={joinCode}
                  onChange={(e) => setJoinCode(e.target.value)}
                  type="number" // Ensure numeric input for code
                />
                <FormErrorMessage>{joinError}</FormErrorMessage>
              </FormControl>
              <Button
                type="submit"
                width="full"
                colorScheme="primary"
                isLoading={joinLoading}
                spinner={<Spinner size="sm" />}
                py={6}
              >
                Join Group
              </Button>
            </VStack>
          </Box>
        </Box>
      </SimpleGrid>

      {/* Create Group Modal */}
      <Modal isOpen={isCreateOpen} onClose={onCreateClose} isCentered>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Create a New Group</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Text mb={4}>
              Creating a new group will generate a unique code that you can share with friends to invite them.
            </Text>
            {createError && (
              <Alert status="error" mb={4} borderRadius="md">
                <AlertIcon />
                {createError}
              </Alert>
            )}
          </ModalBody>
          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={onCreateClose}>
              Cancel
            </Button>
            <Button 
              colorScheme="primary" 
              onClick={handleCreateGroup} 
              isLoading={createLoading}
              spinner={<Spinner size="sm" />}
            >
              Create Group
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Container>
  );
};

export default Groups; 