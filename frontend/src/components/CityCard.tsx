import React from 'react';
import {
  Box,
  Image,
  Heading,
  Text,
  HStack,
  VStack,
  Button,
  Tooltip,
  Badge,
  useStyleConfig,
  Icon,
} from '@chakra-ui/react';
import { CloseIcon } from '@chakra-ui/icons';
import { City, CityCategory } from '../types';

interface CityCardProps {
  city: City;
  showActions?: boolean;
  onLike?: () => void;
  onDislike?: () => void;
  onClick?: () => void;
}

const CityCard: React.FC<CityCardProps> = ({ 
  city, 
  showActions = false, 
  onLike, 
  onDislike, 
  onClick,
}) => {
  const placeholderImage = `https://placehold.co/400x250/CBD5E0/718096?text=${encodeURIComponent(city.name)}`;
  
  const sortedCategories = [...city.categories].sort((a: CityCategory, b: CityCategory) => b.value - a.value);
  const topCategories = sortedCategories.slice(0, 3);

  const isClickable = !!onClick && !showActions;

  return (
    <Box 
      onClick={isClickable ? onClick : undefined}
      borderWidth="1px" 
      borderRadius="lg" 
      overflow="hidden" 
      boxShadow="md"
      bg="white"
      height="100%"
      display="flex"
      flexDirection="column"
      _hover={isClickable ? { 
        boxShadow: "lg", 
        cursor: "pointer" 
      } : {}}
      _focus={isClickable ? { boxShadow: "outline" } : {}}
      w="100%"
      p={0}
    >
      <Image src={placeholderImage} alt={city.name} objectFit="cover" h="200px" borderTopRadius="lg" />

      <VStack p={4} spacing={3} align="stretch" flexGrow={1}>
        <Heading as="h3" size="md">{city.name}</Heading>
        
        <Box flexGrow={1}>
          <Text fontSize="sm" color="gray.600" mb={2}>
            Top Features (Rated):
          </Text>
          <VStack spacing={2} align="stretch">
            {topCategories.length > 0 ? (
              topCategories.map((cat) => (
                <HStack key={cat.category} align="center" spacing={2}>
                  <Badge 
                    colorScheme={cat.value > 7 ? 'green' : cat.value < 4 ? 'red' : 'yellow'} 
                    px={2}
                    borderRadius="full"
                    fontSize="0.7em"
                  >
                    {cat.value}/10
                  </Badge>
                  <Text fontSize="sm" fontWeight="medium">{cat.category}</Text>
                </HStack>
              ))
            ) : (
              <Text fontSize="sm" color="gray.500">No category information available.</Text>
            )}
          </VStack>
        </Box>

        {showActions && (
          <HStack justify="space-around" pt={3} borderTopWidth="1px" borderColor="gray.200">
            <Tooltip label="Dislike" placement="bottom">
              <Button
                onClick={onDislike}
                variant="ghost"
                borderRadius="full"
                color="red"
                _hover={{ bg: 'gray.100' }}
                p={2}
              >
                <Icon as={CloseIcon} boxSize={4} />
              </Button>
            </Tooltip>
            <Tooltip label="Like" placement="bottom">
              <Button
                onClick={onLike}
                variant="ghost"
                borderRadius="full"
                _hover={{ bg: 'gray.100' }}
                p={2}
              >
                <Icon viewBox="0 0 24 24" boxSize={6}>
                  <path
                    d="M12 21s-1-.6-2.3-1.8C7.1 17.2 4 14.2 4 10.5 4 7.4 6.4 5 9.5 5c1.5 0 3 .7 3.9 1.9C14.5 5.7 16 5 17.5 5 20.6 5 23 7.4 23 10.5c0 3.7-3.1 6.7-5.7 8.7C13 20.4 12 21 12 21z"
                    fill="blue"
                    stroke="blue"
                    strokeWidth="2"
                  />
                </Icon>
              </Button>
            </Tooltip>
          </HStack>
        )}
      </VStack>
    </Box>
  );
};

export default CityCard;
