import { faGithub } from '@fortawesome/free-brands-svg-icons';
import { faLinkedin } from '@fortawesome/free-brands-svg-icons';
import { faEnvelope } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import styles from './Header.module.scss';
import { useEffect, useState } from 'react';

const navLinks = [
    { id: 'beatris-ilieva', label: 'Beatris Ilieva' },
    { id: 'experience', label: 'Experience' },
    { id: 'education', label: 'Diploma' },
    { id: 'certificates', label: 'Certificates' },
];

export const Header = () => {
    const [activeSection, setActiveSection] = useState('');

    useEffect(() => {
        const sections = document.querySelectorAll('section[id]');

        const observer = new IntersectionObserver(
            (entries) => {
                const visibleSections = entries
                    .filter((entry) => entry.isIntersecting)
                    .sort((a, b) => {
                        const aTop = a.boundingClientRect.top;
                        const bTop = b.boundingClientRect.top;
                        return Math.abs(aTop) - Math.abs(bTop);
                    });

                if (visibleSections.length > 0) {
                    setActiveSection(visibleSections[0].target.id);
                }
            },
            {
                threshold: 0.1,
                rootMargin: '-80px 0px -80px 0px' // Adjust based on your header height
            }
        );

        sections.forEach((section) => observer.observe(section));

        return () => observer.disconnect();
    }, []);

    return (
        <header className={styles['main-header']}>
            <div className={styles['wrapper']}>
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
