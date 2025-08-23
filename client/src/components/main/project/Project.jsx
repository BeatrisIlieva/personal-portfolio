import { Video } from './video/Video';
import styles from './Project.module.scss';

import { Image } from './image/Image';

export const Project = () => {
    return (
        <section id='project' className={styles['project']}>
            <p>
                DRF React Gems: Full-stack e-commerce platform built with{' '}
                <strong>Django REST Framework</strong> and{' '}
                <strong>React</strong>.
            </p>

            <div className={styles['wrapper']}>
                {/* <div className={styles['relative-container']}>
                    <Image imageName='tablet-rotated.png' />
                    <Image imageName='mobile-rotated.png' />
                </div> */}

                <Video videoName='mockup' />

                <div className={styles['info-wrapper']}>
                    <p>
                        It implements <strong>PostgreSQL</strong> database
                        design and <strong>JWT</strong> authentication. The
                        system utilizes asynchronous processing with{' '}
                        <strong>Celery</strong> and <strong>Redis</strong>.
                        Testing achieved 74% code coverage. The platform is
                        deployed on Azure with Redis Cloud integration.
                    </p>

                    <p>
                        The system includes an AI-powered chatbot built with
                        LangChain. It uses semantic search through Chroma's
                        vector embeddings to match user queries against the
                        product catalog stored in PostgreSQL and deliver
                        relevant recommendations.
                    </p>

                    <div className={styles['buttons-wrapper']}>
                        <button>
                            <a href='https://github.com/BeatrisIlieva/drf-react-gems'>
                                View the app
                            </a>
                        </button>
                        <button>
                            <a href='https://github.com/BeatrisIlieva/drf-react-gems'>
                                View the GitHub repo
                            </a>
                        </button>
                    </div>
                </div>
            </div>
        </section>
    );
};
