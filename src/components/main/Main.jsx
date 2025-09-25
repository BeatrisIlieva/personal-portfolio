import { useEffect, useRef } from 'react';
import { About } from './about/About';
import { Certificates } from './ceritficates/Certificates';
import { Diploma } from './diploma/Diploma';
import { Experience } from './experience/Experience';

import styles from './Main.module.scss';

const useScrollAnimation = (options = {}) => {
    const ref = useRef(null);

    const {
        threshold = 0.1,
        rootMargin = '0px 0px -50px 0px',
        animationClass = 'fadeInVisible'
    } = options;

    useEffect(() => {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add(animationClass);
                    } else {
                        entry.target.classList.remove(animationClass);
                    }
                });
            },
            { threshold, rootMargin }
        );

        const sections = ref.current?.querySelectorAll('section');
        sections?.forEach((section) => {
            observer.observe(section);
        });

        return () => {
            sections?.forEach((section) => {
                observer.unobserve(section);
            });
        };
    }, [threshold, rootMargin, animationClass]);

    return ref;
};

export const Main = () => {
    const mainRef = useScrollAnimation({
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px',
        animationClass: styles.fadeInVisible
    });

    return (
        <main className={styles.main} ref={mainRef}>
            <About />
            <Experience />
            <Diploma />
            <Certificates />
        </main>
    );
};
