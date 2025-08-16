import { useRef } from 'react';

import styles from './Video.module.scss';

export const Video = ({ videoName, text, rowAlignment = null }) => {
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

    const styling = rowAlignment ? 'one-row' : 'two-rows'

    return (
        <article className={styles[styling]}>
            <div className={styles['thumbnail']}>
                <video
                    onMouseEnter={handleMouseEnter}
                    onMouseLeave={handleMouseLeave}
                    ref={videoRef}
                    src={`/project-media/${videoName}.mov`}
                    muted
                    loop
                    playsInline
                />
            </div>
            <p>{text}</p>
        </article>
    );
};
