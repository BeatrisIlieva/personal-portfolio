import { Certificates } from './ceritficates/Certificates';
import styles from './Education.module.scss';

export const Education = () => {
    return (
        <section id='education' className={styles['diploma']}>
            <p>
                Graduated from the{' '}
                <strong>Software Engineering with Python</strong> program at{' '}
                <em>Software University</em>, achieving excellent grades in all
                exams.
            </p>

            <div className={styles['wrapper']}>
                <div>
                    <img src='/diploma-1.jpeg' alt='diploma' />
                </div>

                <div>
                    <img src='/diploma-2.jpeg' alt='diploma' />
                </div>

                <div>
                    <img src='/diploma-3.jpeg' alt='diploma' />
                </div>
            </div>

                        <Certificates />
        </section>
    );
};
