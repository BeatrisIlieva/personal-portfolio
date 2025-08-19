import { Video } from './video/Video';
import styles from './Project.module.scss';

import { Image } from './image/Image';

export const Project = () => {
    return (
        <section id='project' className={styles['project']}>
            <h2>Diploma Project: DRF React Gems</h2>
            <button>
                <a href="https://github.com/BeatrisIlieva/drf-react-gems">View the app</a>
            </button>
            <button>
                <a href="https://github.com/BeatrisIlieva/drf-react-gems">View the GitHub repo</a>
            </button>
            
            

            <div className={styles['wrapper']}>
            <div className={styles['relative-container']}>
                <Image imageName='tablet-rotated.png' />
                <Image imageName='mobile-rotated.png' />
            </div>

            <Video videoName='mockup' />
            </div>

        </section>
    );
};
