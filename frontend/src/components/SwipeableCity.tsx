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
  onClick?: () => void;
}

const SwipeableCity = forwardRef<HTMLDivElement, SwipeableCityProps>((
  { city, onSwipe, loading = false, onClick }, 
  ref
) => {
  const [direction, setDirection] = useState<'left' | 'right' | null>(null);

  // Define flyOffDistance in the component scope
  const flyOffDistance = typeof window !== 'undefined' ? window.innerWidth * 1.2 : 600; // Default if window is undefined

  const [{ x, y, rotate, scale }, api] = useSpring(() => ({
    x: 0,
    y: 0,
    rotate: 0,
    scale: 1,
    config: { tension: 400, friction: 30 }
  }));

  const handlers = useSwipeable({
    onSwiping: (e) => {
      const rot = e.deltaX / 15;
      const sc = 1 - Math.abs(e.deltaX) / 1000;
      const yLift = -Math.abs(e.deltaX) / 20;
      
      api.start({
        x: e.deltaX,
        y: yLift,
        rotate: rot,
        scale: sc,
        immediate: true
      });
      
      if (e.deltaX > 50) setDirection('right');
      else if (e.deltaX < -50) setDirection('left');
      else setDirection(null);
    },
    onSwiped: (e) => {
      setDirection(null);
      const threshold = 120;

      const flyOffAnimation = (liked: boolean) => ({
        x: liked ? flyOffDistance : -flyOffDistance,
        y: -100,
        rotate: liked ? 45 : -45,
        scale: 0.8,
        config: { tension: 200, friction: 30 },
        onRest: () => onSwipe(liked),
      });
      
      if (e.deltaX > threshold) {
        api.start(flyOffAnimation(true));
      } else if (e.deltaX < -threshold) {
        api.start(flyOffAnimation(false));
      } else {
        api.start({
          x: 0,
          y: 0,
          rotate: 0,
          scale: 1,
          config: { tension: 400, friction: 30 }
        });
      }
    },
    trackMouse: true,
  });

  const handleLike = () => {
    setDirection('right');
    api.start({
      x: flyOffDistance,
      y: -100,
      rotate: 45,
      scale: 0.8,
      config: { tension: 200, friction: 30 },
      onRest: () => onSwipe(true)
    });
  };

  const handleDislike = () => {
    setDirection('left');
    api.start({
      x: -flyOffDistance,
      y: -100,
      rotate: -45,
      scale: 0.8,
      config: { tension: 200, friction: 30 },
      onRest: () => onSwipe(false)
    });
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
            y,
            rotate,
            scale,
            touchAction: 'none',
            cursor: 'grab'
          }}
          _active={{ cursor: 'grabbing' }}
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
            transition: 'border-color 0.2s ease-in-out, opacity 0.2s ease-in-out',
            zIndex: 10,
            pointerEvents: 'none',
          }}
        >
          <CityCard 
            city={city} 
            showActions 
            onLike={handleLike} 
            onDislike={handleDislike} 
            onClick={onClick}
          />
        </AnimatedBox>
      )}
    </Box>
  );
});

export default SwipeableCity; 