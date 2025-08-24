import { About } from './about/About';
import { Certificates } from './ceritficates/Certificates';
import { Chatbot } from './chatbot/Chatbot';
import { Diploma } from './diploma/Diploma';

import styles from './Main.module.scss';
import { Project } from './project/Project';

export const Main = () => {
    return (
        <main className={styles['main']}>
            <About />
            <Project />
            <Diploma />
            <Certificates />
            <Chatbot/>
        </main>
    );
};
