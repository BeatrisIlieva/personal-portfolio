import { About } from './about/About';
import { Certificates } from './education/ceritficates/Certificates';
import { Chatbot } from './chatbot/Chatbot';
import { Education } from './education/Education';

import styles from './Main.module.scss';
import { Experience } from './experience/Experience';

export const Main = () => {
    return (
        <main className={styles['main']}>
            <About />
            <Experience />
            <Education />
            {/* <Chatbot/> */}
        </main>
    );
};
