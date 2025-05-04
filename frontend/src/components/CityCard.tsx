import React, { useState } from 'react';
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
  Icon,
  Spinner,
  Center,
} from '@chakra-ui/react';
import { CloseIcon } from '@chakra-ui/icons';
import { City, CityCategory } from '../types';

interface CityCardProps {
  city: City;
  showActions?: boolean;
  onTriggerLike?: () => void;
  onTriggerDislike?: () => void;
  onClick?: () => void;
}

const CityCard: React.FC<CityCardProps> = ({ 
  city, 
  showActions = false, 
  onTriggerLike, 
  onTriggerDislike, 
  onClick,
}) => {
  const [isImageLoading, setIsImageLoading] = useState(true);
  const [imageError, setImageError] = useState(false);

  const hasImage = city.image_ids && city.image_ids.length > 0;
  const imageId = hasImage ? city.image_ids[0] : null;
  const backendUrl = 'http://localhost:8000';
  const imageUrl = imageId ? `${backendUrl}/images/${imageId}` : null;
  const displayImageUrl = imageError || !imageUrl 
    ? `https://placehold.co/400x250/CBD5E0/718096?text=${encodeURIComponent(city.name)}`
    : imageUrl;

  const sortedCategories = [...city.categories].sort((a: CityCategory, b: CityCategory) => b.value - a.value);
  const topCategories = sortedCategories.slice(0, 3);
  const isClickable = !!onClick;

  const handleLikeButtonClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();
    if (onTriggerLike) {
      onTriggerLike();
    }
  };

  const handleDislikeButtonClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();
    if (onTriggerDislike) {
      onTriggerDislike();
    }
  };

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
      p={0}
      _hover={isClickable ? { 
        boxShadow: "lg", 
        cursor: "pointer" 
      } : {}}
      _focus={isClickable ? { 
        outline: "2px solid",
        outlineColor: "primary.500",
        outlineOffset: "2px"
      } : {}}
      w="100%"
      position="relative"
    >
      <Box position="relative" h="200px" bg="gray.200">
        {isImageLoading && !imageError && (
          <Center position="absolute" inset="0" bg="rgba(255,255,255,0.5)">
            <Spinner size="lg" color="primary.500"/>
          </Center>
        )}
        {imageError && (
          <Center position="absolute" inset="0" bg="rgba(255,255,255,0.5)">
            <Text color="red.500">Error loading image</Text>
          </Center>
        )}
        <Image 
          src={displayImageUrl} 
          alt={city.name} 
          objectFit="cover" 
          h="100%" 
          w="100%"
          borderTopRadius="lg"
          onLoad={() => { if(imageUrl) setIsImageLoading(false); } }
          onError={() => {
            setIsImageLoading(false);
            setImageError(true);
            console.error(`Failed to load image: ${imageUrl}`);
          }}
          opacity={isImageLoading && !imageError ? 0.5 : 1}
          transition="opacity 0.3s ease-in-out"
          key={displayImageUrl}
        />
      </Box>

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
                onClick={handleDislikeButtonClick}
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
                onClick={handleLikeButtonClick}
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
