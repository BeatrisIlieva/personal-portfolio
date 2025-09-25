import styles from './Experience.module.scss';

import { Image } from './image/Image';

export const Experience = () => {
    return (
        <section id='experience' className={styles['project']}>
            <p>
                DRF React Gems: Full-stack e-commerce platform built with{' '}
                <strong>Django REST Framework</strong>, <strong>React</strong>,{' '}
                <strong>LangChain</strong> and <strong>Pinecone</strong>.
            </p>

            <div className={styles['wrapper']}>
                <div className={styles['info-wrapper']}>
                    <p>
                        A full-stack luxury jewelry e-commerce platform built
                        with <strong>Django REST Framework</strong> (DRF)
                        backend and <strong>React</strong> frontend. The
                        platform implements <strong>JTW</strong> authentication,
                        shopping cart and wishlist management, payment
                        processing, order history, and asynchronous email
                        notifications using <strong>Celery</strong> and{' '}
                        <strong>Redis</strong>.
                    </p>

                    <p>
                        An AI-powered jewelry consultation system that serves as
                        an intelligent virtual consultant, guides customers
                        through personalized product discovery. Built using
                        technologies such as <strong>LangChain</strong>,{' '}
                        <strong>OpenAI GPT-4.1</strong>,{' '}
                        <strong>Pinecone</strong> vector database, the chatbot
                        combines luxury retail expertise to deliver tailored
                        jewelry recommendations based on customer preferences
                        and available inventory.
                    </p>
                </div>

                <Image imageName='mobile-tablet.png' />
            </div>

            <div className={styles['buttons-wrapper']}>
                <a href='https://drf-react-gems.web.app' target='_blank'>
                    Website
                </a>
                <a
                    href='https://github.com/BeatrisIlieva/drf-react-gems'
                    target='_blank'
                >
                    GitHub
                </a>
            </div>
        </section>
    );
};
