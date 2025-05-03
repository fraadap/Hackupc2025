import React from 'react';
import {
  Box,
  Flex,
  Avatar,
  HStack,
  Link as ChakraLink,
  IconButton,
  Button,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuDivider,
  useDisclosure,
  useColorModeValue,
  Stack,
  Container,
  Text,
  Center,
} from '@chakra-ui/react';
import { HamburgerIcon, CloseIcon } from '@chakra-ui/icons';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const NavLink = ({ children, to }: { children: React.ReactNode; to: string }) => (
  <ChakraLink
    as={RouterLink}
    to={to}
    px={2}
    py={1}
    rounded={'md'}
    _hover={{
      textDecoration: 'none',
      bg: useColorModeValue('gray.200', 'gray.700'),
    }}
  >
    {children}
  </ChakraLink>
);

const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const { isOpen, onOpen, onClose } = useDisclosure();
  
  // Extract hook calls outside of conditionals
  const menuListBg = useColorModeValue('white', 'gray.700');
  const menuListColor = useColorModeValue('gray.800', 'white');
  const navbarBg = useColorModeValue('primary.600', 'primary.800');

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <Box bg={navbarBg} px={4} color="white">
      <Container maxW="container.lg">
        <Flex h={16} alignItems={'center'} justifyContent={'space-between'}>
          <IconButton
            size={'md'}
            icon={isOpen ? <CloseIcon /> : <HamburgerIcon />}
            aria-label={'Open Menu'}
            display={{ md: 'none' }}
            onClick={isOpen ? onClose : onOpen}
            variant="ghost"
            _hover={{ bg: 'primary.700' }}
            _active={{ bg: 'primary.700' }}
          />
          <HStack spacing={8} alignItems={'center'}>
            <ChakraLink as={RouterLink} to={isAuthenticated ? '/dashboard' : '/'}>
              <Text fontSize="xl" fontWeight="bold">
                The Perfect Reunion
              </Text>
            </ChakraLink>
            <HStack
              as={'nav'}
              spacing={4}
              display={{ base: 'none', md: 'flex' }}>
              {isAuthenticated && (
                <>
                  <NavLink to="/dashboard">Dashboard</NavLink>
                  <NavLink to="/groups">Groups</NavLink>
                </>
              )}
            </HStack>
          </HStack>
          <Flex alignItems={'center'}>
            {isAuthenticated ? (
              <Menu>
                <MenuButton
                  as={Button}
                  rounded={'full'}
                  variant={'link'}
                  cursor={'pointer'}
                  minW={0}>
                  <Avatar
                    size={'sm'}
                    name={user?.username}
                    bg="secondary.500" // Use secondary color for avatar
                  />
                </MenuButton>
                <MenuList bg={menuListBg} color={menuListColor}>
                  <Center p={2}>
                    <Text fontWeight="bold">{user?.username}</Text>
                  </Center>
                  <MenuDivider />
                  <MenuItem onClick={() => navigate('/dashboard')} display={{ base: 'block', md: 'none' }}>Dashboard</MenuItem>
                  <MenuItem onClick={() => navigate('/groups')} display={{ base: 'block', md: 'none' }}>Groups</MenuItem>
                  <MenuDivider display={{ base: 'block', md: 'none' }}/>
                  <MenuItem onClick={handleLogout}>Logout</MenuItem>
                </MenuList>
              </Menu>
            ) : (
              <HStack spacing={4}>
                 <Button 
                    as={RouterLink} 
                    to="/login"
                    variant="ghost"
                    _hover={{ bg: 'primary.700' }}
                    _active={{ bg: 'primary.700' }}
                 >
                  Login
                 </Button>
                 <Button 
                    as={RouterLink} 
                    to="/register"
                    variant="outline"
                    borderColor="whiteAlpha.500"
                    _hover={{ bg: 'whiteAlpha.200' }}
                 >
                  Register
                 </Button>
              </HStack>
            )}
          </Flex>
        </Flex>

        {isOpen ? (
          <Box pb={4} display={{ md: 'none' }}>
            <Stack as={'nav'} spacing={4}>
              {isAuthenticated ? (
                <>
                  <NavLink to="/dashboard">Dashboard</NavLink>
                  <NavLink to="/groups">Groups</NavLink>
                </>
              ) : null}
            </Stack>
          </Box>
        ) : null}
      </Container>
    </Box>
  );
};

export default Navbar; 