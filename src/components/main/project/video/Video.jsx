import { useRef } from 'react';

import styles from './Video.module.scss';

export const Video = ({ videoName }) => {
    const videoRef = useRef(null);

    const handleMouseEnter = () => {
        if (videoRef.current) {
            videoRef.current.play();
        }
    };

    const handleMouseLeave = () => {
        if (videoRef.current) {
            videoRef.current.pause();
            videoRef.current.currentTime = 0;
        }
    };

    return (
        <div className={styles['thumbnail']}>
            <video
                onMouseEnter={handleMouseEnter}
                onMouseLeave={handleMouseLeave}
                ref={videoRef}
                src={`/project-media/${videoName}.mp4`}
                muted
                loop
                playsInline
            />
        </div>
    );
};
