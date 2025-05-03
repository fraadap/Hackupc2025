import React from 'react';
import {
  Box,
  Image,
  Heading,
  Text,
  Tag,
  HStack,
  VStack,
  Button,
  Tooltip,
} from '@chakra-ui/react';
import { City } from '../types';

interface CityCardProps {
  city: City;
  showActions?: boolean;
  onLike?: () => void;
  onDislike?: () => void;
}

const CityCard: React.FC<CityCardProps> = ({ 
  city, 
  showActions = false, 
  onLike, 
  onDislike 
}) => {
  // Placeholder image - replace with actual city image logic if available
  const placeholderImage = `https://via.placeholder.com/400x250/CBD5E0/718096?text=${encodeURIComponent(city.name)}`;
  
  // Get top 3 categories to display (assuming they are sorted by relevance/importance)
  const topCategories = city.categories.slice(0, 3);

  return (
    <Box 
      borderWidth="1px" 
      borderRadius="lg" 
      overflow="hidden" 
      boxShadow="md"
      bg="white"
      height="100%"
      display="flex"
      flexDirection="column"
    >
      <Image src={placeholderImage} alt={city.name} objectFit="cover" h="200px" />

      <VStack p={4} spacing={3} align="stretch" flexGrow={1}>
        <Heading as="h3" size="md" >{city.name}</Heading>
        
        <Box flexGrow={1}>
          <Text fontSize="sm" color="gray.600" mb={2}>
            Key Features:
          </Text>
          <VStack spacing={2} align="stretch">
            {topCategories.length > 0 ? (
              topCategories.map((cat) => (
                <Box key={cat.category} >
                  <Tag size="sm" colorScheme="blue" mr={2} mb={1}>{cat.category}</Tag>
                  <Text fontSize="xs" display="inline">{cat.descr}</Text>
                </Box>
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
                colorScheme="red"
                variant="ghost"
                borderRadius="full"
                onClick={onDislike}
              >
                Dislike
              </Button>
            </Tooltip>
            <Tooltip label="Like" placement="bottom">
              <Button
                colorScheme="green"
                variant="ghost"
                borderRadius="full"
                onClick={onLike}
              >
                Like
              </Button>
            </Tooltip>
          </HStack>
        )}
      </VStack>
    </Box>
  );
};

export default CityCard; 