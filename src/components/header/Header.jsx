import { faGithub } from '@fortawesome/free-brands-svg-icons';
import { faLinkedin } from '@fortawesome/free-brands-svg-icons';
import { faEnvelope } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import styles from './Header.module.scss';
import { useEffect, useState } from 'react';

const navLinks = [
    { id: 'about', label: 'About' },
    { id: 'project', label: 'Project' },
    { id: 'diploma', label: 'Diploma' },
    { id: 'certificates', label: 'Certificates' }
];

export const Header = () => {
    const [activeSection, setActiveSection] = useState('');

    useEffect(() => {
        const sections = document.querySelectorAll('section[id]');

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        setActiveSection(entry.target.id);
                    }
                });
            },
            { threshold: 0.6 } // section considered active when 60% visible
        );

        sections.forEach((section) => observer.observe(section));

        return () => observer.disconnect();
    }, []);

    return (
        <header className={styles['main-header']}>
            <div className={styles['wrapper']}>
                <h1>Beatris Ilieva</h1>

                <ul>
                    {navLinks.map(({ id, label }) => (
                        <li key={id}>
                            <a
                                href={`#${id}`}
                                className={
                                    activeSection === id ? styles.active : ''
                                }
                            >
                                {label}
                            </a>
                        </li>
                    ))}
                </ul>

                <ul>
                    <li>
                        <a
                            href='https://github.com/BeatrisIlieva'
                            target='_blank'
                        >
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
            </div>
        </header>
    );
};
