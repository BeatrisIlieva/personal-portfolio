import { faGithub } from '@fortawesome/free-brands-svg-icons';
import { faLinkedin } from '@fortawesome/free-brands-svg-icons';
import { faEnvelope } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import styles from './Header.module.scss';

export const Header = () => {
    return (
        <header className={styles['main-header']}>
            <h1>Beatris Ilieva</h1>

            <ul>
                <li>
                    <a href='https://github.com/BeatrisIlieva' target='_blank'>
                        <FontAwesomeIcon icon={faGithub} />
                    </a>
                </li>
                <li>
                    <a
                        href='https://www.linkedin.com/in/beatrisilieva'
                        target='_blank'
                    >
                        <FontAwesomeIcon icon={faLinkedin} />
                    </a>
                </li>
                <li>
                    <a href='mailto:beatris.ilieva@icloud.com'>
                        <FontAwesomeIcon icon={faEnvelope} />
                    </a>
                </li>
            </ul>
        </header>
    );
};
