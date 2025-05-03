import React, { useState, forwardRef } from 'react';
import { useSwipeable } from 'react-swipeable';
import { animated, useSpring } from 'react-spring';
import { Box, Spinner } from '@chakra-ui/react';
import { City } from '../types';
import CityCard from './CityCard';

interface SwipeableCityProps {
  city: City;
  onSwipe: (liked: boolean) => void;
  loading?: boolean;
}

const SwipeableCity = forwardRef<HTMLDivElement, SwipeableCityProps>((
  { city, onSwipe, loading = false }, 
  ref
) => {
  const [direction, setDirection] = useState<'left' | 'right' | null>(null);

  const [{ x, rotate, scale }, api] = useSpring(() => ({
    x: 0,
    rotate: 0,
    scale: 1,
    config: { tension: 300, friction: 20 }
  }));

  const handlers = useSwipeable({
    onSwiping: (e) => {
      api.start({
        x: e.deltaX,
        rotate: e.deltaX / 20,
        scale: 1,
      });
      
      if (e.deltaX > 50) setDirection('right');
      else if (e.deltaX < -50) setDirection('left');
      else setDirection(null);
    },
    onSwiped: (e) => {
      const threshold = 120;
      
      if (e.deltaX > threshold) {
        api.start({
          x: 500,
          rotate: 30,
          onRest: () => onSwipe(true),
        });
      } else if (e.deltaX < -threshold) {
        api.start({
          x: -500,
          rotate: -30,
          onRest: () => onSwipe(false),
        });
      } else {
        api.start({
          x: 0,
          rotate: 0,
          scale: 1,
        });
        setDirection(null);
      }
    },
    trackMouse: true,
  });

  const handleLike = () => {
    api.start({
      x: 500,
      rotate: 30,
      onRest: () => onSwipe(true),
    });
    setDirection('right');
  };

  const handleDislike = () => {
    api.start({
      x: -500,
      rotate: -30,
      onRest: () => onSwipe(false),
    });
    setDirection('left');
  };

  const AnimatedBox = animated(Box);

  return (
    <Box sx={{ position: 'relative', height: '100%', userSelect: 'none' }} ref={ref}>
      {loading ? (
        <Box display="flex" justifyContent="center" alignItems="center" height="100%">
          <Spinner size="xl" />
        </Box>
      ) : (
        <AnimatedBox
          {...handlers}
          style={{
            x,
            rotate,
            scale,
            touchAction: 'none',
          }}
          _before={{
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            borderRadius: 'lg',
            borderWidth: '8px',
            borderStyle: 'solid',
            borderColor: direction === 'right' ? 'green.300' : direction === 'left' ? 'red.300' : 'transparent',
            opacity: direction ? 0.5 : 0,
            zIndex: 10,
            pointerEvents: 'none',
          }}
        >
          <CityCard city={city} showActions onLike={handleLike} onDislike={handleDislike} />
        </AnimatedBox>
      )}
    </Box>
  );
});

export default SwipeableCity; 