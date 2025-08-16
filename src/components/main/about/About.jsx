import styles from './About.module.scss';

export const About = () => {
    return (
        <section id='about' className={styles['about']}>
            <div>
                <img src='/personal-photo-blue.jpg' alt='BeatrisIlieva' />
            </div>

            <div>
                <p>
                    Graduated with highest honors in a{' '}
                    <strong>Software Engineering with Python</strong> program at{' '}
                    <em>Software University</em>, earning excellent grades in
                    all exams.
                </p>
                <p>
                    My diploma project is a full-stack e-commerce platform built
                    with Django REST Framework and React, PostgreSQL database
                    design, and JWT authentication. The system implements
                    asynchronous processing with Celery and Redis. It achieved
                    74% test coverage. The platform is deployed on Azure with
                    Redis Cloud integration.
                </p>
                <p>
                    Future plans include continuing education with an AI and
                    Machine Learning program covering data science, machine
                    learning, and deep learning to build expertise in modern AI
                    development.
                </p>
            </div>
        </section>
    );
};
