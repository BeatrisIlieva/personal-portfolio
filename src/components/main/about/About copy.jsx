import CircleMatrix from '../../reusable/circle-matrix/CircleMatrix';
import { ZigZag } from '../../reusable/zig-zag/ZigZag';
import styles from './About.module.scss';

export const About = () => {
    return (
        <section id='about' className={styles['about']}>
            <div className={styles['top-wrapper']}>
                <section className={styles['personal-photo']}>
                    <div className={styles['thumbnail']}>
                        <img src='/personal-photo.png' alt='BeatrisIlieva' />
                    </div>
                </section>

                <div className={styles['inner-wrapper']}>
                    <div className={styles['left-border']}>
                        <h3>Education</h3>
                        <p>
                            Graduated from the{' '}
                            <strong>Software Engineering with Python</strong>{' '}
                            program at <em>Software University</em>, achieving
                            excellent grades in all exams.
                        </p>
                    </div>

                    <div className={styles['left-border']}>
                        <h3>Experience</h3>
                        <p>
                            My diploma project is a full-stack e-commerce
                            platform built with{' '}
                            <strong>Django REST Framework</strong> and{' '}
                            <strong>React</strong>. It implements{' '}
                            <strong>PostgreSQL</strong> database design and{' '}
                            <strong>JWT</strong> authentication. The system
                            utilizes asynchronous processing with{' '}
                            <strong>Celery</strong> and <strong>Redis</strong>.
                            Testing achieved 74% code coverage. The platform is
                            deployed on Azure with Redis Cloud integration.
                            
                        </p>
                    </div>
                </div>
            </div>

            <div className={styles['bottom-wrapper']}>
                <div className={styles['top-border']}>
                    <h3>Additional Background</h3>
                    <p>
                        Academic journey includes a{' '}
                        <strong>Master's in Strategic Leadership</strong> from{' '}
                        <em>New Bulgarian University</em> and a{' '}
                        <strong>Bachelor's in Economics</strong> from the{' '}
                        <em>University of National and World Economy</em>.
                    </p>
                </div>
                <div className={styles['left-border']}>
                    <h3>Next Steps</h3>
                    <p>
                        Future plans include continuing education with an{' '}
                        <strong>AI and Machine Learning</strong> program
                        covering data science, machine learning and deep
                        learning.
                    </p>
                </div>
                {/* <button>download cv</button> */}
            </div>
        </section>
    );
};
